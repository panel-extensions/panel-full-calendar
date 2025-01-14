"""Implements FullCalendar within Panel."""

import datetime
import json
from copy import deepcopy
from pathlib import Path
from typing import Literal

import pandas as pd
import param
from panel.custom import JSComponent

from .utils import to_camel_case
from .utils import to_camel_case_keys

THIS_DIR = Path(__file__).parent
MODELS_DIR = THIS_DIR / "models"
VIEW_DEFAULT_INCREMENTS = {
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

    business_hours = param.Dict(default={}, doc="Emphasizes certain time slots on the calendar.")

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

    date_increment = param.String(
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

    event_background_color = param.Color(
        default=None,
        doc="Sets the background color for all events on the calendar.",
    )

    event_border_color = param.Color(
        default=None,
        doc="Sets the border color for all events on the calendar.",
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

    _syncing = param.Boolean(default=False)

    _rename = {
        # callbacks are handled in _handle_msg getattr
        "current_date_callback": None,
        "current_view_callback": None,
        "date_click_callback": None,
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
        if self.event_keys_auto_camel_case:
            self.value = [to_camel_case_keys(event) for event in self.value]
        self.param.watch(
            self._update_options,
            [
                "all_day_maintain_duration",
                "aspect_ratio",
                "business_hours",
                "button_icons",
                "button_text",
                "date_alignment",
                "date_increment",
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

    def increment_date(self, increment: str | datetime.timedelta | int | dict | None = None) -> None:
        """
        Increment the current date by a specific amount.

        Args:
            increment: The amount to increment the current date by.
                Supports a string in the format hh:mm:ss.sss, hh:mm:sss or hh:mm, an int in milliseconds,
                datetime.timedelta objects, or a dict with any of the following keys:
                    year, years, month, months, day, days, minute, minutes, second,
                    seconds, millisecond, milliseconds, ms.
                If not provided, the date_increment parameter will be used.
                If date_increment is not set, the default increment for the current view will be used:
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
        if increment is None and self.date_increment is None:
            increment = VIEW_DEFAULT_INCREMENTS[self.current_view]
        self._send_msg({"type": "incrementDate", "increment": increment})

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
            start: The start date of the event.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
            end: The end date of the event.
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

    def remove_event(
        self,
        start: str | datetime.datetime | datetime.date | int,
        title: str,
        end: str | datetime.datetime | datetime.date | int | None = None,
        all_day: bool | None = None,
        **kwargs,
    ) -> None:
        """
        Remove an event from the calendar.

        Args:
            start: The start date of the event.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
            title: The title of the event.
            end: The end date of the event.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
                If None, the event will be all-day.
            all_day: Whether the event is an all-day event.
            **kwargs: CamelCase properties to match on the event.
        """
        all_day = kwargs.pop("allDay", all_day)

        norm_start = pd.to_datetime(start)
        norm_end = pd.to_datetime(end) if end is not None else None

        events = self.value.copy()
        for i, event in enumerate(self.value):
            event_start = pd.to_datetime(event["start"])
            if event_start == norm_start and event["title"] == title:
                if end is None and all_day is None:
                    del events[i]
                elif end is not None and all_day is not None:
                    event_end = pd.to_datetime(event["end"])
                    if event_end == norm_end and event.get("allDay") == all_day:
                        del events[i]
                elif end is not None:
                    event_end = pd.to_datetime(event["end"])
                    if event_end == norm_end:
                        del events[i]
                elif all_day and not event.get("end"):
                    del events[i]
                self.value = events
                return
        raise ValueError(f"Event {title!r} not found at {norm_start}.")

    def update_event(
        self,
        start: str | datetime.datetime | datetime.date | int,
        title: str,
        updates: dict,
        end: str | datetime.datetime | datetime.date | int | None = None,
        all_day: bool | None = None,
        **kwargs,
    ) -> None:
        """
        Update an event on the calendar by looking up its start date and title.

        Args:
            start: The start date of the event.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
            title: The title of the event to update.
            updates: Updated properties to set on the event.
            end: The end date of the event to update.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
                If None, the event is assumed to be all-day.
            all_day: Whether the event to update is an all-day event.
            **kwargs: CamelCase properties to match on the event.
        """
        if self.event_keys_auto_camel_case:
            updates = to_camel_case_keys(updates)
        all_day = kwargs.pop("allDay", all_day)
        norm_start = pd.to_datetime(start)
        norm_end = pd.to_datetime(end) if end is not None else None
        events = deepcopy(self.value)
        for i, event in enumerate(self.value):
            event_start = pd.to_datetime(event["start"])
            if event_start == norm_start and event["title"] == title:
                if end is None and all_day is None:
                    events[i].update(updates)
                elif end is not None and all_day is not None:
                    event_end = pd.to_datetime(event["end"])
                    if event_end == norm_end and event.get("allDay") == all_day:
                        events[i].update(updates)
                elif end is not None:
                    event_end = pd.to_datetime(event["end"])
                    if event_end == norm_end:
                        events[i].update(updates)
                elif all_day and not event.get("end"):
                    events[i].update(updates)
                self.value = events
                return
        raise ValueError(f"Event {title!r} not found at {norm_start}.")

    def filter_events(
        self,
        start: str | datetime.datetime | datetime.date | int,
        end: str | datetime.datetime | datetime.date | int | None = None,
        all_day: bool | None = None,
        **kwargs,
    ) -> list[dict]:
        """
        Filter events on the calendar by start date and optionally end date and all-day status.

        Args:
            start: The start date of the events to filter.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
            end: The end date of the events to filter.
                Supports ISO 8601 date strings, datetime/date objects, and int in milliseconds.
            all_day: Whether the events to filter are all-day events; if None, will
                return events that are and are not all-day.
            **kwargs: CamelCase properties to match on the events.

        Returns:
            list[dict]: A list of events that match the filter criteria.
        """
        all_day = kwargs.pop("allDay", all_day)

        # Normalize input dates to pandas Timestamp for consistent comparison
        filter_start = pd.to_datetime(start)
        filter_end = pd.to_datetime(end) if end is not None else None

        filtered_events = []

        for event in self.value:
            event_start = pd.to_datetime(event["start"])
            event_end = pd.to_datetime(event.get("end")) if event.get("end") is not None else None

            if event_start != filter_start:
                continue

            if filter_end is not None:
                if event_end is None or event_end != filter_end:
                    continue

            # Check all-day status if specified
            if all_day is not None:
                event_all_day = event.get("allDay", False)
                if event_all_day != all_day:
                    continue

            # If we get here, the event matches all specified criteria
            filtered_events.append(event)
        return filtered_events

    def clear_events(self) -> None:
        """Clear all events from the calendar."""
        self.value = []

    def _handle_msg(self, msg):
        if "events" in msg:
            with param.edit_constant(self):
                self.events = json.loads(msg["events"])
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
            callback = getattr(self, callback_name, None)
            if callback:
                callback(json.loads(msg[key]))

    @param.depends("value", watch=True, on_init=True)
    def _update_events(self):
        self._send_msg({"type": "updateEvents", "value": self.value})

    def _update_options(self, *events):
        updates = [
            {
                "key": ("events" if to_camel_case(event.name) == "value" else to_camel_case(event.name)),
                "value": event.new,
            }
            for event in events
        ]
        self._send_msg({"type": "updateOptions", "updates": updates})
