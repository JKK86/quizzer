# Quizzer
A quiz web application built with Django Framework.

## General Info
An online quiz app, that allows users to choose a quiz from a particular category and test their knowledge within a given time.

## Technologies:
- Python
- Django
- JavaScript
- jQuery
- PyTest
- HTML
- CSS

## Features:
- user authorization (register, login, logout, edit profile, change password, reset password)
- quiz list (all and by category)
- search quizzes
- quiz view (with timer)
- add and modify quizzes for admin users
- admin panel
- tests in PyTest

## Setup

First you should clone this repository:
```
git clone https://github.com/JKK86/quizzer.git
cd  quizzer
```

To run the project you should have Python 3 installed on your computer. Then it's recommended to create a virtual environment for your projects dependencies. To install virtual environment:
```
pip install virtualenv
```
Then run the following command in the project directory:
```
virtualenv venv
```
That will create a new folder venv in your project directory. Next activate virtual environment:
```
source venv/bin/active
```
Then install the project dependencies:
```
pip install -r requirements.txt
```
Now you can run the project with this command:
```
python manage.py runserver
```

**Note** in the settings file you should complete your own database settings.
