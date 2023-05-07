#!/usr/bin/env bash

set -e

for builder in build_*.py; do
    python3 $builder
done
