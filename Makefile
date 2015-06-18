SHELL := /bin/bash  # Use bash syntax

# Settings
# ===

# Default port for the dev server - can be overridden e.g.: "PORT=1234 make run"
ifeq ($(PORT),)
	PORT=8003
endif

# Settings
# ===
PROJECT_NAME=ubuntu-partners
APP_IMAGE=${PROJECT_NAME}
DB_CONTAINER=${PROJECT_NAME}-postgres
SASS_CONTAINER=${PROJECT_NAME}-sass

# Help text
# ===

define HELP_TEXT

${PROJECT_NAME} - A Django website by the Canonical web team
===

Basic usage
---

> make run         # Prepare Docker images and run the Django site

Now browse to http://127.0.0.1:${PORT} to run the site

All commands
---

> make help               # This message
> make run                # build, watch-sass and run-site
> make it so              # a fun alias for "make run"
> make build-app-image    # Build the docker image
> make run-site           # Use Docker to run the website
> make watch-sass         # Setup the sass watcher, to compile CSS
> make compile-sass       # Setup the sass watcher, to compile CSS
> make stop-sass-watcher  # If the watcher is running in the background, stop it
> make prepare-db         # Start and provision the database
> make start-db           # Start the database container
> make stop-db            # Stop the databse container
> make reset-db           # Delete and re-prepare the database
> make update-db          # sync and migrate the database with Django
> make connect-to-db      # Start an interactive postgresql shell to manipulate the database
> make clean              # Delete all created images and containers

(To understand commands in more details, simply read the Makefile)

endef

##
# Print help text
##
help:
	$(info ${HELP_TEXT})

##
# Use docker to run the sass watcher and the website
##
run:
	${MAKE} build-app-image
	${MAKE} prepare-db
	${MAKE} watch-sass &
	${MAKE} run-site && ${MAKE} stop-db

##
# Build the docker image
##
build-app-image:
	docker build -t ${APP_IMAGE} .

##
# Run the Django site using the docker image
##
run-site:
	# Make sure IP is correct for mac etc.
	$(eval docker_ip := 127.0.0.1)
	if hash boot2docker 2> /dev/null; then `eval docker_ip := $(boot2docker ip)`; fi

	@echo ""
	@echo "======================================="
	@echo "Running server on http://${docker_ip}:${PORT}"
	@echo "======================================="
	@echo ""
	docker run -p 0.0.0.0:${PORT}:8000 --link ${DB_CONTAINER}:postgres -v `pwd`:/app -w=/app ${APP_IMAGE} bash -c "DATABASE_URL=\$$(echo \$$POSTGRES_PORT | sed 's!tcp://!postres://postgres@!')/postgres python manage.py runserver 0.0.0.0:8000"

##
# Create or start the sass container, to rebuild sass files when there are changes
##
watch-sass:
	docker attach ${SASS_CONTAINER} || docker start -a ${SASS_CONTAINER} || docker run --name ${SASS_CONTAINER} -v `pwd`:/app ubuntudesign/sass sass --debug-info --watch /app/static/css

##
# Force a rebuild of the sass files
##
compile-sass:
	docker run -ti -v `pwd`:/app ubuntudesign/sass sass --debug-info --update /app/static/css --force

##
# If the watcher is running in the background, stop it
##
stop-sass-watcher:
	docker stop ${SASS_CONTAINER}

##
# Re-create the app image (e.g. to update dependencies)
##
rebuild-app-image:
	-docker rmi -f ${APP_IMAGE}
	${MAKE} build-app-image

# Database commands
# ===

##
# Start and provision the database
##
prepare-db:
	${MAKE} start-db
	while ! docker logs ${DB_CONTAINER} 2>&1 | grep 'database system is ready'; do sleep 0.01; done
	${MAKE} update-db

##
# Start the database container
##
start-db:
	docker start ${DB_CONTAINER} || docker run --name ${DB_CONTAINER} -d postgres

##
# Stop the database container
##
stop-db:
	docker stop ${DB_CONTAINER}

##
# Re-create and provision the database container
##
reset-db:
	-docker rm -f ${DB_CONTAINER}
	${MAKE} prepare-db

##
# Update postgres from the Django application
##
update-db:
	docker run --volume `pwd`:/app -w /app --link ${DB_CONTAINER}:postgres ${APP_IMAGE} bash -c "DATABASE_URL=\$$(echo \$$POSTGRES_PORT | sed 's!tcp://!postres://postgres@!')/postgres python manage.py syncdb --noinput --migrate"

##
# Connect to the postgres database container, for direct editing
##
connect-to-db:
	docker run -it --link ${DB_CONTAINER}:postgres --rm postgres sh -c 'exec psql -h "$$POSTGRES_PORT_5432_TCP_ADDR" -p "$$POSTGRES_PORT_5432_TCP_PORT" -U postgres'

##
# Delete all created images and containers
##
clean:
	-docker rm -f ${DB_CONTAINER} ${SASS_CONTAINER}
	-docker rmi -f ${APP_IMAGE}

# The below targets
# are just there to allow you to type "make it so"
# as a replacement for "make develop"
# - Thanks to https://directory.canonical.com/list/ircnick/deadlight/

it:
so: run

# Phone targets (don't correspond to files or directories)
.PHONY: help build run run-site watch-sass compile-sass stop-sass-watcher rebuild-app-image it so
