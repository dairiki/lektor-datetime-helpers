from datetime import date, datetime

from jinja2 import Undefined
from lektor import types
import pytest
from pytz import UTC


@pytest.fixture
def env():
    return DummyEnv()


def raw_value(value):
    name = 'test'
    field = None
    pad = None
    return types.RawValue(name, value, field, pad)


class TestDateOrDateTimeType(object):
    @pytest.fixture
    def type_(self, env):
        from lektor_datetime_helpers import DateOrDateTimeType
        options = None
        return DateOrDateTimeType(env, options)

    def test_missing(self, type_):
        value = type_.value_from_raw(raw_value(None))
        assert isinstance(value, Undefined)
        assert not isinstance(value, types.BadValue)

    def test_date(self, type_):
        value = type_.value_from_raw(raw_value('2017-04-01'))
        assert isinstance(value, date)

    def test_datetime(self, type_):
        value = type_.value_from_raw(raw_value('2017-04-01 12:04'))
        assert isinstance(value, datetime)

    def test_bad_value(self, type_):
        value = type_.value_from_raw(raw_value('Not a date'))
        assert isinstance(value, types.BadValue)


class TestPlugin(object):
    @pytest.fixture
    def plugin(self, env):
        from lektor_datetime_helpers import DatetimeHelpersPlugin
        id_ = 'test-plugin'
        return DatetimeHelpersPlugin(env, id_)

    def test_localize_aware_datetime(self, plugin):
        dt = datetime(2017, 4, 1, 12, 34, tzinfo=UTC)
        localized = plugin.localize_datetime(dt)
        assert localized is dt

    def test_localize_naive_datetime(self, plugin):
        plugin.on_setup_env()
        dt = datetime(2017, 4, 1, 12, 34)
        localized = plugin.localize_datetime(dt)
        assert localized is not dt
        assert localized == plugin.default_timezone.localize(dt)

    def test_isoformat(self, plugin):
        dt = date(2017, 4, 1)
        assert plugin.isoformat(dt) == '2017-04-01'


class DummyEnv(object):
    def __init__(self):
        self.jinja_env = DummyJinjaEnv()
        self.types = set()

    def add_type(self, type_):
        self.types.add(type_)


class DummyJinjaEnv(object):
    def __init__(self):
        self.filters = {}
