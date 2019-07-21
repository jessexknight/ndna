#!/usr/bin/env bash
score=$(pylint ndna/ | tail -n2 | awk '{print $7}' | cut -d"/" -f1)
url=https://mperlet.github.io/pybadge/badges/$score.svg
curl -s $url > ci/pylint/badge.svg 
