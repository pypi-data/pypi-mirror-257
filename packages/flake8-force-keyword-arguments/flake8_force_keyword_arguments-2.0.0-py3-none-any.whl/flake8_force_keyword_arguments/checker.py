import ast
import importlib
import re
import sys
from argparse import Namespace
from itertools import chain
from typing import ClassVar, Final, Iterable, Tuple, Type

import flake8_force_keyword_arguments
from flake8.options.manager import OptionManager
from flake8_force_keyword_arguments import util
from marisa_trie import Trie

if sys.version_info < (3, 9):
    from typing import Pattern
else:
    from re import Pattern

DEFAULT_MAX_POS_ARGS: Final[int] = 2
DEFAULT_IGNORE_PATTERNS: Final[str] = (
    r'(:?'
    r'^logger.(:?log|debug|info|warning|error|exception|critical)$'
    r'|__setattr__$'
    r'|__delattr__$'
    r'|__getattr__$'
    r'|^(:?typing\.)?cast$'
    r')'
)
DEFAULT_INSPECT_MODULES: Final[Tuple[str, ...]] = ('builtins',)
DEFAULT_QUALIFIER_OPTION: Final[util.QualifierOption] = util.QualifierOption.BOTH


class Checker:
    name: Final[str] = flake8_force_keyword_arguments.__name__
    version: Final[str] = flake8_force_keyword_arguments.__version__
    MESSAGE_TEMPLATE: Final[str] = (
        'FKA100 {function_name}\'s call uses {number_of_args} positional arguments, use keyword arguments.'
    )

    _max_pos_args: ClassVar[int] = DEFAULT_MAX_POS_ARGS
    _ignore_patterns: ClassVar[Tuple[Pattern[str], ...]] = ()
    _ignore_trie: ClassVar[Trie]

    _tree: ast.AST

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        parser.add_option(  # pragma: no cover
            '--kwargs-max-positional-arguments',
            type=int,
            dest='max_positional_arguments',
            default=DEFAULT_MAX_POS_ARGS,
            parse_from_config=True,
            help='How many positional arguments are allowed (default: %(default)s)',
        )
        parser.add_option(  # pragma: no cover
            '--kwargs-ignore-function-pattern',
            type=str,
            dest='ignore_function_pattern',
            default=DEFAULT_IGNORE_PATTERNS,
            parse_from_config=True,
            help='Ignore pattern list (default: %(default)s)',
        )
        parser.add_option(  # pragma: no cover
            '--kwargs-ignore-function-pattern-extend',
            type=str,
            dest='ignore_function_pattern_extend',
            default=None,
            parse_from_config=True,
            help='Extend ignore pattern list.',
        )
        parser.add_option(  # pragma: no cover
            '--kwargs-inspect-module',
            dest='inspect_module',
            comma_separated_list=True,
            default=DEFAULT_INSPECT_MODULES,
            parse_from_config=True,
            help=(
                'Inspect module level constructor of classes or functions to gather positional only callables '
                'and ignore it on lint. Note that methods are not subject to inspection. (default: %(default)s)'
            ),
        )
        parser.add_option(  # pragma: no cover
            '--kwargs-inspect-module-extend',
            dest='inspect_module_extend',
            comma_separated_list=True,
            default=(),
            parse_from_config=True,
            help='Extend --kwargs-inspect-module',
        )
        parser.add_option(  # pragma: no cover
            '--kwargs-inspect-qualifier-option',
            type=util.QualifierOption,
            dest='inspect_qualifier_option',
            choices=tuple(v.value for v in util.QualifierOption.__members__.values()),
            default=DEFAULT_QUALIFIER_OPTION.value,
            parse_from_config=True,
            help=(
                'For detected positional only callables by inspection, option to append the qualifier or not. '
                'e.g. In case builtins.setattr(), '
                '`both` will register `builtins.setattr` and `setattr` as positional only function. '
                '`only_name` will register `setattr` and `only_with_qualifier` will register `builtins.setattr`. '
                '(default: %(default)s)'
            ),
        )

    @classmethod
    def parse_options(cls, options: Namespace) -> None:
        cls._max_pos_args = options.max_positional_arguments

        ignore_patterns = (options.ignore_function_pattern, options.ignore_function_pattern_extend)
        cls._ignore_patterns = tuple(map(re.compile, filter(None, ignore_patterns)))

        qualifier_option = options.inspect_qualifier_option

        cls._ignore_trie = Trie(
            chain.from_iterable(
                util.list_pos_only_callables(
                    m=importlib.import_module(module_name),
                    parent_module_qualifier=module_name,
                    poa_threshold=cls._max_pos_args,
                    qualifier_option=qualifier_option,
                )
                for module_name in chain(options.inspect_module, options.inspect_module_extend)
            )
        )

    def run(self) -> Iterable[Tuple[int, int, str, Type['Checker']]]:
        for node in ast.walk(self._tree):
            if not isinstance(node, ast.Call) or len(node.args) < self._max_pos_args:
                continue

            invocation_line = util.get_invocation_line(node)

            # ignored because of patterns
            if any(p.search(invocation_line) for p in self._ignore_patterns):
                continue

            # ignored because of inspection
            if invocation_line in self._ignore_trie:
                continue

            message = self.MESSAGE_TEMPLATE.format(function_name=invocation_line, number_of_args=len(node.args))
            yield node.lineno, node.col_offset, message, type(self)
