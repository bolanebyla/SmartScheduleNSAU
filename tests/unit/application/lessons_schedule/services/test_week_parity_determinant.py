import pytest
import pytz

from smart_schedule_nsau.application.lessons_schedule import (
    WeekParityDeterminant,
)


@pytest.fixture(scope='function')
def service(tz_info: pytz.timezone):
    return WeekParityDeterminant(tz_info=tz_info)
