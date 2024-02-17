# Copyright (C) 2017 ScienJus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use this rule to prevent values with octal numbers. In YAML, numbers that
start with ``0`` are interpreted as octal, but this is not always wanted.
For instance ``010`` is the city code of Beijing, and should not be
converted to ``8``.

.. rubric:: Options

* Use ``forbid-implicit-octal`` to prevent numbers starting with ``0``.
* Use ``forbid-explicit-octal`` to prevent numbers starting with ``0o``.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   octal-values:
     forbid-implicit-octal: true
     forbid-explicit-octal: true

.. rubric:: Examples

#. With ``octal-values: {forbid-implicit-octal: true}``

   the following code snippets would **PASS**:
   ::

    user:
      city-code: '010'

   the following code snippets would **PASS**:
   ::

    user:
      city-code: 010,021

   the following code snippets would **FAIL**:
   ::

    user:
      city-code: 010

#. With ``octal-values: {forbid-explicit-octal: true}``

   the following code snippets would **PASS**:
   ::

    user:
      city-code: '0o10'

   the following code snippets would **FAIL**:
   ::

    user:
      city-code: 0o10
"""

import re

import yaml

from yamllint.linter import LintProblem

ID = 'octal-values'
TYPE = 'token'
CONF = {'forbid-implicit-octal': bool,
        'forbid-explicit-octal': bool}
DEFAULT = {'forbid-implicit-octal': True,
           'forbid-explicit-octal': True}

IS_OCTAL_NUMBER_PATTERN = re.compile(r'^[0-7]+$')


def check(conf, token, prev, next, nextnext, context):
    if prev and isinstance(prev, yaml.tokens.TagToken):
        return

    if conf['forbid-implicit-octal']:
        if isinstance(token, yaml.tokens.ScalarToken):
            if not token.style:
                val = token.value
                if (val.isdigit() and len(val) > 1 and val[0] == '0' and
                        IS_OCTAL_NUMBER_PATTERN.match(val[1:])):
                    yield LintProblem(
                        token.start_mark.line + 1, token.end_mark.column + 1,
                        f'forbidden implicit octal value "{token.value}"')

    if conf['forbid-explicit-octal']:
        if isinstance(token, yaml.tokens.ScalarToken):
            if not token.style:
                val = token.value
                if (len(val) > 2 and val[:2] == '0o' and
                        IS_OCTAL_NUMBER_PATTERN.match(val[2:])):
                    yield LintProblem(
                        token.start_mark.line + 1, token.end_mark.column + 1,
                        f'forbidden explicit octal value "{token.value}"')
