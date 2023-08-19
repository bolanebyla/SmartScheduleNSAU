import pytest
import pytz


@pytest.fixture(scope='function')
def tz_info():
    return pytz.timezone('Asia/Novosibirsk')
