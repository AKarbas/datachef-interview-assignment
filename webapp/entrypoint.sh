#!/usr/bin/env bash

set -eEuo pipefail

./wait-for-it.sh campaigns_postgres:5432
./wait-for-it.sh campaigns_cache:11211

./manage.py migrate
#./manage.py importdata

$($@)
