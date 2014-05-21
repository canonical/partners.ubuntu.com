develop:
	python bootstrap.py env
	env/bin/pip install -r requirements.txt
	env/bin/python manage.py syncdb --noinput
	make sass-watch
	make runserver

sass-watch:
	# Build sass
	sass --debug-info --watch cms/static/css/styles.scss:cms/static/css/styles.css &

runserver:
	env/bin/python manage.py runserver_plus

runserver_prod:
	gunicorn fenchurch.wsgi:application

rebuild-packages:
	pip2tgz packages/ -r requirements.txt

graph:
	./manage.py graph_models cms -o cms.svg -X PartnerModel,CategoryModel && gnome-open cms.svg
