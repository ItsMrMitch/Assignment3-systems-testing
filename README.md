README.md

# Assignment 3 - Automated tests, By Mitchell (OpenCart demo store: https://opencart.abstracta.us)

This package holds my three test cases (9 scenarios) plus the shared code every member uses
(`tests/helpers.py`, `tests/conftest.py`).

| Test cases in `tests/test_member1_account.py` |
| --------------------------------------------- |
| T001 Registration                             |
| T002 Login                                    |
| T003 Forgotten Password                       |

## Run

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
set HEADLESS=0
pytest --html=report.html --self-contained-html
```

Screenshots of every test are saved to `screenshots/` (file name ends in `__PASS` or `__FAIL`).
Requires Python 3.10+ and Google Chrome (Selenium Manager downloads the driver).
