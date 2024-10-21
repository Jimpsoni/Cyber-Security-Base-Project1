
## Simple way:
Download and unzip the git repo folder. To set up the app, first run the `init.bat` file, then start the server by running `run.bat`. You only have to run `init.bat` once.

## Manual install:
If for some reason these don't work, create a new python virtual environment, activate it, 
and download all the dependencies found in the `dependencies.txt` file. Then cd to project1 folder, run `python manage.py migrate --run-syncdb` and then start the server by running `python manage.py runserver`
