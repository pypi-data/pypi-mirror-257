from typing import Optional

from hestia_earth.schema import MeasurementMethodClassification
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.source import get_source
from hestia_earth.models.utils.measurement import (
    _new_measurement, group_measurements_by_depth, _group_measurement_key, measurement_value
)
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "measurements": [
            {
                "@type": "Measurement",
                "value": "",
                "term.@id": "soilBulkDensity",
                "depthUpper": "",
                "depthLower": ""
            },
            {
                "@type": "Measurement",
                "value": "",
                "term.@id": "organicCarbonPerKgSoil",
                "depthUpper": "",
                "depthLower": ""
            }
        ]
    }
}
RETURNS = {
    "Measurement": [{
        "value": "",
        "depthUpper": "",
        "depthLower": "",
        "methodClassification": "modelled using other measurements"
    }]
}
TERM_ID = 'organicCarbonPerHa'
BIBLIO_TITLE = 'Soil organic carbon sequestration rates in vineyard agroecosystems under different soil management practices: A meta-analysis'  # noqa: E501
RESCALE_DEPTH_UPPER = 0
RESCALE_DEPTH_LOWER = 30


def _measurement(site: dict, value: float, depthUpper: int, depthLower: int, date: Optional[str] = None):
    data = _new_measurement(TERM_ID)
    data['value'] = [value]
    data['depthUpper'] = depthUpper
    data['depthLower'] = depthLower
    data['methodClassification'] = MeasurementMethodClassification.MODELLED_USING_OTHER_MEASUREMENTS.value
    if date is not None:
        data['dates'] = [date]
    return data | get_source(site, BIBLIO_TITLE)


def _should_run_rescale(measurements: list):
    return any([m for m in measurements if all([
            m.get('depthUpper', 1) == RESCALE_DEPTH_UPPER,
            m.get('depthLower', 101) <= 100
    ])]) and not any([m for m in measurements if all([
            m.get('depthUpper', 1) == RESCALE_DEPTH_UPPER,
            m.get('depthLower', 101) == RESCALE_DEPTH_LOWER
    ])])


def _c_to_depth(d: float) -> float:
    """
    The definite integral of `c_density_at_depth` between `0` and `d`.

    Parameters
    ----------
    d : float
        Measurement depth in meters (min `0`, max `1`).

    Returns
    -------
    float
        The carbon stock per m2 to depth `d`, kg C-2.
    """
    return 22.1 * d - (33.3 * pow(d, 2)) / 2 + (14.9 * pow(d, 3)) / 3


def _cdf(depth_upper: float, depth_lower: float) -> float:
    """
    The ratio between the carbon stock per m2 to depth `d` and the carbon
    stock per meter to depth `1`.

    Parameters
    ----------
    depth_upper : float
        Measurement depth upper in meters (min `0`, max `1`).
    depth_lower : float
        Measurement depth lower in meters (min `0`, max `1`).

    Returns
    -------
    float
        The proportion of carbon stored between `depth_upper` and `depth_lower` compared to between `0` and `1` meters.
    """
    return (_c_to_depth(depth_lower) - _c_to_depth(depth_upper)) / _c_to_depth(1)


def _rescale_soc_value(
    source_value: float,
    source_depth_upper: float,
    source_depth_lower: float,
    target_depth_upper: float,
    target_depth_lower: float
) -> float:
    """
    Rescale an SOC measurement value from a source depth interval to a target depth interval.

    Depths are converted from centimetres (Hestia schema) to metres for use in `cdf` function.

    Parameters
    ----------
    source_value : float
        Source SOC stock (kg C ha-1).
    source_depth_upper : float
        Source measurement depth upper in centimetres (min `0`, max `100`).
    source_depth_lower : float
        Source measurement depth lower in centimetres, must be greater than `source_depth_upper` (min `0`, max `100`).
    target_depth_upper : float
        Target measurement depth upper in centimetres (min `0`, max `100`).
    target_depth_lower : float
        Target measurement depth lower in centimetres, must be greater than `target_depth_upper` (min `0`, max `100`).

    Returns
    -------
    float
        The estimated SOC stock for the target depth interval (kg C ha-1).
    """
    cd_target = _cdf(target_depth_upper/100, target_depth_lower/100)
    cd_measurement = _cdf(source_depth_upper/100, source_depth_lower/100)
    return source_value * (cd_target / cd_measurement)


def _get_last_date(dates: list[str]) -> str:
    """
    Reduces a node's dates field down to a single date. As the `arrayTreatment` for `organicCarbonPerKgSoil` and
    `organicCarbonPerHa` is `mean` the latest date should be selected.
    """
    return sorted(dates)[-1] if len(dates) > 0 else None


def _run_rescale(site: dict, measurements: list):
    measurements = [m for m in measurements if all([
            m.get('depthUpper', 1) == RESCALE_DEPTH_UPPER,
            m.get('depthLower', 101) <= 100
    ])]
    # order measurements by depthLower and use the biggest
    measurement = sorted(measurements, key=lambda x: x.get('depthLower'))[-1] if len(measurements) > 0 else None

    value = _rescale_soc_value(
        measurement_value(measurement),
        RESCALE_DEPTH_UPPER, measurement.get('depthLower'),
        RESCALE_DEPTH_UPPER, RESCALE_DEPTH_LOWER,
    ) if measurement else None

    date = _get_last_date(measurement.get("dates", [])) if measurement else None

    return [_measurement(site, value, RESCALE_DEPTH_UPPER, RESCALE_DEPTH_LOWER, date)] if value is not None else []


def _run(site: dict, measurements: list):
    soilBulkDensity = measurement_value(find_term_match(measurements, 'soilBulkDensity'))
    organicCarbonPerKgSoil = find_term_match(measurements, 'organicCarbonPerKgSoil')
    organicCarbonPerKgSoil_value = measurement_value(organicCarbonPerKgSoil)

    value = (
        organicCarbonPerKgSoil.get('depthLower') - organicCarbonPerKgSoil.get('depthUpper')
    ) * soilBulkDensity * (organicCarbonPerKgSoil_value/10) * 1000

    depthUpper = organicCarbonPerKgSoil.get('depthUpper')
    depthLower = organicCarbonPerKgSoil.get('depthLower')
    date = _get_last_date(organicCarbonPerKgSoil.get("dates", []))

    return _measurement(site, value, depthUpper, depthLower, date)


def _should_run_measurements(site: dict, measurements: list):
    soilBulkDensity = find_term_match(measurements, 'soilBulkDensity', None)
    has_soilBulkDensity_depthLower = (soilBulkDensity or {}).get('depthLower') is not None
    has_soilBulkDensity_depthUpper = (soilBulkDensity or {}).get('depthUpper') is not None
    organicCarbonPerKgSoil = find_term_match(measurements, 'organicCarbonPerKgSoil', None)
    has_organicCarbonPerKgSoil_depthLower = (organicCarbonPerKgSoil or {}).get('depthLower') is not None
    has_organicCarbonPerKgSoil_depthUpper = (organicCarbonPerKgSoil or {}).get('depthUpper') is not None

    depth_logs = {
        _group_measurement_key(measurements[0], include_dates=False): ';'.join([
            '_'.join([
                'id:soilBulkDensity',
                f"hasDepthLower:{has_soilBulkDensity_depthLower}",
                f"hasDepthUpper:{has_soilBulkDensity_depthUpper}"
            ]),
            '_'.join([
                'id:organicCarbonPerKgSoil',
                f"hasDepthLower:{has_organicCarbonPerKgSoil_depthLower}",
                f"hasDepthUpper:{has_organicCarbonPerKgSoil_depthUpper}"
            ])
        ])
    } if len(measurements) > 0 else {}

    logRequirements(site, model=MODEL, term=TERM_ID,
                    **depth_logs)

    should_run = all([
        has_soilBulkDensity_depthLower, has_soilBulkDensity_depthUpper,
        has_organicCarbonPerKgSoil_depthLower, has_organicCarbonPerKgSoil_depthUpper
    ])
    return should_run


def _should_run(site: dict):
    grouped_measurements = list(group_measurements_by_depth(site.get('measurements', [])).values())
    values = [(measurements, _should_run_measurements(site, measurements)) for measurements in grouped_measurements]
    should_run = any([_should_run for measurements, _should_run in values])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return should_run, [measurements for measurements, _should_run in values if _should_run]


def run(site: dict):
    should_run, values = _should_run(site)
    calculated_measurements = [_run(site, value) for value in values] if should_run else []

    # rescale from existing and added measurements matching Term
    all_measurements = [
        m for m in (site.get('measurements', []) + calculated_measurements)
        if m.get('term', {}).get('@id') == TERM_ID
    ]
    return calculated_measurements + (
        _run_rescale(site, all_measurements) if _should_run_rescale(all_measurements) else []
    )
