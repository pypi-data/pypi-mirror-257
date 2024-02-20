from unittest.mock import patch
import json
from hestia_earth.schema import TermTermType

from tests.utils import fixtures_path, fake_new_emission
from hestia_earth.models.ipcc2006.n2OToAirExcretaDirect import MODEL, TERM_ID, run, _should_run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}._is_term_type_complete", return_value=False)
def test_should_run(mock_is_complete, *args):
    # no inputs => no run
    cycle = {'inputs': []}
    should_run, *args = _should_run(cycle)
    assert not should_run

    # is complete => run
    mock_is_complete.return_value = True
    should_run, *args = _should_run(cycle)
    assert should_run is True

    # with kg N inputs => run
    cycle['inputs'] = [{
        'term': {
            'units': 'kg N',
            'termType': TermTermType.EXCRETA.value
        },
        'value': [100]
    }]
    should_run, *args = _should_run(cycle)
    assert should_run is True


@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
def test_run(*args):
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
def test_run_with_product_sheep(*args):
    with open(f"{fixtures_folder}/with-product-sheep/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/with-product-sheep/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
def test_run_with_product_goat(*args):
    with open(f"{fixtures_folder}/with-product-goat/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/with-product-goat/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
