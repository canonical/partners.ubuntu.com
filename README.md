Ubuntu Partners
===

The Django-based website project for <http://partners.ubuntu.com>.

Dependencies
---

    sudo apt-get install postgresql
    sudo apt-get install postgresql-server-dev-9.x
    sudo apt-get install graphviz-dev
    sudo apt-get install rubygems
    sudo gem install sass

To create your postgres user and database::

    $ sudo -u postgres psql postgres

    postgres=# \password postgres
    <type 'dev' as the password>
    postgres=# \q

    $ sudo -u postgres createdb partners
