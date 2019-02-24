# blog
A simple django based backend apis to create blog posts which lets user (superuser) to write blog and other users to read, comment on it.

# Installation Guide
Pre Requirements-
- Python 3.x
- git
- MySql 5.7 or above
- virtualenv

Get the source code from git-
```
git clone https://github.com/pingrs/blog.git
```
Create virtual environment and install dependencies-
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
Create local settings file-
```
cd blog
cp blog/dev_settings_sample.py blog/dev_settings.py
```
Change the MySql credentials in blog/dev_settings.py

Create a SUPER USER-
```
python manage.py createsuperuser --settings=blog.dev_settings
```
Migrate Database-
```
python manage.py makemigrations
python manage.py migrate --settings=blog.dev_settings
```
Now you are all done. You can run server using-
```
python manage.py runserver --settings=blog.dev_settings
```
Open <http://127.0.0.1:8000> and enjoy!!!
