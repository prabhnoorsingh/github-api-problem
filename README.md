## Steps to run this project

1. Clone this git repository (master branch) to your local system folder.
2. Install all Python3.5 packages which are present in requirements.txt.
3. Run below commands (in-order) in the top-level folder of this project:
   * python manage.py makemigrations
   * python manage.py migrate
   * python manage.py runserver
4. Command - *python manage.py runserver*  will by default start the django server on localhost:8000 . Run *localhost:8000* in your browser.

### Accessing the APIs of this project

1. Open *http://127.0.0.1:8000/* in browser. It will list out all the API urls.
2. Admin panel of this project can be accessed via url *http://127.0.0.1:8000/admin* . Credentials of admin module are present in admin_credentials.txt file.