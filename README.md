## GYMKHANA Calendar

__Installing and running__

Clone the repository

Add  `ALLOWED_HOSTS` in `mycalendar/settings.py` for deployment

### Install virtual environment

Install **pip** first

    sudo apt-get install python3-pip

Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

Now create a virtual environment

    virtualenv venv 

>you can use any name insted of **venv**

Active your virtual environment:

    source venv/bin/activate

Run the following commands in project directory

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Go to [http:localhost:8000/admin](http:localhost:8000/admin) and sign in as superuser.
