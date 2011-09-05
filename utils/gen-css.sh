#!/bin/bash
#
# Script to generate the Solarized CSS from the Pygments style.
# Adds `.highlight span >` to play nice with other content.

css_file=../css/solarized.css

pygmentize -S solarized -f html > $css_file
sed -i -e 's/.*/.highlight span&/g' $css_file
