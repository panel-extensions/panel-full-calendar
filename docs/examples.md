# Examples

```{.python pycafe-embed pycafe-embed-style="border: 1px solid #e6e6e6; border-radius: 8px;" pycafe-embed-width="100%" pycafe-embed-height="400px" pycafe-embed-scale="1.0"}
import datetime
import panel as pn
from panel_full_calendar import Calendar

pn.extension()

def update_date_clicked(event_dict):
    date_clicked.object = f"Date clicked: {event['startStr']}"

def update_event_title(event_dict):
    event = CalendarEvent.from_dict(event_dict, calendar)
    if "❌" in event.title:
        title = event.title.replace("❌", "✅")
    else:
        title = event.title.replace("✅", "❌")
    event.set_props(title=title)

now = datetime.datetime.now()
date_clicked = pn.pane.Markdown()
calendar = Calendar(
    value=[
        {"title": "❌ Toggle me!", "start": now},
    ],
    selectable=True,
    select_callback=update_date_clicked,
    event_click_callback=update_event_title,
    sizing_mode="stretch_width",
)
pn.Column(date_clicked, calendar).servable()
```

## Basics

```python
calendar = Calendar(sizing_mode="stretch_width")
calendar
```

The current date that the calendar initially displays can be set with `current_date`, but **only upon instantiation**.

```python
calendar = Calendar(current_date="2008-08-08", sizing_mode="stretch_width")
calendar
```

Afterwards, you can use the `go_to_date` method to programmatically change the date.

Dates can be ISO8601 strings, e.g. `2018-06-01T12:30:00`, millisecond time, e.g. `1537302134028` (Tue Sep 18 2018 16:22:14 GMT-0400), or datetime objects, e.g. `datetime.datetime(2028, 08, 18)`. See [FullCalendar date parsing docs](https://fullcalendar.io/docs/date-parsing) for more info.

```python
now = datetime.datetime.now()
calendar.go_to_date(now)
```

The calendar can be limited to a specific date range by setting `valid_range`.

```python
calendar.valid_range = {
    "start": now - datetime.timedelta(days=2),
    "end": now + datetime.timedelta(days=2),
}
```

## Events

In addition to setting `value` directly, events can be managed through the methods `add_event`, `add_events`, `remove_event`, `update_event`, `get_event_in_view`, and `clear_events`. These methods allow for flexible event handling by normalizing dates internally and ensuring precise event matching.

### Add Events

An individual event can be added using the `add_event` method.

```python
calendar.add_event(
    title="Bi-Weekly Event",
    startRecur="2024-10-22",
    daysOfWeek=[2],  # 2 represents Tuesday (0 = Sunday, 1 = Monday, ...)
    startTime="06:30:00",
    endTime="07:30:00",
    duration="01:00",
)
```

### Add Multiple Events

Multiple events can be added simultaneously using the `add_events` method.

```python
calendar.add_events([
    {
        "title": "Bi-Weekly Event",
        "startRecur": "2024-10-22",
        "daysOfWeek": [2],  # 2 represents Tuesday (0 = Sunday, 1 = Monday, ...)
        "startTime": "06:30:00",
        "endTime": "07:30:00",
        "duration": "01:00",
    },
    {
        "title": "Monthly Meeting",
        "start": "2024-11-01T10:00:00",
        "end": "2024-11-01T11:00:00",
    }
])
```

The `add_events` method accepts a list of dictionaries, each representing an event. Event keys can be provided in either `snake_case` or `camelCase`, with automatic conversion available if `event_keys_auto_camel_case=True`.

### Retrieve Events

Events can be retrieved using the `get_event_in_view` method. This method allows searching for events by start date and title, with optional precise time matching. Retrieved events are returned as `CalendarEvent` objects, which provide a convenient way to interact with individual events in the calendar.

```python
from datetime import datetime

try:
    event = calendar.get_event_in_view(
        start=datetime(2024, 10, 22),
        title="Bi-Weekly Event",
        match_by_time=False,
    )
    print("Event found:", event)
    # Modifying the retrieved event
    event.set_start("2024-10-22T12:00:00")
    event.set_end("2024-10-22T13:00:00")
except ValueError as e:
    print(e)
```

Events retrieved using `get_event_in_view` return `CalendarEvent` objects, allowing for easy modification and interaction with the calendar.

```python
calendar_event.set_props(title="New title")
calendar_event.set_start("2024-11-10T13:00:00")
calendar_event.set_end("2024-11-10T16:00:00")
calendar_event.remove()
```

### Clear Events

All events can be cleared from the calendar using the `clear_events` method.

```python
calendar.clear_events()
```

## Views

The initial view can be set with `current_view`, but **only during instantiation**.

```python
calendar = Calendar(current_view="timeGridDay", sizing_mode="stretch_width")
calendar
```

After, it can only be programmatically changed with `change_view`, or through user interaction on the header/footer toolbar.

```python
calendar.change_view("timeGridWeek")
```

The header/footer toolbar's can be customized to subset the available views users can toggle. This also reduces the number of plugins loaded, which can benefit rendering speed.

Please see the [FullCalendar headerToolbar docs](https://fullcalendar.io/docs/headerToolbar) for full customizability.

```python
calendar = Calendar(
    header_toolbar={
        "left": "title",
        "center": "",
        "right": "prev,next today",
    },
    sizing_mode="stretch_width",
)
calendar
```

## Interaction

The calendars' events can be dragged and dropped with `editable=True`.

```python
now = datetime.datetime.now()
calendar = Calendar(
    value=[
        {"title": "Drag and drop me to reschedule!", "start": now},
    ],
    editable=True,
    sizing_mode="stretch_width",
)
calendar
```

It's possible to watch for dropped events by setting `event_drop_callback`, resulting in output like:

```python
{
    "oldEvent": {
        "allDay": False,
        "title": "Drag and drop me to reschedule!",
        "start": "2024-10-24T16:12:41.154-07:00",
    },
    "event": {
        "allDay": False,
        "title": "Drag and drop me to reschedule!",
        "start": "2024-10-17T16:12:41.154-07:00",
    },
    "relatedEvents": [],
    "el": {...},
    "delta": {"years": 0, "months": 0, "days": -7, "milliseconds": 0},
    "jsEvent": {"isTrusted": True},
    "view": {
        "type": "dayGridMonth",
        "dateEnv": {...},
    },
}
```

```python
calendar.event_drop_callback = lambda event: print(event)
```

Dates can also be selected by setting `selectable=True` and selections can also be watched with `select_callback`, which you can use to update other Panel components.

```python
def update_date_clicked(event):
    date_clicked.object = f"Date clicked: {event['startStr']}"

date_clicked = pn.pane.Markdown()
calendar = Calendar(
    selectable=True,
    select_callback=update_date_clicked,
    sizing_mode="stretch_width",
)
pn.Column(date_clicked, calendar)
```

## Additional Resources

FullCalendar is full of features and options, so be sure to check out the full list of options in the [FullCalendar docs](https://fullcalendar.io/docs).

Note, not all functionality has been ported over--if there's one you want, please submit a [GitHub issue](https://github.com/panel-extensions/panel_full_calendar/issues/new/choose).
