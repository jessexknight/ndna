#!/usr/bin/env bash
score=$(pylint --rcfile=ci/pylint/.pylintrc ndna/ | tail -n2 | awk '{print $7}' | cut -d"/" -f1)
echo pylint score = $score
url=https://mperlet.github.io/pybadge/badges/$score.svg
curl -s $url > ci/pylint/badge.svg
cp ci/pylint/badge.svg docs/src/_static/icon/pylint-badge.svg
