help:
	@echo "Usage: 'make develop' to set up your environment, then 'make start-dev' to start the devserver and sass compilation. If stuff breaks, run 'make develop' again"

start-dev:
	$(MAKE) sass-watch
	env/bin/python manage.py runserver_plus 0.0.0.0:8000

develop:
	python bootstrap.py env
	$(MAKE) pip-requirements
	. env/bin/activate && $(MAKE) update-db
	$(MAKE) sass-watch
	$(MAKE) runserver

apt-requirements:
	sudo apt-get -y install libjpeg-dev graphviz zlib1g-dev libpng12-dev python-dev

pip-requirements:
	env/bin/pip install -r requirements/dev.txt

sass-watch:
	# Build sass
	sass --debug-info --watch cms/static/css/styles.scss:cms/static/css/styles.css &

sass:
	# Build sass
	sass --style compressed --update cms/static/css/styles.scss:cms/static/css/styles.css

runserver_prod:
	gunicorn fenchurch.wsgi:application

rebuild-packages:
	-mkdir packages
	pip install --download pip-cache/ -r requirements/dev.txt

graph:
	./manage.py graph_models cms -o cms.svg -X PartnerModel,CategoryModel && xdg-open cms.svg

update-db:
	./manage.py syncdb --noinput --migrate

update-charm:
	if [ $(DATABASE_URL) ]; then $(MAKE) update-db; fi
