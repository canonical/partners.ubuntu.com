develop:
	python bootstrap.py env
	$(MAKE) pip-requirements
	. env/bin/activate && $(MAKE) update-db
	$(MAKE) sass-watch
	$(MAKE) runserver

pip-requirements:
	sudo apt-get -y install libjpeg-dev graphviz zlib1g-dev libpng12-dev python-dev
	env/bin/pip install -r requirements/dev.txt

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
	pip2tgz packages/ -r requirements/dev.txt

graph:
	./manage.py graph_models cms -o cms.svg -X PartnerModel,CategoryModel && xdg-open cms.svg

update-db:
	./manage.py syncdb --noinput
	./manage.py migrate

# Should be called when installed on a juju box
update:
	@echo $(CHARM_DIR)/charm_cache/env.json
	@if [ -e $(CHARM_DIR)/charm_cache/env.json ]; then echo "exists"; fi
	@if [ -e $(CHARM_DIR)/charm_cache/env.json ] && grep -q 'DATABASE_URL' $(CHARM_DIR)/charm_cache/env.json; then \
	$(MAKE) update-db; \
	fi
