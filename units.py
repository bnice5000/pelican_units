''' Units is a plugin that convert between unit systems.

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

'''

import logging
import re

from pelican.settings import DEFAULT_CONFIG
from pelican import contents, signals

logger = logging.getLogger(__name__)

try:
    import pint
except ImportError:
    logger.fatal('Pint not found')

try:
    import inflect
except ImportError:
    logger.fatal('Inflect not found')


def pluralizer(value):
    """This procedure pluralizes the unit if it is not singular.


    Args:
        value ([Quantity]): [parameter takes in a pint quantity]

    Returns:
        [string]: [returns a formatted string of the magnitude with a pluralized or singular unit]
    """

    if value.magnitude != 1:
        p = inflect.engine()
        return p.inflect("{magnitude} plural('{units}')".format(magnitude=round(value.magnitude,
                                                                                DEFAULT_CONFIG['UNIT_PRECISION']),
                                                                units=value.units))
    else:
        return '{magnitude} {units}'.format(magnitude=round(value.magnitude, DEFAULT_CONFIG['UNIT_PRECISION']),
                                            units=value.units)


def replacer(value):
    """This procedure takes in markdown search for specified unit text and converts unit annotations

    Args:
        value ([string]): [parameter takes in the preprocess markdown]

    Returns:
        [string]: [returns the preprocess markdown with any unit annotations converted to alternate units]
    """

    ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
    ureg.default_system = DEFAULT_CONFIG['UNIT_SYSTEM']
    expression = value.group()[5:-1].strip()
    Q_ = ureg.Quantity

    if '::' in expression:
        unit, *other_units = expression.split('::')
        unit = Q_(unit)
        converted_unit = ', '.join([pluralizer(unit.to(other_unit)) for other_unit in other_units])
        unit = pluralizer(unit)

    else:
        unit = pluralizer(Q_(expression))
        converted_unit = pluralizer(Q_(expression).to_base_units())

    html_unit = DEFAULT_CONFIG['UNIT_HTML_WRAPPER'].format(unit=unit, converted=converted_unit)
    return html_unit


def initialized(pelican):
    """Initializes default variables and then checks for changes to the default in the pelican.conf

    Args:
        pelican ([string]): [parameter takes in all the set variables in the pelican.conf]
    """

    DEFAULT_CONFIG.setdefault('UNIT_SYSTEM', 'SI')
    DEFAULT_CONFIG.setdefault('UNIT_PRECISION', 2)
    DEFAULT_CONFIG.setdefault('UNIT_HTML_WRAPPER', '{unit} (<em>{converted}</em>)')

    if pelican:
        pelican.settings.setdefault('UNIT_SYSTEM', 'SI')
        DEFAULT_CONFIG.setdefault('UNIT_PRECISION', 2)
        pelican.settings.setdefault('UNIT_HTML_WRAPPER', '{unit} (<em>{converted}</em>)')


def unit(content):
    """checks the content for a unit annotation. If there is, it sends it for processing, else it skips the content

    Args:
        content ([string]): [contains the markdown content of each article or page entry in the corpus]
    """

    if isinstance(content, contents.Static):
        return

    if content._content and ('{unit:' in content._content):
        pattern = re.compile(r'\{unit:([^}]+)\}')
        content._content = re.sub(pattern, replacer, content._content)


def register():
    """Registers the plugin with the pelican signal system
    """
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(unit)
