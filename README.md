# ✨ panel-full-calendar

[![CI](https://img.shields.io/github/actions/workflow/status/panel-extensions/panel-full-calendar/ci.yml?style=flat-square&branch=main)](https://github.com/panel-extensions/panel-full-calendar/actions/workflows/ci.yml)
[![pypi-version](https://img.shields.io/pypi/v/panel-full-calendar.svg?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/panel-full-calendar)
[![python-version](https://img.shields.io/pypi/pyversions/panel-full-calendar?logoColor=white&logo=python&style=flat-square)](https://pypi.org/project/panel-full-calendar)

Extends HoloViz Panel with FullCalendar capabilities

![Clipboard-20250116-183814-139](https://github.com/user-attachments/assets/54a6d396-926e-4a3b-a9f1-0428776201ce)

## Features

`panel-full-calendar` integrates the powerful [FullCalendar](https://fullcalendar.io/) JavaScript library with the [Panel](https://panel.holoviz.org/) ecosystem, enabling interactive calendar widgets directly in Python applications. It provides the ability to:

- Display and interact with calendars in various views (day, week, month).
- Add, update, and remove events programmatically or through user interactions.
- Customize the calendar's appearance, event handling, and toolbar controls.
- Enable event dragging, resizing, and date selection callbacks.
- Handle recurring events and complex scheduling logic.

This widget is perfect for building dashboards, scheduling applications, and any interface that requires robust calendar functionality.

---

## Pin Your Version

This project is **in its early stages**, so if you find a version that suits your needs, it’s recommended to **pin your version**, as updates may introduce breaking changes.

To pin your version in `requirements.txt`, specify the version explicitly:

```text
panel-full-calendar==0.x.x
```

Or in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
panel-full-calendar = "0.x.x"
```

---

## Installation

Install `panel-full-calendar` via `pip`:

```bash
pip install panel-full-calendar
```

Alternatively, add it to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
panel-full-calendar = "^0.x.x"
```

---

## Usage

To use the calendar in a Panel application:

```python
import panel as pn
from panel_full_calendar import Calendar

pn.extension("fullcalendar")

# Create a basic calendar widget
calendar = Calendar(sizing_mode="stretch_width")
calendar.show()
```

## Development

```bash
git clone https://github.com/panel-extensions/panel-full-calendar
cd panel-full-calendar
```

For a simple setup use [`uv`](https://docs.astral.sh/uv/):

```bash
uv venv
source .venv/bin/activate # on linux. Similar commands for windows and osx
uv pip install -e .[dev]
pre-commit run install
pytest tests
```

For the full Github Actions setup use [pixi](https://pixi.sh):

```bash
pixi run pre-commit-install
pixi run postinstall
pixi run test
```

This repository is based on [copier-template-panel-extension](https://github.com/panel-extensions/copier-template-panel-extension).
To update to the latest template version run:

```bash
pixi exec --spec copier --spec ruamel.yaml -- copier update --defaults --trust
```

Note: `copier` will show `Conflict` for files with manual changes during an update. This is normal. As long as there are no merge conflict markers, all patches applied cleanly.

## ❤️ Contributing

Contributions are welcome 🤗! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

Please ensure your code adheres to the project's coding standards and passes all tests.

If you encounter issues or want to request features, please submit a [GitHub issue](https://github.com/panel-extensions/panel-full-calendar/issues/new/choose).
