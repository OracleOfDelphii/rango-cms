# rango-cms

A mini-CMS developed with Django framework.

## Current features:
- Seperate adminstratoin Panel with nice Bootstrap powered UI
- add/delete articles
- A minimal ready to use template.
## New features!
- add/delete categories
- nice Login UI with bootstrap

### Technologies Used:
- Django3.1.12 and Django rest 3.12.4
- Ajax
- HTML, CSS, Bootstrap
- Sqlite3
- ckeditor
- tempus-dominus

### How to install and work:

```
-- clone --
cd rango-cms
python -m venv venv
./venv/scripts/activate # or source for linux
pip3 install -r requirements.txt
cd website
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
