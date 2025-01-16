"""Implements FullCalendar within Panel."""

import asyncio
import datetime
import json
from pathlib import Path
from typing import Literal

import param
from panel.custom import JSComponent

from .utils import normalize_datetimes
from .utils import to_camel_case
from .utils import to_camel_case_keys

THIS_DIR = Path(__file__).parent
MODELS_DIR = THIS_DIR / "models"
VIEW_DEFAULT_deltaS = {
    "dayGridMonth": {"days": 1},
    "dayGridWeek": {"weeks": 1},
    "dayGridDay": {"days": 1},
    "timeGridWeek": {"weeks": 1},
    "timeGridDay": {"days": 1},
    "listWeek": {"weeks": 1},
    "listMonth": {"months": 1},
    "listYear": {"years": 1},
    "multiMonthYear": {"years": 1},
}


class Calendar(JSComponent):
    """
    The Calendar widget is a wrapper around the FullCalendar library.

    See https://fullcalendar.io/docs for more information on the parameters.
    """

    all_day_maintain_duration = param.Boolean(
        default=False,
        doc="Determines how an event's duration should be mutated when it is dragged from a timed section to an all-day section and vice versa.",
    )

    aspect_ratio = param.Number(default=None, doc="Sets the width-to-height aspect ratio of the calendar.")

    business_hours = param.Dict(default=None, doc="Emphasizes certain time slots on the calendar.")

    button_icons = param.Dict(
        default={},
        doc="Icons that will be displayed in buttons of the header/footer toolbar.",
    )

    button_text = param.Dict(
        default={},
        doc="Text that will be displayed on buttons of the header/footer toolbar.",
    )

    current_date = param.String(
        default=None,
        constant=True,
        doc="The onload or current date of the calendar view. Use go_to_date() to change the date.",
    )

    current_date_callback = param.Callable(
        default=None,
        doc="A callback that will be called when the current date changes.",
    )

    current_view = param.Selector(
        default="dayGridMonth",
        objects=[
            "dayGridMonth",
            "dayGridWeek",
            "dayGridDay",
            "timeGridWeek",
            "timeGridDay",
            "listWeek",
            "listMonth",
            "listYear",
            "multiMonthYear",
        ],
        constant=True,
        doc="The onload or current view of the calendar. Use change_view() to change the view.",
    )

    current_view_callback = param.Callable(
        default=None,
        doc="A callback that will be called when the current view changes.",
    )

    date_alignment = param.String(default=None, doc="Determines how certain views should be initially aligned.")

    date_click_callback = param.Callable(
        default=None,
        doc="A callback that will be called when a date is clicked.",
    )

    date_delta = param.String(
        default=None,
        doc="The duration to move forward/backward when prev/next is clicked.",
    )

    day_max_event_rows = param.Integer(
        default=False,
        doc=(
            "In dayGrid view, the max number of stacked event levels within a given day. "
            "This includes the +more link if present. The rest will show up in a popover."
        ),
    )

    day_max_events = param.Integer(
        default=None,
        doc=("In dayGrid view, the max number of events within a given day, not counting the +more link. " "The rest will show up in a popover."),
    )

    day_popover_format = param.Dict(
        default=None,
        doc="Determines the date format of title of the popover created by the moreLinkClick option.",
    )

    display_event_end = param.Boolean(
        default=None,
        doc="Whether or not to display an event's end time.",
    )

    display_event_time = param.Boolean(
        default=True,
        doc="Whether or not to display the text for an event's date/time.",
    )

    drag_revert_duration = param.Integer(
        default=500,
        doc="Time it takes for an event to revert to its original position after an unsuccessful drag.",
    )

    drag_scroll = param.Boolean(
        default=True,
        doc="Whether to automatically scroll the scroll-containers during event drag-and-drop and date selecting.",
    )

    editable = param.Boolean(
        default=False,
        doc="Determines whether the events on the calendar can be modified.",
    )

    events_in_view = param.List(
        default=[],
        doc="List of events that are currently in view on the calendar.",
        constant=True,
    )

    event_background_color = param.Color(
        default=None,
        doc="Sets the background color for all events on the calendar.",
    )

    event_border_color = param.Color(
        default=None,
        doc="Sets the border color for all events on the calendar.",
    )

    event_change_callback = param.Callable(
        default=None,
        doc="A callback that will be called when an event is changed.",
    )

    event_color = param.Color(
        default=None,
        doc="Sets the background and border colors for all events on the calendar.",
    )

    event_click_callback = param.Callable(
        default=None,
        doc="A callback that will be called when an event is clicked.",
    )

    event_display = param.String(
        default="auto",
        doc="Controls which preset rendering style events use.",
    )

    event_drag_min_distance = param.Integer(
        default=5,
        doc="How many pixels the user's mouse/touch must move before an event drag activates.",
    )

    event_drag_start_callback = param.Callable(
        default=None,
        doc="Triggered when event dragging begins.",
    )

    event_drag_stop_callback = param.Callable(
        default=None,
        doc="Triggered when event dragging stops.",
    )

    event_drop_callback = param.Callable(
        default=None,
        doc="Triggered when dragging stops and the event has moved to a different day/time.",
    )

    event_duration_editable = param.Boolean(
        default=True,
        doc="Allow events' durations to be editable through resizing.",
    )

    event_keys_auto_camel_case = param.Boolean(
        default=True,
        doc=(
            "Whether to automatically convert value and event keys to camelCase for convenience. "
            "However, this can slow down the widget if there are many events or if the events are large."
        ),
    )

    event_keys_auto_snake_case = param.Boolean(
        default=True,
        doc=(
            "Whether to automatically convert value and event keys to snake_case for convenience. "
            "However, this can slow down the widget if there are many events or if the events are large."
        ),
    )

    event_max_stack = param.Integer(
        default=None,
        doc="For timeline view, the maximum number of events that stack top-to-bottom. For timeGrid view, the maximum number of events that stack left-to-right.",
    )

    event_order = param.String(
        default="start,-duration,title,allDay",
        doc="Determines the ordering events within the same day.",
    )

    event_order_strict = param.Boolean(
        default=False,
        doc="Ensures the eventOrder setting is strictly followed.",
    )

    event_remove_callback = param.Callable(
        default=None,
        doc="Triggered when an event is removed.",
    )

    event_resize_callback = param.Callable(
        default=None,
        doc="Triggered when resizing stops and the event has changed in duration.",
    )

    event_resize_start_callback = param.Callable(
        default=None,
        doc="Triggered when event resizing begins.",
    )

    event_resize_stop_callback = param.Callable(
        default=None,
        doc="Triggered when event resizing stops.",
    )

    event_resizable_from_start = param.Boolean(
        default=True,
        doc="Whether the user can resize an event from its starting edge.",
    )

    event_start_editable = param.Boolean(
        default=True,
        doc="Allow events' start times to be editable through dragging.",
    )

    event_text_color = param.Color(
        default=None,
        doc="Sets the text color for all events on the calendar.",
    )

    event_time_format = param.Dict(
        default=None,
        doc="Determines the time-text that will be displayed on each event.",
    )

    expand_rows = param.Boolean(
        default=False,
        doc="If the rows of a given view don't take up the entire height, they will expand to fit.",
    )

    footer_toolbar = param.Dict(default={}, doc="Defines the buttons and title at the bottom of the calendar.")

    handle_window_resize = param.Boolean(
        default=True,
        doc="Whether to automatically resize the calendar when the browser window resizes.",
    )

    header_toolbar = param.Dict(
        default={
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
        doc="Defines the buttons and title at the top of the calendar.",
    )

    more_link_click = param.String(
        default="popover",
        doc='Determines the action taken when the user clicks on a "more" link created by the dayMaxEventRows or dayMaxEvents options.',
    )

    multi_month_max_columns = param.Integer(
        default=1,
        doc="Determines the maximum number of columns in the multi-month view.",
    )

    nav_links = param.Boolean(
        default=True,
        doc="Turns various datetime text into clickable links that the user can use for navigation.",
    )

    next_day_threshold = param.String(
        default="00:00:00",
        doc="When an event's end time spans into another day, the minimum time it must be in order for it to render as if it were on that day.",
    )

    now_indicator = param.Boolean(default=True, doc="Whether to display an indicator for the current time.")

    progressive_event_rendering = param.Boolean(
        default=False,
        doc="When to render multiple asynchronous event sources in an individual or batched manner.",
    )

    selectable = param.Boolean(
        default=False,
        doc="Allows a user to highlight multiple days or timeslots by clicking and dragging.",
    )

    select_callback = param.Callable(
        default=None,
        doc="A callback that will be called when a selection is made.",
    )

    select_mirror = param.Boolean(
        default=False,
        doc="Whether to draw a 'placeholder' event while the user is dragging.",
    )

    unselect_auto = param.Boolean(
        default=True,
        doc="Whether clicking elsewhere on the page will cause the current selection to be cleared.",
    )

    unselect_cancel = param.String(
        default=None,
        doc="A way to specify elements that will ignore the unselectAuto option.",
    )

    select_allow = param.Callable(
        default=None,
        doc="Exact programmatic control over where the user can select.",
    )

    select_min_distance = param.Integer(
        default=0,
        doc="The minimum distance the user's mouse must travel after a mousedown, before a selection is allowed.",
    )

    show_non_current_dates = param.Boolean(
        default=False,
        doc="Whether to display dates in the current view that don't belong to the current month.",
    )

    snap_duration = param.String(
        default=None,
        doc="The time interval at which a dragged event will snap to the time axis. Also affects the granularity at which selections can be made.",
    )

    sticky_footer_scrollbar = param.Boolean(
        default=True,
        doc="Whether to fix the view's horizontal scrollbar to the bottom of the viewport while scrolling.",
    )

    sticky_header_dates = param.String(
        default=None,
        doc="Whether to fix the date-headers at the top of the calendar to the viewport while scrolling.",
    )

    time_zone = param.String(
        default="local",
        doc="Determines the time zone the calendar will use to display dates.",
    )

    title_format = param.Dict(
        default=None,
        doc="Determines the text that will be displayed in the header toolbar's title.",
    )

    title_range_separator = param.String(
        default=" to ",
        doc="Determines the separator text when formatting the date range in the toolbar title.",
    )

    unselect_callback = param.Callable(
        default=None,
        doc="A callback that will be called when a selection is cleared.",
    )

    valid_range = param.Dict(
        default=None,
        doc=("Dates outside of the valid range will be grayed-out and inaccessible. " "Can have `start` and `end` keys, but both do not need to be together."),
    )

    value = param.List(default=[], item_type=dict, doc="List of events to display on the calendar.")

    views = param.Dict(
        default={},
        doc=("Options to pass to only to specific calendar views. " "Provide separate options objects within the views option, keyed by the name of your view."),
    )

    window_resize_delay = param.Integer(
        default=100,
        doc="The time the calendar will wait to adjust its size after a window resize occurs, in milliseconds.",
    )

    _esm = MODELS_DIR / "fullcalendar.js"

    _rename = {
        # callbacks are handled in _handle_msg getattr
        "current_date_callback": None,
        "current_view_callback": None,
        "date_click_callback": None,
        "event_change_callback": None,
        "event_click_callback": None,
        "event_drag_start_callback": None,
        "event_drag_stop_callback": None,
        "event_drop_callback": None,
        "event_remove_callback": None,
        "event_resize_callback": None,
        "event_resize_start_callback": None,
        "event_resize_stop_callback": None,
        "select_callback": None,
        "unselect_callback": None,
        "events_in_view": None,
    }

    _importmap = {
        "imports": {
            "@fullcalendar/core": "https://cdn.skypack.dev/@fullcalendar/core@6.1.15",
            "@fullcalendar/daygrid": "https://cdn.skypack.dev/@fullcalendar/daygrid@6.1.15",
            "@fullcalendar/timegrid": "https://cdn.skypack.dev/@fullcalendar/timegrid@6.1.15",
            "@fullcalendar/list": "https://cdn.skypack.dev/@fullcalendar/list@6.1.15",
            "@fullcalendar/multimonth": "https://cdn.skypack.dev/@fullcalendar/multimonth@6.1.15",
            "@fullcalendar/interaction": "https://cdn.skypack.dev/@fullcalendar/interaction@6.1.15",
        }
    }

    def __init__(self, **params):
        """Create a new Calendar widget."""
        super().__init__(**params)
        self._assign_id_to_events()

        self._buffer = []
        self.param.watch(
            self._update_options,
            [
                "all_day_maintain_duration",
                "aspect_ratio",
                "business_hours",
                "button_icons",
                "button_text",
                "date_alignment",
                "date_delta",
                "day_max_event_rows",
                "day_max_events",
                "day_popover_format",
                "display_event_end",
                "display_event_time",
                "drag_revert_duration",
                "drag_scroll",
                "editable",
                "event_background_color",
                "event_border_color",
                "event_color",
                "event_display",
                "event_drag_min_distance",
                "event_duration_editable",
                "event_max_stack",
                "event_order",
                "event_order_strict",
                "event_resizable_from_start",
                "event_start_editable",
                "event_text_color",
                "event_time_format",
                "expand_rows",
                "footer_toolbar",
                "handle_window_resize",
                "header_toolbar",
                "more_link_click",
                "multi_month_max_columns",
                "nav_links",
                "next_day_threshold",
                "now_indicator",
                "progressive_event_rendering",
                "selectable",
                "select_mirror",
                "unselect_auto",
                "unselect_cancel",
                "select_allow",
                "select_min_distance",
                "show_non_current_dates",
                "snap_duration",
                "sticky_footer_scrollbar",
                "sticky_header_dates",
                "time_zone",
                "title_format",
                "title_range_separator",
                "valid_range",
                "value",
                "window_resize_delay",
            ],
        )

    def click_next(self) -> None:
        """Click the next button through the calendar's UI."""
        self._send_msg({"type": "next"})

    def click_prev(self) -> None:
        """Click the previous button through the calendar's UI."""
        self._send_msg({"type": "prev"})

    def click_prev_year(self) -> None:
        """Click the previous year button through the calendar's UI."""
        self._send_msg({"type": "prevYear"})

    def click_next_year(self) -> None:
        """Click the next year button through the calendar's UI."""
        self._send_msg({"type": "nextYear"})

    def click_today(self) -> None:
        """Click the today button through the calendar's UI."""
        self._send_msg({"type": "today"})

    def change_view(
        self,
        view: str,
        date: str | datetime.datetime | datetime.date | int | None = None,
    ) -> None:
        """
        Change the current view of the calendar, and optionally go to a specific date.

        Args:
            view: The view to change to.
                Options: "dayGridMonth", "dayGridWeek", "dayGridDay", "timeGridWeek", "timeGridDay",
                "listWeek", "listMonth", "listYear", "multiMonthYear".
            date: The date to go to after changing the view; if None, the current date will be used.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
        """
        self._send_msg({"type": "changeView", "view": view, "date": date})

    def go_to_date(self, date: str | datetime.datetime | datetime.date | int) -> None:
        """
        Go to a specific date on the calendar.

        Args:
            date: The date to go to.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
        """
        self._send_msg({"type": "gotoDate", "date": date})

    def delta_date(self, delta: str | datetime.timedelta | int | dict | None = None) -> None:
        """
        delta the current date by a specific amount.

        Args:
            delta: The amount to delta the current date by.
                Supports a string in the format hh:mm:ss.sss, hh:mm:sss or hh:mm, an int in milliseconds,
                datetime.timedelta objects, or a dict with any of the following keys:
                    year, years, month, months, day, days, minute, minutes, second,
                    seconds, millisecond, milliseconds, ms.
                If not provided, the date_delta parameter will be used.
                If date_delta is not set, the default delta for the current view will be used:
                    dayGridMonth: {"days": 1}
                    dayGridWeek: {"weeks": 1}
                    dayGridDay: {"days": 1}
                    timeGridWeek: {"weeks": 1}
                    timeGridDay: {"days": 1}
                    listWeek: {"weeks": 1}
                    listMonth: {"months": 1}
                    listYear: {"years": 1}
                    multiMonthYear: {"years": 1}
        """
        if delta is None and self.date_delta is None:
            delta = VIEW_DEFAULT_deltaS[self.current_view]
        self._send_msg({"type": "deltaDate", "delta": delta})

    def scroll_to_time(self, time: str | datetime.time | int) -> None:
        """
        Scroll the calendar to a specific time.

        Args:
            time: The time to scroll to.
                Supports ISO 8601 time strings, datetime.time objects, and int in milliseconds.
        """
        self._send_msg({"type": "scrollToTime", "time": time})

    def add_event(
        self,
        start: str | datetime.datetime | datetime.date | int | None = None,
        end: str | datetime.datetime | datetime.date | int | None = None,
        title: str | None = "(no title)",
        all_day: bool | None = None,
        display: Literal["background", "inverse-background"] | None = None,
        **kwargs,
    ) -> None:
        """
        Add an event to the calendar.

        Args:
            start: The start of the event.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
            end: The end of the event.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
                If None, the event will be all-day.
            title: The title of the event.
            all_day: Whether the event is an all-day event.
            display: How the event should be displayed. Options: "background", "inverse-background".
            **kwargs: Additional properties to set on the event. Takes precedence over other arguments.
        """
        if self.event_keys_auto_camel_case:
            kwargs = to_camel_case_keys(kwargs)

        event = {}
        if start is not None:
            event["start"] = start
        if end is not None:
            event["end"] = end
        if title is not None:
            event["title"] = title
        if all_day is not None:
            event["allDay"] = all_day
        if display is not None:
            event["display"] = display
        event.update(kwargs)
        self.value = self.value + [event]

    def add_events(self, events: list[dict]) -> None:
        """
        Add multiple events to the calendar.

        Args:
            events: A list of events to add to the calendar.
        """
        with param.parameterized.batch_call_watchers(self):
            for event in events:
                self.add_event(**event)

    def get_event_in_view(
        self,
        start: str | datetime.datetime | datetime.date | int,
        title: str,
        match_by_time: bool = False,
    ) -> "CalendarEvent":
        """
        Get an event from the calendar.

        Args:
            start: The start of the event.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
            title: The title of the event.
            match_by_time: Whether to match the start time exactly, or by date only.

        Returns:
            Event: The event with the given start and title.
        """
        for event in self.events_in_view:  # type: ignore
            norm_start, event_start = normalize_datetimes(start, event["start"])  # type: ignore
            if match_by_time:
                norm_start = norm_start.date()
                event_start = event_start.date()
            if norm_start != event_start or event["title"] != title:
                continue
            return CalendarEvent(
                id=event["id"],
                title=event["title"],
                start=event["start"],
                end=event.get("end"),
                all_day=event.get("allDay"),
                calendar=self,
            )
        raise ValueError(f"No event found with start {start} and title {title}.")

    def clear_events(self) -> None:
        """Clear all events from the calendar."""
        self.value = []

    def _handle_msg(self, msg):
        if "events_in_view" in msg:
            events = json.loads(msg["events_in_view"])
            with param.edit_constant(self):
                self.events_in_view = events
        elif "current_date" in msg:
            current_date_info = json.loads(msg["current_date"])
            with param.edit_constant(self):
                self.current_date = current_date_info["startStr"]
            if self.current_date_callback:
                self.current_date_callback(current_date_info)
        elif "current_view" in msg:
            current_view_info = json.loads(msg["current_view"])
            with param.edit_constant(self):
                self.current_view = current_view_info["view"]["type"]
            if self.current_view_callback:
                self.current_view_callback(current_view_info)
        else:
            key = list(msg.keys())[0]
            callback_name = f"{key}_callback"
            if hasattr(self, callback_name):
                info = json.loads(msg[key])
                if callback_name == "event_change_callback":
                    new_event = info["event"]
                    for value in self.value:
                        if value["id"] != new_event["id"]:
                            continue
                        value.update(new_event)
                        break
                    self.param.trigger("value")
                elif callback_name == "event_remove_callback":
                    removed_event = info["event"]
                    for value in self.value:
                        if value["id"] != removed_event["id"]:
                            continue
                        self.value.remove(value)
                        break
                    self.param.trigger("value")
                callback = getattr(self, callback_name)
                if callback:
                    callback(info)
            else:
                raise RuntimeError(f"Unhandled message: {msg}")

    def _update_options(self, *events):
        updates = [
            {
                "key": ("events" if to_camel_case(event.name) == "value" else to_camel_case(event.name)),
                "value": event.new,
            }
            for event in events
        ]
        self._send_msg({"type": "updateOptions", "updates": updates})

    def _assign_id_to_events(self):
        for event in self.value:
            event["id"] = event.get("id", str(id(event)))
            if self.event_keys_auto_camel_case:
                for key in list(event.keys()):
                    event[to_camel_case(key)] = event.pop(key)

    @param.depends("value", watch=True)
    async def _update_events_in_view(self):
        self._assign_id_to_events()
        await asyncio.sleep(0.001)  # needed to prevent race condition
        self._send_msg({"type": "updateEventsInView"})


class CalendarEvent(param.Parameterized):
    """A class representing an event on a Calendar."""

    id: str = param.String(default=None, doc="A unique identifier for the event.", constant=True)

    start = param.String(
        default=None,
        constant=True,
        doc="The start of the event. Supports ISO 8601 date strings. Use `set_start` to change.",
    )

    end = param.String(
        default=None,
        constant=True,
        doc="The end of the event. Supports ISO 8601 date strings. Use `set_end` to change.",
    )

    title = param.String(
        default="(no title)",
        constant=True,
        doc="The title of the event. Use `set_props` to change.",
    )

    all_day = param.Boolean(
        default=False,
        constant=True,
        doc="Whether the event is an all-day event. Use `set_props` to change.",
    )

    props = param.Dict(
        default={},
        constant=True,
        doc="Additional properties of the event. Use `set_props` to change.",
    )

    calendar = param.ClassSelector(
        class_=Calendar,
        constant=True,
        doc="The calendar that the event belongs to.",
    )

    def remove(self):
        """Remove the event from the calendar."""
        self.calendar._send_msg({"type": "removeEvent", "id": self.id})

    def set_props(self, **kwargs):
        """Modifies any of the non-date-related properties of the event."""
        updates = kwargs.copy()
        if self.calendar.event_keys_auto_camel_case:
            updates = to_camel_case_keys(kwargs)

        self.calendar._send_msg({"type": "setProp", "id": self.id, "updates": updates})
        with param.edit_constant(self):
            if "title" in kwargs:
                self.title = kwargs.pop("title")
            if "allDay" in kwargs:
                self.all_day = kwargs.pop("allDay")
            self.props.update(kwargs)

    def set_start(self, start: str | datetime.datetime | datetime.date | int):
        """Update the start of the event."""
        self.calendar._send_msg({"type": "setStart", "id": self.id, "updates": {"start": start}})
        with param.edit_constant(self):
            self.start = start

    def set_end(self, end: str | datetime.datetime | datetime.date | int):
        """Update the end of the event."""
        self.calendar._send_msg({"type": "setEnd", "id": self.id, "updates": {"end": end}})
        with param.edit_constant(self):
            self.end = end

    @classmethod
    def from_dict(cls, event_dict: dict, calendar: Calendar):
        """
        Create a CalendarEvent from a dictionary.

        Args:
            event_dict: A dictionary representing the event.
            calendar: The calendar that the event belongs to.

        Returns:
            CalendarEvent: The event.
        """
        return cls(
            id=event_dict.pop("id"),
            title=event_dict.pop("title", "(no title)"),
            start=event_dict.pop("start"),
            end=event_dict.pop("end", None),
            all_day=event_dict.pop("allDay", False),
            props=event_dict,
            calendar=calendar,
        )

    def __repr__(self):
        """Return a simplified string representation of the event."""
        attributes = [f"{p[0]}={p[1]}" for p in self.param.get_param_values() if p[1] is not None and p[0] not in ("calendar", "name")]
        attributes_str = ", ".join(attributes)
        return f"CalendarEvent({attributes_str})"
