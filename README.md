README.md

# Assignment 3 - Automated tests, By Mitchell (OpenCart demo store: https://opencart.abstracta.us)

This package holds my three test cases (9 scenarios) helper functions and results
(`tests/helpers.py`, `tests/conftest.py`).

| Test cases in `tests/test_mitchell.py` |
| --------------------------------------------- |
| T001 Registration                             |
| T002 Login                                    |
| T003 Forgotten Password                       |

## Run

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest   # runs the tests once
$env:HEADLESS="0"                # show the browser
pytest --html=report.html --self-contained-html   # runs the tests AND writes an HTML report; no need to run plain pytest first
```

Screenshots of every test are saved to `screenshots/` (file name ends in `__PASS` or `__FAIL`).
Requires Python 3.10+ and Google Chrome (Selenium Manager downloads the driver).

## Requirements
requirements are in requirements.txt
