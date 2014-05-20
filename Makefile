develop:
	python bootstrap.py env
	env/bin/pip install -r requirements.txt
	env/bin/python manage.py syncdb --noinput
	make runserver

runserver:
	env/bin/python manage.py runserver_plus

runserver_prod:
	gunicorn fenchurch.wsgi:application

rebuild-packages:
	pip2tgz packages/ -r requirements.txt

