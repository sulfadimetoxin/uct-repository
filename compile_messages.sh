#!/bin/bash

pybabel extract -o uct-repository/translations/messages.pot uct-repository
pybabel update -d uct-repository/translations -i uct-repository/translations/messages.pot -l cs
pybabel update -d uct-repository/translations -i uct-repository/translations/messages.pot -l en
pybabel compile -d uct-repository/translations
