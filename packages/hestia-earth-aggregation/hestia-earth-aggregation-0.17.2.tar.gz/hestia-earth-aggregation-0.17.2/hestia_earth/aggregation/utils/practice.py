from hestia_earth.schema import TermTermType
from hestia_earth.utils.tools import flatten


_PRACTICE_AGGREGATE_TERM_TYPES = [
    TermTermType.CROPRESIDUEMANAGEMENT.value,
    TermTermType.LANDCOVER.value,
    TermTermType.TILLAGE.value,
    TermTermType.WATERREGIME.value
]


def _is_complete(practices: list, termType: str):
    all_practices = [p for p in practices if all([
        p.get('term', {}).get('termType') == termType,
        p.get('term', {}).get('units', '').startswith('%')
    ])]
    sum_all_practices = sum(flatten([p.get('value', []) for p in all_practices]))

    # do not aggregate if the sum of all termType is not around 100%
    return all([
        termType in _PRACTICE_AGGREGATE_TERM_TYPES,
        99.5 <= sum_all_practices <= 100.5
    ])


def is_complete(node: dict, termType: str):
    return _is_complete(node.get('practices', []), termType)


def filter_practices(practices: list):
    return list(filter(lambda p: _is_complete(practices, p.get('term', {}).get('termType')), practices))
