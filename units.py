''' Units is a plugin that convert between unit systems.

Units uses [Pints](https://pint.readthedocs.io/en/stable/) to automatically convert between unit systems.

Using the special notation (INSERT NOTATION HERE), units will seek out, create,
and insert a unit conversion into the page so that measurements are useful to
all readers.

SI

FU

FFF
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

    if value.magnitude != 1:
        p = inflect.engine()
        return p.inflect("{magnitude} plural('{units}')".format(magnitude=round(value.magnitude, DEFAULT_CONFIG['UNIT_PRECISION']), units=value.units))
    else:
        return '{magnitude} {units}'.format(magnitude=round(value.magnitude, DEFAULT_CONFIG['UNIT_PRECISION']), units=value.units)


def replacer(value):
    ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
    ureg.default_system = DEFAULT_CONFIG['UNIT_SYSTEM']
    expression = value.group()[5:-1].strip()
    Q_ = ureg.Quantity
    dir(ureg.sys)

    if '::' in expression:
        unit, *other_units = expression.split('::')
        unit = Q_(unit)
        converted_unit = ', '.join([pluralizer(unit.to(other_unit)) for other_unit in other_units])
        unit = pluralizer(unit)

    else:
        unit = pluralizer(Q_(expression))
        converted_unit = pluralizer(Q_(expression).to_base_units())

    logger.debug(converted_unit)
    # breakpoint()
    html_unit = DEFAULT_CONFIG['UNIT_HTML_WRAPPER'].format(unit=unit, converted=converted_unit)
    return html_unit


def initialized(pelican):

    DEFAULT_CONFIG.setdefault('UNIT_SYSTEM', 'SI')
    DEFAULT_CONFIG.setdefault('UNIT_PRECISION', 2)
    DEFAULT_CONFIG.setdefault('UNIT_HTML_WRAPPER', '{unit} (<em>{converted}</em>)')

    if pelican:
        pelican.settings.setdefault('UNIT_SYSTEM', 'SI')
        DEFAULT_CONFIG.setdefault('UNIT_PRECISION', 2)
        pelican.settings.setdefault('UNIT_HTML_WRAPPER', '{unit} (<em>{converted}</em>)')


def unit(content):

    if isinstance(content, contents.Static):
        return

    if content._content and ('{unit:' in content._content):
        pattern = re.compile(r'\{unit:([^}]+)\}')
        content._content = re.sub(pattern, replacer, content._content)


def register():
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(unit)
