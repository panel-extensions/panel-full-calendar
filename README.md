# ✨ panel-full-calendar

[![CI](https://img.shields.io/github/actions/workflow/status/panel-extensions/panel-full-calendar/ci.yml?style=flat-square&branch=main)](https://github.com/panel-extensions/panel-full-calendar/actions/workflows/ci.yml)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/panel-full-calendar?logoColor=white&logo=conda-forge&style=flat-square)](https://prefix.dev/channels/conda-forge/packages/panel-full-calendar)
[![pypi-version](https://img.shields.io/pypi/v/panel-full-calendar.svg?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/panel-full-calendar)
[![python-version](https://img.shields.io/pypi/pyversions/panel-full-calendar?logoColor=white&logo=python&style=flat-square)](https://pypi.org/project/panel-full-calendar)
Extends HoloViz Panel with FullCalendar capabilities

## Features

panel-full-calendar

## Pin your version!

This project is **in its early stages**, so if you find a version that suits your needs, it’s recommended to **pin your version**, as updates may introduce changes.

## Installation

Install it via `pip`:

```bash
pip install panel-full-calendar
```

## Usage

```python
import panel_full_calendar
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

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

Please ensure your code adheres to the project's coding standards and passes all tests.
