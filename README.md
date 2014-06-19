extra requirements::

    sudo apt-get install postgresql
    sudo apt-get install postgresql-server-dev-9.x


To create your postgres user and database::

    $ sudo -u postgres psql postgres

    postgres=# \password postgres
    <type 'dev' as the password>
    postgres=# \q

    $ sudo -u postgres createdb partners