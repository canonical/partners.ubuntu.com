develop:
	python bootstrap.py env
	make requirements
	env/bin/python manage.py syncdb --noinput
	env/bin/python manage.py migrate
	make sass-watch
	make runserver

requirements:
	sudo apt-get -y install libjpeg-dev graphviz zlib1g-dev libpng12-dev python-dev
	env/bin/pip install -r requirements.txt

sass-watch:
	# Build sass
	sass --debug-info --watch cms/static/css/styles.scss:cms/static/css/styles.css &

sass:
	# Build sass
	sass --style compressed --update cms/static/css/styles.scss:cms/static/css/styles.css

runserver:
	make sass-watch
	env/bin/python manage.py runserver_plus 0.0.0.0:8000

runserver_prod:
	gunicorn fenchurch.wsgi:application

rebuild-packages:
	pip2tgz packages/ -r requirements.txt

graph:
	./manage.py graph_models cms -o cms.svg -X PartnerModel,CategoryModel && xdg-open cms.svg
