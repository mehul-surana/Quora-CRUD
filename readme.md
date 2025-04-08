# Quora Clone (Django + DRF + JWT)

A mini Quora-like app built using **Django**, **Django REST Framework**, and **JWT Authentication**. Users can register, log in, ask questions, answer, and like answers via a clean UI.


## Setup Instructions

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
