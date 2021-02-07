# tzdb.txt

The rule definition in the Olson database. A tool called `zic` parses these rules, instantiates all individual transitions in a given timeframe and then stores these instances in a binary format that ships with most UNIXes and the python `zoneinfo` module. All clients just parse those binary files with the specific transition dates, which do not contain any 'meta' information about the rules behind the transition dates.

# zoneinfo.txt

The data I was able to extract from `zoneinfo` instances, as long as the plain-python implementation was used instead of the C-module.

# apple-ccs-pycalendar-zonal.ics

Generated by [Cyrus Daboo's / Apple's ccs-pycalendar tzconvert.py](https://github.com/apple/ccs-pycalendar/blob/master/src/zonal/tzconvert.py).
The database directory of ics vTimezone files is used like this:
```python
from pycalendar.icalendar.calendar import Calendar
from pycalendar.timezonedb import TimezoneDatabase
cal = TimezoneDatabase.getTimezoneInCalendar("Europe/Berlin")
with open("apple-ccs-pycalendar-none.ics", "wt") as f:
	cal.generate(f, includeTimezones=Calendar.NO_TIMEZONES)
with open("apple-ccs-pycalendar-all.ics", "wt") as f:
	cal.generate(f, includeTimezones=Calendar.ALL_TIMEZONES)
```

# python-icalendar(-khal).ics

The python icalendar module seems to be [unable](https://stackoverflow.com/questions/13338391/) to generate vTimezones,
but the khal calendar cli seems to add a [converter from pytz](https://github.com/pimutils/khal/blob/master/khal/khalendar/event.py#L762).

```python
from icalendar import Calendar, Event
from datetime import datetime
import pytz
cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
event = Event()
event.add('summary', 'Test')
event.add('dtstart', datetime(2021, 2, 7, 12, 0, 0, tzinfo=pytz.timezone("Europe/Berlin")))
event.add('dtend',   datetime(2021, 2, 7, 13, 0, 0, tzinfo=pytz.timezone("Europe/Berlin")))
event.add('dtstamp', datetime(2021, 2, 7, 11, 0, 0, tzinfo=pytz.utc))
cal.add_component(event)
with open("python-icalendar.ics", "wb") as f:
	f.write(cal.to_ical())

from khal.khalendar.event import create_timezone
cal.add_component(create_timezone(pytz.timezone("Europe/Berlin")))
with open("python-icalendar-khal.ics", "wb") as f:
	f.write(cal.to_ical())
```

# python-vobject.ics

```python
import vobject
import pytz
cal = vobject.iCalendar()
vevent = cal.add('vevent')
vevent.add('summary').value = "Test"
vevent.add('dtstart').value = datetime(2021, 2, 7, 12, 0, 0, tzinfo=pytz.timezone("Europe/Berlin"))
vevent.add('dtend').value =   datetime(2021, 2, 7, 13, 0, 0, tzinfo=pytz.timezone("Europe/Berlin"))
vevent.add('dtstamp').value = datetime(2021, 2, 7, 11, 0, 0, tzinfo=pytz.utc)
with open("python-vobject.ics", "wt") as f:
	f.write(cal.serialize())
```

# tzurl(-outlook).ics

[tzurl](http://tzurl.sgp1.cdn.digitaloceanspaces.com/index.html) is hosting two versions of files generated by a slightly modified vzic.
Their [python version](https://github.com/benfortuna/tzurl/commit/31bfdfa1ad3ce79b132f9bf1c6137cb7d668f7e3) of the tools seems to be non-functional.

# vzic.ics

The vzic generated files included in ics_vtimezones.
