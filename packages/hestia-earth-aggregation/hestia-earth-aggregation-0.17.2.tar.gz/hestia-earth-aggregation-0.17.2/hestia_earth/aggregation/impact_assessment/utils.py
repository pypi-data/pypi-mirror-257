from functools import reduce
from hestia_earth.schema import NodeType, TermTermType
from hestia_earth.utils.api import node_exists, download_hestia
from hestia_earth.utils.model import linked_node, find_term_match
from hestia_earth.utils.tools import non_empty_list, list_sum, list_average, flatten

from hestia_earth.aggregation.utils import (
    _unique_nodes, _aggregated_version, _aggregated_node, _set_dict_single, sum_values
)
from hestia_earth.aggregation.utils.queries import _download_node
from hestia_earth.aggregation.utils.term import (
    _update_country, _format_country_name, _format_irrigated, _format_organic, _group_by_term_id
)
from hestia_earth.aggregation.utils.source import format_aggregated_sources
from hestia_earth.aggregation.utils.quality_score import KEY as QUALITY_SCORE_KEY, KEY_MAX as QUALITY_SCORE_KEY_MAX
from .indicator import _new_indicator

AGGREGATION_KEYS = ['emissionsResourceUse', 'impacts', 'endpoints']


def get_product(impact_assessment: dict) -> dict:
    """
    Get the full `Product` from the `ImpactAssessment.cycle`.

    Parameters
    ----------
    impact_assessment : dict
        The `ImpactAssessment`.

    Returns
    -------
    dict
        The `Product` of the `ImpactAssessment`.
    """
    product = impact_assessment.get('product', {})
    products = impact_assessment.get('cycle', {}).get('products', [])
    return find_term_match(products, product.get('@id'))


def _format_aggregate(aggregate: dict, include_methodModel=False):
    value = aggregate.get('value')
    min = aggregate.get('min')
    max = aggregate.get('max')
    sd = aggregate.get('sd')
    observations = aggregate.get('observations')
    node = _new_indicator(aggregate.get('node'), value, include_methodModel, aggregate.get('nodes', []))
    _set_dict_single(node, 'observations', observations)
    _set_dict_single(node, 'min', min)
    _set_dict_single(node, 'max', max)
    _set_dict_single(node, 'sd', sd, True)
    return _aggregated_version(node, 'min', 'max', 'sd', 'observations')


def _format_aggregated_impacts(cycles: list):
    all_cycles = non_empty_list(flatten([v.get('aggregatedImpactAssessments', v) for v in cycles]))
    return list(map(linked_node, all_cycles))


def _format_terms_results(results: tuple):
    emissionsResourceUse, data = results.get('emissionsResourceUse')
    impacts, _ = results.get('impacts')
    endpoints, _ = results.get('endpoints')
    nodes = data.get('nodes', [])
    return {
        **_create_impact_assessment(nodes),
        'emissionsResourceUse': list(map(lambda v: _format_aggregate(v, False), emissionsResourceUse)),
        'impacts': list(map(lambda v: _format_aggregate(v, True), impacts)),
        'endpoints': list(map(lambda v: _format_aggregate(v, True), endpoints)),
        'aggregatedImpactAssessments': _format_aggregated_impacts(nodes),
        'aggregatedSources': format_aggregated_sources(nodes)
    } if len(nodes) > 0 else None


def _format_country_results(results: tuple):
    _, data = results.get('emissionsResourceUse')
    nodes = data.get('nodes', [])
    impact = nodes[0] if len(nodes) > 0 else None
    return {
        **_format_world_results(results),
        'name': _impact_assessment_name(impact, False),
        'id': _impact_assessment_id(impact, False),
        'aggregatedImpactAssessments': _format_aggregated_impacts(nodes),
        'aggregatedSources': format_aggregated_sources(nodes)
    } if impact else None


def _format_world_results(results: tuple):
    _, data = results.get('emissionsResourceUse')
    nodes = data.get('nodes', [])
    return {
        **_format_terms_results(results),
        'organic': False,
        'irrigated': False,
        'aggregatedImpactAssessments': _format_aggregated_impacts(nodes),
        'aggregatedSources': format_aggregated_sources(nodes)
    }


def _cycle_productValue(impact: dict):
    impact['cycle'] = _download_node('recalculated')(impact.get('cycle', {})) or {}
    return list_sum(get_product(impact).get('value', []))


def _get_productValue(impact: dict):
    # only created since version `11.2.0`, fallback to getting value from Cycle otherwise
    is_crop = impact.get('product', {}).get('term', {}).get('termType') == TermTermType.CROP.value
    return (
        list_sum(impact.get('product', {}).get('value', []), None) or _cycle_productValue(impact) or 1
    ) if is_crop else 1


def _merge_emissions(values: list):
    emission = values[0]
    value = sum_values(v.get('value', 0) for v in values)
    return {**emission, 'value': value, 'inputs': _unique_nodes(flatten([n.get('inputs', []) for n in values]))}


def _format_for_grouping(impacts: dict):
    def format(impact: dict):
        # we need to sum up all emissionsResourceUse with the same `term` first before aggregating
        emissions = reduce(_group_by_term_id(True), impact.get('emissionsResourceUse', []), {})
        emissions = [_merge_emissions(value) for value in emissions.values() if len(value) > 0]
        return {
            **impact,
            'emissionsResourceUse': emissions,
            'productValue': _get_productValue(impact)
        }
    return list(map(format, impacts))


def _impact_assessment_id(n: dict, include_matrix=True):
    # TODO: handle impacts that dont have organic/irrigated version => only 1 final version
    return '-'.join(non_empty_list([
        n.get('product', {}).get('term', {}).get('@id'),
        _format_country_name(n.get('country', {}).get('name')),
        _format_organic(n.get('organic', False)) if include_matrix else '',
        _format_irrigated(n.get('irrigated', False)) if include_matrix else '',
        n.get('startDate'),
        n.get('endDate')
    ]))


def _impact_assessment_name(n: dict, include_matrix=True):
    return ' - '.join(non_empty_list([
        n.get('product', {}).get('term', {}).get('name'),
        n.get('country', {}).get('name'),
        ', '.join(non_empty_list([
            ('Organic' if n.get('organic', False) else 'Conventional') if include_matrix else '',
            ('Irrigated' if n.get('irrigated', False) else 'Non Irrigated') if include_matrix else ''
        ])),
        '-'.join([n.get('startDate'), n.get('endDate')])
    ]))


def _create_impact_assessment(nodes: list):
    data = nodes[0]

    impact = {'type': NodeType.IMPACTASSESSMENT.value}
    # copy properties from existing ImpactAssessment
    impact['startDate'] = data.get('startDate')
    impact['endDate'] = data.get('endDate')
    product = data.get('product', {})
    impact['product'] = {
        '@type': 'Product',
        'term': product.get('term'),
        'value': [
            list_average(flatten([node.get('product', {}).get('value', [1]) for node in nodes]), 1)
        ],
        'economicValueShare': list_average(flatten([
            node.get('product', {}).get('economicValueShare', 100) for node in nodes
        ]), 100)
    }
    impact['functionalUnitQuantity'] = data.get('functionalUnitQuantity')
    impact['allocationMethod'] = data.get('allocationMethod')
    impact['organic'] = data.get('organic', False)
    impact['irrigated'] = data.get('irrigated', False)
    impact['dataPrivate'] = False
    if data.get('country'):
        impact['country'] = data['country']
    return _aggregated_node(impact)


def _update_impact_assessment(country_name: str, start: int, end: int, source: dict = None, include_matrix=True):
    def update(impact: dict):
        impact['startDate'] = str(start)
        impact['endDate'] = str(end)
        impact['country'] = _update_country(country_name) if country_name else impact.get('country')
        impact['name'] = _impact_assessment_name(impact, include_matrix)
        id = _impact_assessment_id(impact, include_matrix)
        impact['id'] = id
        cycle = download_hestia(id, NodeType.CYCLE)
        cycle_id = (cycle or {}).get('@id')
        # cannot aggregate without a Cycle
        if cycle_id:
            impact['cycle'] = linked_node(cycle)
            impact[QUALITY_SCORE_KEY] = cycle.get(QUALITY_SCORE_KEY, 0)
            impact[QUALITY_SCORE_KEY_MAX] = cycle.get(QUALITY_SCORE_KEY_MAX, 3)
            if node_exists(id, NodeType.SITE):
                impact['site'] = linked_node({'@type': NodeType.SITE.value, '@id': id})
            return impact if source is None else {**impact, 'source': source}
        return None
    return update
