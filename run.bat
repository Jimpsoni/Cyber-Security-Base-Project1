call .\venv\Scripts\activate.bat
cd project1/
python manage.py migrate --run-syncdb
python manage.py runserver