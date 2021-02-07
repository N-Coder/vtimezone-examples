from collections import defaultdict
from datetime import datetime, timezone, timedelta, tzinfo
from pprint import pprint
from typing import NamedTuple, List

from dateutil.rrule import rrule, rruleset, YEARLY

try:
    from zoneinfo._zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo._zoneinfo import ZoneInfo

from ics.timezone import Timezone, TimezoneStandardObservance, TimezoneDaylightObservance


class TimezoneTransitionInfo(NamedTuple("TimezoneTransitionInfo", [
    ("tzoffsetfrom", timedelta),
    ("tzoffsetto", timedelta),
    ("dst", timedelta),
    ("tzname", str),
])):
    @classmethod
    def from_transition_dt(cls, trans_tz: datetime):
        before_tz = trans_tz - timedelta(minutes=1)
        return cls(
            tzoffsetfrom=before_tz.utcoffset(),
            tzoffsetto=trans_tz.utcoffset(),
            dst=trans_tz.dst(),
            tzname=trans_tz.tzname()
        )

    def to_vtimezone_observance(self, rrule):
        cls = TimezoneDaylightObservance if bool(self.dst) else TimezoneStandardObservance
        return cls(tzoffsetfrom=self.tzoffsetfrom, tzoffsetto=self.tzoffsetto, rrule=rrule, tzname=self.tzname)


def convert_rdates(dates: List[datetime]):
    rrules = rruleset()
    dates.sort()
    rrules.rrule(rrule(YEARLY, count=1, dtstart=dates.pop(0).replace(tzinfo=None)))
    for dt in dates:
        rrules.rdate(dt.replace(tzinfo=None))
    return [rrules]


def convert_timezone(tz: tzinfo, transitions: List[datetime]):
    transition_map = defaultdict(list)
    for trans in sorted(transitions):
        transition_map[TimezoneTransitionInfo.from_transition_dt(trans.astimezone(tz))].append(trans)
    vtz = Timezone(str(tz))
    for tti, tti_transitions in transition_map.items():
        vtz.observances.extend(
            tti.to_vtimezone_observance(rrule)
            for rrule in convert_rdates(tti_transitions)
        )
    vtz.observances.sort(key=lambda obs: obs.rrule[0])
    return vtz


def check_vtz(tz1, tz2, transitions):
    for trans in transitions:
        for td in [
            timedelta(days=-1),
            timedelta(hours=-1),
            timedelta(minutes=-1),
            timedelta(seconds=0),
            timedelta(minutes=1),
            timedelta(hours=1),
            timedelta(days=1)
        ]:
            t = trans + td
            t1 = export_tzinfo(t.astimezone(tz1))
            t2 = export_tzinfo(t.astimezone(tz2))
            print(t1 == t2, t1, t2)


def export_tzinfo(dt: datetime):
    return dt.replace(tzinfo=None), dt.replace(tzinfo=None).timestamp(), dt.fold, dt.tzname(), dt.utcoffset(), dt.dst()


berlin = ZoneInfo("Europe/Berlin")
transitions = [datetime.fromtimestamp(trans, timezone.utc) for trans in berlin._trans_utc]
berlin_vtz = convert_timezone(berlin, transitions)
pprint((berlin_vtz))
check_vtz(berlin, berlin_vtz, transitions)
