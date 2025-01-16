from panel_full_calendar import Calendar


def test_calendar_value_snake_case():
    calendar = Calendar(value=[{"start": "2020-01-01", "all_day": True, "id": "1"}])
    assert calendar.value == [{"start": "2020-01-01", "allDay": True, "id": "1"}]

    calendar.add_event(start="2020-01-02", start_recur="2020-01-03", id="2")
    assert calendar.value == [
        {"start": "2020-01-01", "allDay": True, "id": "1"},
        {"start": "2020-01-02", "startRecur": "2020-01-03", "title": "(no title)", "id": "2"},
    ]


def test_calendar_value_snake_case_disabled():
    calendar = Calendar(
        value=[{"start": "2020-01-01", "all_day": True, "id": "3"}],
        event_keys_auto_camel_case=False,
    )
    assert calendar.value == [{"start": "2020-01-01", "all_day": True, "id": "3"}]

    calendar.add_event(start="2020-01-02", start_recur="2020-01-03", id="4")
    assert calendar.value == [
        {"start": "2020-01-01", "all_day": True, "id": "3"},
        {"start": "2020-01-02", "start_recur": "2020-01-03", "title": "(no title)", "id": "4"},
    ]


def test_calendar_value_camel_case():
    calendar = Calendar(value=[{"start": "2020-01-01", "allDay": True, "id": "5"}])
    assert calendar.value == [{"start": "2020-01-01", "allDay": True, "id": "5"}]


def test_calendar_add_event():
    calendar = Calendar()
    calendar.add_event(start="2020-01-01", end="2020-01-02", title="event", id="6")
    assert calendar.value == [{"start": "2020-01-01", "end": "2020-01-02", "title": "event", "id": "6"}]

    calendar.add_event(start="2020-01-03", end="2020-01-04", title="event2", display="background", id="7")
    assert calendar.value == [
        {"start": "2020-01-01", "end": "2020-01-02", "title": "event", "id": "6"},
        {"start": "2020-01-03", "end": "2020-01-04", "title": "event2", "display": "background", "id": "7"},
    ]


def test_calendar_add_event_camel_case_precedence():
    calendar = Calendar()
    calendar.add_event(start="2020-01-01", end="2020-01-02", allDay=True, all_day=False, id="8")
    assert calendar.value == [{"start": "2020-01-01", "end": "2020-01-02", "title": "(no title)", "allDay": True, "id": "8"}]


def test_calendar_clear():
    calendar = Calendar(value=[{"start": "2020-01-01", "allDay": True, "id": "9"}])
    calendar.clear_events()
    assert calendar.value == []
