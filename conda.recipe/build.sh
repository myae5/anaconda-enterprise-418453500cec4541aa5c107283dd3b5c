#!/bin/bash

mkdir -p $PREFIX/share/intake/data-model-precip
cp $RECIPE_DIR/../data/* $PREFIX/share/intake/data-model-precip
cp $RECIPE_DIR/../catalog.yml $PREFIX/share/intake/
