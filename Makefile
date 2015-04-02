define HELP_TEXT
Canonical.com website project
===

Usage:

> make run  # Run the Docker containers, mapping 8003 to the site

endef

# Variables
##

ifeq ($(PORT),)
	PORT=8003
endif

help:
	$(info ${HELP_TEXT})

clean:
	rm -rf pip-cache

update-db:
	./manage.py syncdb --noinput --migrate
 
update-charm:
	if [ $(DATABASE_URL) ]; then $(MAKE) update-db; fi

pip-cache:
	bzr branch -r `cat pip-cache-revno.txt` lp:~webteam-backend/ubuntu-partner-website/dependencies pip-cache

# New docker instructions
# ===

APP_IMAGE=ubuntudesign/ubuntu-partners
DB_CONTAINER=ubuntu-partners-postgres
SASS_CONTAINER=ubuntu-partners-sass

rebuild-app-image:
	-docker rm -f ${APP_IMAGE}
	docker build -t ubuntu-partners .

sass-watch:
	docker start ${SASS_CONTAINER} || docker run --name ${SASS_CONTAINER} -d -v `pwd`:/app ubuntudesign/sass sass --debug-info --watch /app/cms/static/css

start-db:
	-docker rm -f ${DB_CONTAINER}
	docker run --name ${DB_CONTAINER} -d postgres
	while ! echo "^]" | netcat `docker inspect --format '{{ .NetworkSettings.IPAddress }}' ${DB_CONTAINER}` 5432; do sleep 0.01; done
	${MAKE} update-db-container

update-db-container:
	docker run --volume `pwd`/app --link ${DB_CONTAINER}:postgres ${APP_IMAGE} bash -c "DATABASE_URL=\$$(echo \$$POSTGRES_PORT | sed 's!tcp://!postres://postgres@!')/postgres python manage.py syncdb --noinput --migrate"

run:
	docker start ${DB_CONTAINER} || ${MAKE} start-db
	${MAKE} sass-watch
	@echo ""
	@echo "======================================="
	@echo "Running server on http://localhost:${PORT}"
	@echo "======================================="
	@echo ""
	docker run --tty --interactive --volume `pwd`:/app --publish ${PORT}:8000 --link ${DB_CONTAINER}:postgres ${APP_IMAGE}
