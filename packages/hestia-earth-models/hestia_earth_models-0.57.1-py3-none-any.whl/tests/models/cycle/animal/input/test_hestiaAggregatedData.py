from unittest.mock import patch
import json

from tests.utils import fixtures_path
from hestia_earth.models.cycle.animal.input.hestiaAggregatedData import MODEL_ID, run, _should_run_animal

class_path = f"hestia_earth.models.cycle.animal.input.{MODEL_ID}"
fixtures_folder = f"{fixtures_path}/cycle/animal/input/{MODEL_ID}"

IMPACT_ASSESSMENT = {
    "@id": "wheatGrain-australia-2000-2009",
    "@type": "ImpactAssessment",
    "name": "Wheat, grain, Australia, 2000-2009",
    "endDate": "2009"
}


def fake_search(query, **args):
    match_name = query['bool']['must'][2]['bool']['should'][0]['match']['product.term.name.keyword']
    return [IMPACT_ASSESSMENT] if match_name != 'Seed' else []


def test_should_run():
    cycle = {}
    animal = {}

    # no inputs => no run
    animal['inputs'] = []
    should_run, *args = _should_run_animal(cycle, animal)
    assert not should_run

    # with inputs and no impactAssessment => no run
    animal['inputs'] = [{}]
    should_run, *args = _should_run_animal(cycle, animal)
    assert not should_run

    # with endDate => run
    cycle['endDate'] = {'2019'}
    should_run, *args = _should_run_animal(cycle, animal)
    assert should_run is True


@patch('hestia_earth.models.utils.aggregated.search', side_effect=fake_search)
def test_run(*args):
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(cycle)
    assert result == expected
