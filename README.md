## SNTC Calendar

__Installing and running__

Clone the repository

Add  `ALLOWED_HOSTS`  in  `mycalendar/models.py` for deployment

Run the following commands in project directory

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Go to [http:localhost:8000/admin](http:localhost:8000/admin) and sign in as superuser.
