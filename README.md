Ubuntu Partners
===

The Django-based website project for <http://partners.ubuntu.com>.

Local development
---

First, [install Docker](https://docs.docker.com/installation/). (For Ubuntu 14.04, try [this guide instead](https://robinwinslow.co.uk/2015/04/02/installing-docker-on-ubuntu/).)

### Run local server

Run the site on <http://localhost:8003> as follows:

``` bash
make run  # Run docker containers, mapping server to port 8003
```

Or to start the server using a different port:

``` bash
PORT=4321 make run  # Start server on port 4321
```
