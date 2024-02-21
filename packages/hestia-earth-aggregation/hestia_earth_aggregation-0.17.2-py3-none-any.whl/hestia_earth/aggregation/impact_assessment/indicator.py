from hestia_earth.schema import IndicatorJSONLD, IndicatorStatsDefinition
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.tools import flatten

from hestia_earth.aggregation.utils import _aggregated_version, _unique_nodes
from hestia_earth.aggregation.utils.term import METHOD_MODEL


def _new_indicator(data: dict, value: float = None, include_methodModel=False, nodes: list = []):
    node = IndicatorJSONLD().to_dict()
    node['term'] = linked_node(data.get('term', {}))
    node['methodModel'] = linked_node(data.get('methodModel')) if include_methodModel else METHOD_MODEL
    if value is not None:
        node['value'] = value
        node['statsDefinition'] = IndicatorStatsDefinition.IMPACTASSESSMENTS.value

    inputs = flatten([n.get('inputs', []) for n in nodes])
    if len(inputs) > 0:
        node['inputs'] = list(map(linked_node, _unique_nodes(inputs)))

    return _aggregated_version(node, 'term', 'methodModel', 'statsDefinition', 'value')
