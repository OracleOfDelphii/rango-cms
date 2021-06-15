# rango-cms

A mini-CMS developed with Django framework.

## Current features:
- Seperate adminstration Panel with nice Bootstrap powered UI
- add/delete articles
- add/delete categories
- publish date for posts(you can send to future or past with this feature.)
- draft/publish
- A minimal ready to use template.


### Technologies Used:
- Django3.1.12 and Django rest 3.12.4
- Ajax
- HTML, CSS, Bootstrap + colorlib Theme
- Sqlite3
- ckeditor
- tempus-dominus

### How to install and work:

```
-- clone --
cd rango-cms
python -m venv venv
./venv/Scripts/activate # or source ./venv/bin/activate for linux
pip3 install -r requirements.txt
cd website
python manage.py makemigrations
python manage.py migrate
python manage.py runserver  # for deployment
```

If you want to use this cms for production change STATIC_ROOT in settings.py to your desired path and then run:

```
python manage.py collectstatic

```



#### TO-DO
API(implemented serializers for now)

##### Screenshots:

![panel](/screenshots/panel.png?raw=true)
![panel](/screenshots/panel2.png?raw=true)
![panel](/screenshots/panel3.png?raw=true)
![panel](/screenshots/post.png?raw=true)
![login](/screenshots/login.jpg?raw=true)
