import json
from pytest import mark
from unittest.mock import patch

from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.site.organicCarbonPerHa import (
    MODEL, TERM_ID, run, _cdf, _c_to_depth, _get_last_date, _should_run_measurements
)

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"

SUBFOLDERS = ["calculate", "rescale", "calculate-and-rescale"]


@mark.parametrize("depth, expected", [(0, 0), (1, 10.41666666666667)], ids=["0m", "1m"])
def test_c_to_depth(depth, expected):
    assert _c_to_depth(depth) == expected


@mark.parametrize(
    "depth_upper, depth_lower, expected",
    [(0, 0, 0), (0, 0.3, 0.5054975999999999), (0, 1, 1)],
    ids=["0-0m", "0-0.3m", "0-1m"]
)
def test_cdf(depth_upper, depth_lower, expected):
    assert _cdf(depth_upper, depth_lower) == expected


@mark.parametrize(
    "dates, expected",
    [
        (["2020", "2021", "2020"], "2021"),
        (["2020-01", "2020-02"], "2020-02"),
        (["2020-01-01", "2020-02-28"], "2020-02-28"),
        ([], None)
    ],
    ids=["YYYY", "YYYY-MM", "YYYY-MM-DD", "Empty list"]
)
def test_get_node_date(dates, expected):
    assert _get_last_date(dates) == expected


@patch(f"{class_path}.find_term_match")
def test_should_run_measurements(mock_find):
    # no measurement => no run
    mock_find.return_value = {}
    assert not _should_run_measurements({}, [])

    # with measurement => run
    mock_find.return_value = {'value': [10], 'depthUpper': 0, 'depthLower': 10}
    assert _should_run_measurements({}, []) is True


@mark.parametrize("subfolder", SUBFOLDERS)
@patch(f"{class_path}.get_source", return_value={})
@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
def test_run(_new_measurement_mock, get_source_mock, subfolder):
    with open(f"{fixtures_folder}/{subfolder}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    with open(f"{fixtures_folder}/{subfolder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(site)
    assert value == expected
