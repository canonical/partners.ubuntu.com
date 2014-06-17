extra requirements::

    sudo apt-get install postgresql postgresql-server-dev-9.3

To create your postgres user and database::

    $ sudo -u postgres psql postgres

    postgres=# \password postgres
    <type 'dev' as the password>
    postgres=# \q

    $ sudo -u postgres createdb partners
