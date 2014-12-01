Ubuntu Partners
===

The Django-based website project for <http://partners.ubuntu.com>.

Local development
---

Once you've installed dependencies (see below), then you can run the site as follows:

``` bash
make develop  # Auto-compile sass files and run the dev server
```

Or to start the repository on a different port:

``` bash
PORT=4321 make develop  # Start server on port 4321
```

Dependencies
---

``` bash
sudo apt-get install postgresql
sudo apt-get install postgresql-server-dev-9.x
sudo apt-get install graphviz-dev
sudo apt-get install rubygems
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

