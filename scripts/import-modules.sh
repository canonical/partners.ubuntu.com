#! /usr/bin/env bash

set -euo pipefail # http://redsymbol.net/articles/unofficial-bash-strict-mode/

# Make directories
mkdir -p static/js/modules
mkdir -p static/sass/modules

# Cookie-policy
cp node_modules/cookie-policy/build/js/cookie-policy.js static/js/modules/cookie-policy.js
cp node_modules/cookie-policy/build/css/cookie-policy.css static/sass/modules/cookie-policy.css

# Global nav
cp node_modules/@canonical/global-nav/dist/index.js static/js/modules/global-nav.js
