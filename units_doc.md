Module units
============
Units is a plugin that convert between unit systems.

# pelican_units
A pelican plugin that will automatically convert units between different systems.

Units uses [Pints](https://pint.readthedocs.io/en/stable/) to automatically convert between unit systems.

Units will automagically convert your units and measurements into another unit. Units will seek out, create, and insert a unit conversion into the page so that measurements are useful to a wider audience. This plugin is especially useful to people who live in a country that does not use the SI system of measurement (such as the United States). It will give their audience a better appreciation of the measurements that are mentioned without much additional work for the author.

## Prerequisites:

This package requires [Pint](https://github.com/hgrecco/pint) and [inflict](https://github.com/jaraco/inflect) before running. Pint is the engine behind the unit conversion. Inflict pluralizes the units so that they are grammatically correct.

## Usage:

Units takes two different notations.

The first notation will convert the annotated measurement to the default system:

`This is a test of a single conversion {unit: 10 ft}.`

The second method allows you to specify the unit conversion or many converstions:

`This tests a single conversion to a specified unit {unit: 28g :: oz}`

`This tests multiple conversion to a specified unit {unit: 28g :: oz :: lbs}`

## Project Information

__author__ = "Brian Levin"
__copyright__ = "Copyright 2021, Brian Levin"
__credits__ = [Brian Levin]
__license__ = "MIT"
__version__ = "20210915W"
__maintainer__ = "Brian Levin"
__email__ = "brian4lawschool+units@gmail.com"
__status__ = "Beta"

Functions
---------

    
`initialized(pelican)`
:   Initializes default variables and then checks for changes to the default in the pelican.conf
    
    Args:
        pelican ([string]): [parameter takes in all the set variables in the pelican.conf]

    
`pluralizer(value)`
:   This procedure pluralizes the unit if it is not singular.
    
    
    Args:
        value ([Quantity]): [parameter takes in a pint quantity]
    
    Returns:
        [string]: [returns a formatted string of the magnitude with a pluralized or singular unit]

    
`register()`
:   Registers the plugin with the pelican signal system

    
`replacer(value)`
:   This procedure takes in markdown search for specified unit text and converts unit annotations
    
    Args:
        value ([string]): [parameter takes in the preprocess markdown]
    
    Returns:
        [string]: [returns the preprocess markdown with any unit annotations converted to alternate units]

    
`unit(content)`
:   checks the content for a unit annotation. If there is, it sends it for processing, else it skips the content
    
    Args:
        content ([string]): [contains the markdown content of each article or page entry in the corpus]
