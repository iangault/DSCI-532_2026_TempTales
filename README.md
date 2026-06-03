# TempTales: Climate Change Explorer Dashboard

|  |  |
|:-----------------------------------|:-----------------------------------|
| **License** | [![License](https://img.shields.io/github/license/ubc-mds/dsci-532_2026_26_tbd?label=License)](LICENSE) |
| **Python** | [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/) |
| **CI** | [![CI](https://github.com/iangault/DSCI-532_2026_TempTales/actions/workflows/ci.yml/badge.svg)](https://github.com/iangault/DSCI-532_2026_TempTales/actions/workflows/ci.yml) |

## About this repo

This is a personal continuation of a UBC MDS group project (DSCI 532, 2026). The original dashboard was built collaboratively; this fork is a solo rebuild and improvement focused on production-readiness: adding CI, fixing test infrastructure, improving code quality, and preparing for redeployment.

**Skills this project covers:** - **Python Shiny** — reactive server/UI separation, ibis lazy expressions, DuckDB backend - **Data visualization** — Altair (time-series, comparison charts), Plotly (choropleth map) - **Testing** — pytest unit tests + Playwright end-to-end browser tests (62 unit + 6 UI tests) - **CI/CD** — GitHub Actions workflow: unit tests → Playwright UI tests on every push/PR - **LLM integration** — GitHub Models API (`gpt-4.1-mini`) via `chatlas` + `querychat` for an AI assistant tab - **Cloud deployment** — Posit Connect Cloud via GitHub integration

## Overview

**TempTales** is an interactive dashboard for exploring global and country-level temperature trends from 1860–2012. Users can select a country, compare two years, view seasonal and monthly patterns, and see temperature shifts on a world heatmap. An AI assistant tab lets users query the data in natural language.

Deployed dashboard: https://iangault-dsci-532-2026-temptales.share.connect.posit.cloud/

## Features

-   **Country selection** — explore temperature data for any country in the dataset
-   **Two-year comparison** — validated baseline vs. target year inputs with error messaging
-   **Monthly dual-line chart** — Altair overlay of monthly averages (Jan–Dec) with hover tooltips
-   **Data table** — monthly comparison with red/blue diverging color scale; CSV export
-   **World heatmap** — Plotly choropleth of global temperatures for the selected year
-   **Seasonal breakdown** — seasonal averages and historical event context
-   **AI assistant** — natural language queries over the dataset via GitHub Models API

## Project structure

```         
src/
├── app.py           # entry point — reactive server logic only
├── ui.py            # all layout and widget definitions
├── plot.py          # Altair chart builders (monthly line, yearly, diff)
├── map.py           # Plotly choropleth map
├── utils.py         # ibis/DuckDB connection; pre-aggregated lazy tables
├── chat.py          # QueryChat + ChatGithub setup for the AI tab
├── data_count.py    # temperature/observation summary helpers
└── table_styles.py  # diverging colour styles for DataGrid tables

tests/
├── test_data_count.py       # 9 tests — data_count_prep()
├── test_data_processor.py   # 13 tests — get_season()
├── test_map.py              # 9 tests — apply_country_highlight()
├── test_plot.py             # 9 tests — build_temp_chart()
├── test_table_styles.py     # 9 tests — table_styles_wide(), diverging_styles()
└── test_ui_playwright.py    # 6 UI tests — full dashboard in Chromium
```

## Local setup

``` bash
git clone https://github.com/iangault/DSCI-532_2026_TempTales.git
cd DSCI-532_2026_TempTales
make install            # creates the '532_project' conda env
conda activate 532_project
```

**Data:** the processed parquet is committed — no download needed. If you need to regenerate it from raw Kaggle CSVs:

``` bash
make db
```

**AI tab:** requires a `GITHUB_API_KEY` in a `.env` file at the project root. Get one at [github.com/marketplace/models](https://github.com/marketplace/models). Without it the app starts but the AI tab will error.

```         
GITHUB_API_KEY=your_token_here
```

**Run the app:**

``` bash
make run   # launches http://localhost:8000 with auto-reload
```

## Tests

All test dependencies are included in the conda env — no separate `pip install` needed.

**Unit tests** (fast, no browser):

``` bash
pytest tests/ --ignore=tests/test_ui_playwright.py -v
```

**Playwright UI tests** (starts the app, drives a real browser):

``` bash
playwright install --with-deps chromium   # one-time browser binary install
pytest tests/test_ui_playwright.py -v -k "chromium"
```

> Only Chromium is installed in this setup. Always pass `-k "chromium"` — Firefox and WebKit will error without their binaries.

## Deployment

Target: **Posit Connect Cloud** via GitHub integration. `make run` is local-only.

-   Set `GITHUB_API_KEY` as an environment variable in the Connect app settings (not `.env`, which is local-only)
-   The parquet file is committed, so no Kaggle credentials are needed at deploy time

## Original contributors

Emily Jin, Ian Gault, Purity Jangaya, Yusheng Li

## License

Copyright © 2026 Emily Jin, Ian Gault, Purity Jangaya, Yusheng Li. Distributed under the [MIT License](./LICENSE).