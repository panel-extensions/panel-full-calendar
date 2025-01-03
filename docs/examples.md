# Examples

```{.python pycafe-embed pycafe-embed-style="border: 1px solid #e6e6e6; border-radius: 8px;" pycafe-embed-width="100%" pycafe-embed-height="400px" pycafe-embed-scale="1.0"}
import panel as pn

from panel_full_calendar import Calendar

pn.extension()

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

Events can be added through `value` as a list of dictionaries.

```python
calendar.value = [
    {
        "start": now,
        "end": now + datetime.timedelta(minutes=30),
        "title": "Calendar Tutorial",
    },
    {
        "start": now,
        "allDay": True,
        "title": "Enjoying Panel",
    },
]
```

Alternatively, an event can be added through the method `add_event`. Valid event keys can be found on the [FullCalendar Event Parsing docs](https://fullcalendar.io/docs/event-parsing).

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

Note, the keys can be defined in `snake_case` or `camelCase` as long as `event_keys_auto_camel_case=True`, which pre-processes the keys into `camelCase` internally.

The following is equivalent to above.

```python
calendar.add_event(
    title="Bi-Weekly Event",
    start_recur="2024-10-22",
    days_of_week=[2],
    start_time="06:30:00",
    end_time="07:30:00",
    duration="01:00",
)
```

If there are many events or if the events are large, use `camelCase` and set `event_keys_auto_camel_case=False` to speed up rendering.

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
