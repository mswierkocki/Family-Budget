# Family Budget
### Simple Family Budget APP
**Description**  
Family Budget example app based on [task](TASKS.md).
The project contain authorisation, tests, fixtures, filtering and pagination.
Entire project is available as an open source project on GitHub.
Commits were add on regular basis. Made with my best judgement.

**Features**
- The application allow for creating several users. 

**Tech**
- Python 3.8
- Django 3.0
    - decouple

# How to
## **Install the application in a local environment**
1. We start with creation of [virtual environments](https://docs.python.org/3/library/venv.html)
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2. (Optional) Create `.env` file with configuration variables:
```text
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=django-insecure-1=django-insecure-1=django-insecure-1=django-insec
```

