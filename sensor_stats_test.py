import pytest

from sensor_stats import average, find_alarms, moving_average, normalize, summary


def test_average():
    assert average([10.0, 20.0, 30.0]) == 20.0


def test_average_empty():
    assert average([]) == 0.0


def test_moving_average():
    assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]


def test_moving_average_invalid_window():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)


def test_normalize():
    assert normalize([0.0, 5.0, 10.0]) == [0.0, 0.5, 1.0]


def test_normalize_constant_signal():
    assert normalize([3.0, 3.0, 3.0]) == [0.0, 0.0, 0.0]


def test_find_alarms():
    readings = [
        {"sensor": "pressure", "value": 7.1},
        {"sensor": "temperature", "value": 65.0},
    ]
    assert find_alarms(readings) == ["pressure: 7.1 > 6.5"]


def test_find_alarms_skips_unknown_sensor():
    readings = [
        {"sensor": "humidity", "value": 80.0},
        {"sensor": "vibration", "value": 15.0},
    ]
    assert find_alarms(readings) == ["vibration: 15.0 > 12.0"]


def test_summary():
    assert summary([1.0, 2.0, 4.0]) == {"min": 1.0, "max": 4.0, "avg": 2.33, "count": 3}