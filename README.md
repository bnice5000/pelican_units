# pelican_units
A pelican plugin that will automatically convert units between different systems.

Units uses [Pints](https://pint.readthedocs.io/en/stable/) to automatically convert between unit systems.

Units will automagically convert your units and measurements into another unit. Units will seek out, create, and insert a unit conversion into the page so that measurements are useful to a wider audience. This plugin is especially useful to people who live in a country that does not use the SI system of measurement (such as the United States). It will give their audience a better appreciation of the measurements that are mentioned without much additional work for the author.

## Prerequisites: 

This package requires [Pint](https://github.com/hgrecco/pint) and [inflict](https://github.com/jaraco/inflect) before running. Pint is the engine 
behind the unit conversion. Inflict pluralizes the units so that they are grammatically correct.

## Usage:

Units takes two different notations.

The first notation will convert the annotated measurement to the default system:

`This is a test of a single conversion {unit: 10 ft}.`

The second method allows you to specify the unit conversion or many converstions:

`This tests a single conversion to a specified unit {unit: 28g :: oz}`

`This tests multiple conversion to a specified unit {unit: 28g :: oz :: lbs}`
