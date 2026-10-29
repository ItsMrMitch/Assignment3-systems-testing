README.md

# Assignment 3 - Automated tests, Member 1 (OpenCart demo store: https://opencart.abstracta.us)

This package holds Member 1's three test cases (9 scenarios) plus the shared code every member uses
(`tests/helpers.py`, `tests/conftest.py`).

| Test cases in `tests/test_member1_account.py` |
| --------------------------------------------- |
| T001 Registration                             |
| T002 Login                                    |
| T003 Forgotten Password                       |

## Run

```
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest
set HEADLESS=0                   # (macOS/Linux: export HEADLESS=0) to watch the browser
pytest --html=report.html --self-contained-html
```

Screenshots of every test are saved to `screenshots/` (file name ends in `__PASS` or `__FAIL`).
Requires Python 3.10+ and Google Chrome (Selenium Manager downloads the driver).

This one??
