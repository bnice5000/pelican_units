''' Units is a plugin that convert between unit systems.

Units uses [Pints](https://pint.readthedocs.io/en/stable/) to automatically convert between unit systems.

Using the special notation (INSERT NOTATION HERE), units will seek out, create,
and insert a unit conversion into the page so that measurements are useful to
all readers.

SI

FU

FFF
'''

import copy
import logging
import pprint
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
    
    if value.magnitude != 1:
        p = inflect.engine()
        return p.inflect("{0.magnitude} plural('{0.units}')".format(value))
    else:
        return '{0.magnitude} {0.units}'.format(value)


def replacer(value):
    ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
    ureg.default_system = 'US'
    expression = value.group()[5:-1].strip()
    Q_ = ureg.Quantity
    dir(ureg.sys)

    if '->' in expression:
        unit, to = expression.split('->')
        converted_unit = Q_(unit).to(to)
    else:
        converted_unit = Q_(expression).to_base_units()

    logger.debug('Unit Conversion: {0}'.format(pluralizer(converted_unit)))
    html_unit = 
    return '{0}'.format(pluralizer(converted_unit))


def initialized(pelican):

    DEFAULT_CONFIG.setdefault('UNIT_SYSTEM', 'SI')
    DEFAULT_CONFIG.setdefault('UNIT_HTML_WRAPPER', '<dl><dt>{orig}</dt><dd>{converted}</dd></dl>')

    if pelican:
        pelican.settings.setdefault('UNIT_SYSTEM', 'SI')
        pelican.setdefault('UNIT_HTML_WRAPPER', '<dl><dt>{orig}</dt><dd>{converted}</dd></dl>')


def unit(content):

    if isinstance(content, contents.Static):
        return

    if content._content and ('{unit:' in content._content):
        pattern = re.compile(r'\{unit:([^}]+)\}')
        content._content = re.sub(pattern, replacer, content._content)


def register():
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(unit)
