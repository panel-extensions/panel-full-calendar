# ignore: D103
from datetime import date

import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel.tests.util import wait_until
from panel.widgets import TextInput

from panel_full_calendar import Calendar

pytestmark = pytest.mark.ui


Calendar.time_zone = "UTC"


def test_calendar_current_date_view(page):
    calendar = Calendar(current_date="2020-01-01", current_view="timeGridDay")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 1, 2020"
    assert page.locator(".fc-timeGridDay-button").first.get_attribute("class").split()[-1] == "fc-button-active"


def test_calendar_change_view(page):
    calendar = Calendar(current_date="2020-01-01")
    serve_component(page, calendar)

    assert calendar.current_view == "dayGridMonth"
    assert page.locator(".fc-dayGridMonth-button").first.get_attribute("class").split()[-1] == "fc-button-active"

    calendar.change_view("timeGridDay")
    assert page.locator(".fc-timeGridDay-button").first.get_attribute("class").split()[-1] == "fc-button-active"
    assert calendar.current_view == "timeGridDay"


def test_calendar_go_to_date(page):
    calendar = Calendar(current_date="2020-01-01", current_view="timeGridDay")
    serve_component(page, calendar)

    assert calendar.current_date == "2020-01-01"
    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 1, 2020"

    calendar.go_to_date("2021-01-01")
    assert calendar.current_date == "2020-01-01T00:00:00Z"
    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 1, 2021"


def test_calendar_click_next(page):
    calendar = Calendar(current_date="2020-01-01", current_view="dayGridMonth")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 2020"

    calendar.click_next()
    assert page.locator(".fc-toolbar-title").first.inner_text() == "February 2020"


def test_calendar_click_prev(page):
    calendar = Calendar(current_date="2020-01-01", current_view="dayGridMonth")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 2020"

    calendar.click_prev()
    assert page.locator(".fc-toolbar-title").first.inner_text() == "December 2019"


def test_calendar_click_next_year(page):
    calendar = Calendar(current_date="2020-01-01", current_view="dayGridMonth")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 2020"

    calendar.click_next_year()
    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 2021"


def test_calendar_click_prev_year(page):
    calendar = Calendar(current_date="2020-01-01", current_view="dayGridMonth")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 2020"

    calendar.click_prev_year()
    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 2019"


def test_calendar_click_today(page):
    calendar = Calendar(current_date="2020-01-01", current_view="dayGridMonth")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 2020"

    calendar.click_today()
    today = date.today().strftime("%B %Y")
    assert page.locator(".fc-toolbar-title").first.inner_text() == today


def test_calendar_scroll_to_time(page):
    calendar = Calendar(current_date="2020-01-01", current_view="timeGridDay")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 1, 2020"

    calendar.scroll_to_time("18:00:00")

    found_in_viewport = False
    for label in page.locator(".fc-timegrid-slot-label").all():
        if label.inner_text() == "6pm":
            box = label.bounding_box()
            if box and box["y"] >= 0:
                found_in_viewport = True
                break
    assert found_in_viewport


def test_calendar_update_options_day_max_events(page):
    calendar = Calendar(
        current_date="2020-01-01",
        value=[
            {"start": "2020-01-01", "end": "2020-01-02", "title": "Event 0"},
            {"start": "2020-01-01", "end": "2020-01-02", "title": "Event 1"},
        ],
    )
    serve_component(page, calendar)

    assert page.locator(".fc-event-title").last.inner_text() == "Event 1"

    calendar.day_max_events = 1
    assert page.locator(".fc-event-title").first.inner_text() == "Event 0"

    assert page.locator(".fc-daygrid-more-link").first.inner_text() == "+1 more"


def test_calendar_batch_update_options_title(page):
    calendar = Calendar(current_date="2020-01-01", current_view="timeGridWeek")
    serve_component(page, calendar)

    assert page.locator(".fc-toolbar-title").first.inner_text() == "Dec 29, 2019 to Jan 4, 2020"

    calendar.param.update(
        title_format={"month": "numeric", "year": "numeric"},
        title_range_separator=" - ",
    )
    assert page.locator(".fc-toolbar-title").first.inner_text() == "12/2019 - 1/2020"


def test_calendar_current_date_callback(page):
    def callback(event):
        text_input.value = event["startStr"]

    text_input = TextInput(name="Current Date")
    calendar = Calendar(
        current_date="2020-01-01",
        current_view="timeGridDay",
        current_date_callback=callback,
    )
    serve_component(page, calendar)

    assert calendar.current_date == "2020-01-01"
    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 1, 2020"

    calendar.go_to_date("2021-01-01")
    assert page.locator(".fc-toolbar-title").first.inner_text() == "January 1, 2021"
    assert calendar.current_date == "2021-01-01T00:00:00Z"
    assert text_input.value == "2021-01-01T00:00:00Z"


def test_calendar_current_view_callback(page):
    def callback(event):
        text_input.value = event["view"]["type"]

    text_input = TextInput(name="Current View")
    calendar = Calendar(current_view="timeGridDay", current_view_callback=callback)
    serve_component(page, calendar)

    assert calendar.current_view == "timeGridDay"
    assert page.locator(".fc-timeGridDay-button").first.get_attribute("class").split()[-1] == "fc-button-active"

    calendar.change_view("dayGridMonth")
    assert page.locator(".fc-dayGridMonth-button").first.get_attribute("class").split()[-1] == "fc-button-active"
    assert calendar.current_view == "dayGridMonth"
    assert text_input.value == "dayGridMonth"


def test_calendar_date_click_callback(page):
    def callback(event):
        text_input.value = event["dateStr"]

    text_input = TextInput(name="Date Click")
    calendar = Calendar(
        current_date="2020-01-01",
        current_view="dayGridMonth",
        date_click_callback=callback,
        selectable=True,
    )
    serve_component(page, calendar)

    page.locator(".fc-daygrid-day-frame", has_text="15").first.click()
    assert text_input.value == "2020-01-15"


def test_calendar_event_click_callback(page):
    def callback(event):
        text_input.value = event["title"]

    text_input = TextInput(name="Event Click")
    calendar = Calendar(
        current_date="2020-01-01",
        value=[{"title": "Test Event", "start": "2020-01-15"}],
        event_click_callback=callback,
    )
    serve_component(page, calendar)

    page.locator(".fc-sticky").first.click()
    wait_until(lambda: text_input.value == "Test Event")
    assert text_input.value == "Test Event"


def test_calendar_event_drop_callback(page):
    def callback(event):
        text_input.value = f"{event['event']['title']}:{event['event']['start']}"

    text_input = TextInput(name="Drop")
    calendar = Calendar(
        current_date="2020-01-01",
        value=[{"title": "Test Event", "start": "2020-01-15"}],
        event_drop_callback=callback,
        editable=True,
    )
    serve_component(page, calendar)

    event = page.locator(".fc-event").first
    target = page.locator(".fc-daygrid-day-frame", has_text="16").first
    event.drag_to(target)
    assert text_input.value == "Test Event:2020-01-16"


def test_calendar_select_callback(page):
    def callback(event):
        text_input.value = f"{event['start']}:{event['end']}"

    text_input = TextInput(name="Select")
    calendar = Calendar(
        current_date="2020-01-01",
        current_view="dayGridMonth",
        selectable=True,
        select_callback=callback,
    )
    serve_component(page, calendar)

    start = page.locator(".fc-daygrid-day-frame", has_text="15").first
    end = page.locator(".fc-daygrid-day-frame", has_text="17").first
    start.drag_to(end)
    assert text_input.value == "2020-01-15T00:00:00.000Z:2020-01-18T00:00:00.000Z"


def test_calendar_unselect_callback(page):
    def callback(event):
        text_input.value = "unselected"

    text_input = TextInput(name="Unselect")
    calendar = Calendar(
        current_date="2020-01-01",
        current_view="dayGridMonth",
        selectable=True,
        unselect_callback=callback,
    )
    serve_component(page, calendar)

    start = page.locator(".fc-daygrid-day-frame", has_text="15").first
    end = page.locator(".fc-daygrid-day-frame", has_text="17").first
    start.drag_to(end)
    page.locator(".fc-toolbar-title").first.click()
    assert text_input.value == "unselected"


def test_calendar_get_event_in_view(page):
    calendar = Calendar(
        current_date="2020-01-15",
        value=[
            {"title": "Test Event", "start": "2020-01-15"},
            {"title": "Test Event 2", "start": "2020-01-16"},
        ],
    )
    serve_component(page, calendar)
    wait_until(lambda: page.locator(".fc-event-title").first.inner_text() == "Test Event")
    event = calendar.get_event_in_view("2020-01-15", title="Test Event")
    assert event.title == "Test Event"
    assert event.start == "2020-01-15"

    event.set_start("2020-01-17")
    wait_until(lambda: calendar.value[0]["start"] == "2020-01-17")
    assert calendar.value[1]["start"] == "2020-01-16"

    event.set_end("2020-01-18")
    wait_until(lambda: calendar.value[0]["end"] == "2020-01-18")
    assert "end" not in calendar.value[1]

    event.set_props(title="New Title", all_day=True)
    wait_until(lambda: calendar.value[0]["title"] == "New Title")
    assert calendar.value[0]["allDay"] == True
    assert calendar.value[1]["title"] == "Test Event 2"
    assert "allDay" not in calendar.value[1]

    event.remove()
    wait_until(lambda: len(calendar.value) == 1)
    assert calendar.value[0]["title"] == "Test Event 2"
