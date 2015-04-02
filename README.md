Ubuntu Partners
===

The Django-based website project for <http://partners.ubuntu.com>.

Local development
---

### Dependencies

``` bash
sudo apt-get install postgresql postgresql-server-dev-9.x graphviz-dev rubygems
sudo gem install sass
```

To create your postgres user and database::

``` bash
$ sudo -u postgres psql postgres

postgres=# \password postgres
<type 'dev' as the password>
postgres=# \q

$ sudo -u postgres createdb partners
```

### Run local server

Run the site on <http://localhost:7500> as follows:

``` bash
make develop  # Auto-compile sass files and run the dev server
```

Or to start the server using a different port:

``` bash
PORT=4321 make develop  # Start server on port 4321
```

