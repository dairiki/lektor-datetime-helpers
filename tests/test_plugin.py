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


class TestComparableDate(object):
    def make_one(self, year=1970, month=1, day=1):
        from lektor_datetime_helpers import comparable_date
        return comparable_date(year, month, day)

    def test_compare_to_date(self):
        left = self.make_one(1970, 1, 2)
        assert left == date(1970, 1, 2)

    def test_compare_to_naive_datetime(self):
        left = self.make_one(1970, 1, 2)
        assert left < datetime(1970, 1, 2)
        assert left > datetime(1970, 1, 1, 23, 59, 59)

    def test_compare_to_tzaware_datetime(self):
        left = self.make_one(1970, 1, 2)
        assert left < datetime(1970, 1, 2, tzinfo=UTC)
        assert left > datetime(1970, 1, 1, 23, 59, 59, tzinfo=UTC)

    def test_compare_to_integer(self):
        left = self.make_one(1970, 1, 2)
        with pytest.raises(TypeError):
            left < 0

    def test_compare_to_none(self):
        left = self.make_one(date.min.year, date.min.month, date.min.day)
        assert left > None


class TestComparableDatetime(object):
    def make_one(self, year=1970, month=1, day=1,
                 hour=0, minute=0, second=0, tzinfo=None):
        from lektor_datetime_helpers import comparable_datetime
        return comparable_datetime(year, month, day,
                                   hour, minute, second, tzinfo=tzinfo)

    def test_compare_to_date(self):
        left = self.make_one(1970, 1, 2)
        assert left > date(1970, 1, 2)
        assert left < date(1970, 1, 3)

    def test_compare_to_naive_datetime(self):
        left = self.make_one(1970, 1, 2)
        assert left == datetime(1970, 1, 2)

    def test_compare_to_tzaware_datetime(self):
        left = self.make_one(1970, 1, 2)
        left < datetime(1970, 1, 2, tzinfo=UTC)

    def test_compare_to_integer(self):
        left = self.make_one(1970, 1, 2)
        with pytest.raises(TypeError):
            left < 0

    def test_compare_to_none(self):
        left = self.make_one(
            datetime.min.year, datetime.min.month, datetime.min.day,
            datetime.min.hour, datetime.min.minute, datetime.min.second)
        assert left > None


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
