# [Learning Logs](https://learning-logs-app.onrender.com/)

Django APP for creating notes on your study topics

## Tools

[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

## Run locally

The first thing to do is to clone the repository:

```sh
git clone https://github.com/ogabrielrdgs/learning_logs.git
cd learning_logs
```

Create a virtual environment to install dependencies in and activate it:

```sh
python -m venv venv
source venv/Scripts/activate
```

Then install the dependencies:

```sh
pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:

```sh
python manage.py migrate
python manage.py runserver
```

And navigate to `http://localhost:8000`.
