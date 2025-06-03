import pytest
from datetime import datetime, time, date
from app.utils.time_calc import calculate_hours_for_day

@pytest.mark.parametrize("punches, configs, expected", [
    # Caso: un solo intervallo 09:00-17:00, fascia 09:00-18:00 => ore ord 8.0, extra 0.0
    (
        [(datetime(2025, 6, 1, 9, 0), True), (datetime(2025, 6, 1, 17, 0), False)],
        [(time(9,0), time(18,0), None, None)],
        (8.0, 0.0)
    ),
    # Caso: intervallo 08:00-19:00, fascia 09:00-18:00 => ore ord 9.0, extra 2.0
    (
        [(datetime(2025, 6, 2, 8, 0), True), (datetime(2025, 6, 2, 19, 0), False)],
        [(time(9,0), time(18,0), None, None)],
        (9.0, 2.0)
    ),
])
def test_calculate_hours(punches, configs, expected):
    ore = calculate_hours_for_day(date(2025, 6, 1), punches, configs)
    assert ore == expected
