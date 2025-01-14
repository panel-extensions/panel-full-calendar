import pytest

from panel_full_calendar import Calendar


def test_calendar_value_snake_case():
    calendar = Calendar(value=[{"start": "2020-01-01", "all_day": True}])
    assert calendar.value == [{"start": "2020-01-01", "allDay": True}]

    calendar.add_event(start="2020-01-02", start_recur="2020-01-03")
    assert calendar.value == [
        {"start": "2020-01-01", "allDay": True},
        {"start": "2020-01-02", "startRecur": "2020-01-03", "title": "(no title)"},
    ]


def test_calendar_value_snake_case_disabled():
    calendar = Calendar(
        value=[{"start": "2020-01-01", "all_day": True}],
        event_keys_auto_camel_case=False,
    )
    assert calendar.value == [{"start": "2020-01-01", "all_day": True}]

    calendar.add_event(start="2020-01-02", start_recur="2020-01-03")
    assert calendar.value == [
        {"start": "2020-01-01", "all_day": True},
        {"start": "2020-01-02", "start_recur": "2020-01-03", "title": "(no title)"},
    ]


def test_calendar_value_camel_case():
    calendar = Calendar(value=[{"start": "2020-01-01", "allDay": True}])
    assert calendar.value == [{"start": "2020-01-01", "allDay": True}]


def test_calendar_add_event():
    calendar = Calendar()
    calendar.add_event(start="2020-01-01", end="2020-01-02", title="event")
    assert calendar.value == [{"start": "2020-01-01", "end": "2020-01-02", "title": "event"}]

    calendar.add_event(start="2020-01-03", end="2020-01-04", title="event2", display="background")
    assert calendar.value == [
        {"start": "2020-01-01", "end": "2020-01-02", "title": "event"},
        {
            "start": "2020-01-03",
            "end": "2020-01-04",
            "title": "event2",
            "display": "background",
        },
    ]


def test_calendar_add_event_camel_case_precedence():
    calendar = Calendar()
    calendar.add_event(start="2020-01-01", end="2020-01-02", allDay=True, all_day=False)
    assert calendar.value == [
        {
            "start": "2020-01-01",
            "end": "2020-01-02",
            "title": "(no title)",
            "allDay": True,
        }  # camelCase takes precedence
    ]


def test_remove_event_simple():
    # Test basic removal with start, title, no end/all_day provided
    calendar = Calendar(
        value=[
            {
                "start": "2020-01-01",
                "end": "2020-01-02",
                "title": "event",
                "allDay": False,
            },
            {"start": "2020-01-03", "title": "event2", "allDay": True},
        ]
    )
    # Remove first event using minimal arguments (branch: end is None and all_day is None)
    calendar.remove_event("2020-01-01", "event")
    assert calendar.value == [{"start": "2020-01-03", "title": "event2", "allDay": True}]

    # Remove second event (all-day) using appropriate arguments
    calendar.remove_event("2020-01-03", "event2")
    assert calendar.value == []


def test_remove_event_with_end_and_all_day():
    # Test removal when both end and all_day parameters are provided
    calendar = Calendar(
        value=[
            {
                "start": "2020-01-01",
                "end": "2020-01-02",
                "title": "meeting",
                "allDay": True,
            }
        ]
    )
    calendar.remove_event("2020-01-01", "meeting", end="2020-01-02", all_day=True)
    assert calendar.value == []


def test_remove_event_with_end_only():
    # Test removal when only end parameter is provided
    calendar = Calendar(
        value=[
            {
                "start": "2020-02-01",
                "end": "2020-02-02",
                "title": "workshop",
                "allDay": False,
            }
        ]
    )
    calendar.remove_event("2020-02-01", "workshop", end="2020-02-02")
    assert calendar.value == []


def test_remove_event_with_all_day_only():
    # Test removal when only all_day parameter is provided
    calendar = Calendar(value=[{"start": "2020-03-01", "title": "holiday", "allDay": True}])
    calendar.remove_event("2020-03-01", "holiday", all_day=True)
    assert calendar.value == []


def test_remove_event_not_found():
    # Test that removing a non-existent event raises ValueError
    calendar = Calendar(
        value=[
            {
                "start": "2020-04-01",
                "end": "2020-04-02",
                "title": "nonexistent",
                "allDay": False,
            }
        ]
    )
    with pytest.raises(ValueError):
        calendar.remove_event("2021-01-01", "missing event")


def test_remove_event_norm_start():
    calendar = Calendar(
        value=[
            {
                "start": "2020-05-01",
                "end": "2020-05-02",
                "title": "event",
                "allDay": False,
            }
        ]
    )
    calendar.remove_event("2020-05-01T00:00:00", "event")
    assert calendar.value == []


def test_update_event_simple():
    # Test basic update with no end/all_day provided
    calendar = Calendar(
        value=[
            {
                "start": "2020-01-01",
                "end": "2020-01-02",
                "title": "original",
                "allDay": False,
            }
        ]
    )
    calendar.update_event("2020-01-01", "original", updates=dict(title="updated event", location="Room 1"))
    assert calendar.value == [
        {
            "start": "2020-01-01",
            "end": "2020-01-02",
            "title": "updated event",
            "allDay": False,
            "location": "Room 1",
        }
    ]


def test_update_event_with_end_and_all_day():
    # Test update when both end and all_day parameters are provided
    calendar = Calendar(
        value=[
            {
                "start": "2020-05-01",
                "end": "2020-05-02",
                "title": "conference",
                "allDay": True,
            }
        ]
    )
    calendar.update_event(
        "2020-05-01",
        "conference",
        end="2020-05-02",
        all_day=True,
        updates=dict(
            title="updated conference",
            speakers=5,
        ),
    )
    assert calendar.value == [
        {
            "start": "2020-05-01",
            "end": "2020-05-02",
            "title": "updated conference",
            "allDay": True,
            "speakers": 5,
        }
    ]


def test_update_event_with_end_only():
    # Test update when only end parameter is provided
    calendar = Calendar(
        value=[
            {
                "start": "2020-06-01",
                "end": "2020-06-02",
                "title": "seminar",
                "allDay": False,
            }
        ]
    )
    calendar.update_event(
        "2020-06-01",
        "seminar",
        end="2020-06-02",
        updates=dict(
            title="updated seminar",
            duration="2h",
        ),
    )
    assert calendar.value == [
        {
            "start": "2020-06-01",
            "end": "2020-06-02",
            "title": "updated seminar",
            "allDay": False,
            "duration": "2h",
        }
    ]


def test_update_event_with_all_day_only():
    # Test update when only all_day parameter is provided
    calendar = Calendar(value=[{"start": "2020-07-01", "title": "festival", "allDay": True}])
    calendar.update_event(
        "2020-07-01",
        "festival",
        all_day=True,
        updates=dict(
            title="updated festival",
            location="Park",
        ),
    )
    assert calendar.value == [
        {
            "start": "2020-07-01",
            "title": "updated festival",
            "allDay": True,
            "location": "Park",
        }
    ]


def test_update_event_not_found():
    # Test that updating a non-existent event raises ValueError
    calendar = Calendar(value=[{"start": "2020-08-01", "title": "gala", "allDay": False}])
    with pytest.raises(ValueError):
        calendar.update_event("2020-09-01", "nonexistent", updates=dict(title="should fail"))


def test_update_event_norm_start():
    calendar = Calendar(
        value=[
            {
                "start": "2020-10-01",
                "end": "2020-10-02",
                "title": "meeting",
                "allDay": False,
            }
        ]
    )
    calendar.update_event(
        "2020-10-01T00:00:00",
        "meeting",
        updates=dict(
            title="updated meeting",
            location="Office",
        ),
    )
    assert calendar.value == [
        {
            "start": "2020-10-01",
            "end": "2020-10-02",
            "title": "updated meeting",
            "allDay": False,
            "location": "Office",
        }
    ]


def test_filter_events_with_start_only():
    # Test filtering when only start date is provided
    calendar = Calendar(
        value=[
            {"start": "2020-07-01", "title": "festival", "allDay": True},
            {"start": "2020-07-01", "title": "meeting", "allDay": False},
            {"start": "2020-07-02", "title": "concert", "allDay": True},
        ]
    )
    filtered = calendar.filter_events("2020-07-01")
    assert filtered == [
        {"start": "2020-07-01", "title": "festival", "allDay": True},
        {"start": "2020-07-01", "title": "meeting", "allDay": False},
    ]


def test_filter_events_with_all_day():
    # Test filtering with start date and all_day parameter
    calendar = Calendar(
        value=[
            {"start": "2020-08-01", "title": "conference", "allDay": True},
            {"start": "2020-08-01", "title": "meeting", "allDay": False},
            {"start": "2020-08-02", "title": "workshop", "allDay": True},
        ]
    )
    filtered = calendar.filter_events("2020-08-01", all_day=True)
    assert filtered == [
        {"start": "2020-08-01", "title": "conference", "allDay": True},
    ]


def test_filter_events_with_end_date():
    # Test filtering with both start and end dates
    calendar = Calendar(
        value=[
            {
                "start": "2020-09-01",
                "end": "2020-09-02",
                "title": "seminar",
                "allDay": False,
            },
            {
                "start": "2020-09-01",
                "end": "2020-09-03",
                "title": "workshop",
                "allDay": False,
            },
        ]
    )
    filtered = calendar.filter_events("2020-09-01", end="2020-09-02")
    assert filtered == [
        {
            "start": "2020-09-01",
            "end": "2020-09-02",
            "title": "seminar",
            "allDay": False,
        },
    ]


def test_filter_events_norm_datetime():
    # Test that different datetime formats are normalized correctly
    calendar = Calendar(
        value=[
            {
                "start": "2020-10-01",
                "end": "2020-10-02",
                "title": "meeting",
                "allDay": False,
            }
        ]
    )
    filtered = calendar.filter_events("2020-10-01T00:00:00")
    assert filtered == [
        {
            "start": "2020-10-01",
            "end": "2020-10-02",
            "title": "meeting",
            "allDay": False,
        }
    ]


def test_filter_events_no_matches():
    # Test that filtering with no matches returns empty list
    calendar = Calendar(value=[{"start": "2020-11-01", "title": "gala", "allDay": False}])
    filtered = calendar.filter_events("2020-12-01")
    assert filtered == []
