#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# from_json.py
#
# Copyright © 2023 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

import os
import json

from mediapack.eqf import EqFluidJCA, EqFluidJCAL
from mediapack.elastic import Elastic
from mediapack.pem import PEM
from mediapack.screen import Screen
from mediapack.fluid import Fluid


__MEDIUMCLASSES_MAP = {
    _.MEDIUM_TYPE: _ for _ in [EqFluidJCA, EqFluidJCAL, Elastic, PEM, Fluid, Screen]
}


def from_json(filename, force=None):
    """Reads medium definition from JSON file filename. Raises an IOError if the file
    is not found, ValueError if medium type is not known and a LookupError if the
    parameter definition is incomplete.

    One may set the optional argument 'force' to a medium type to force loading this one.
    """

    if not os.path.exists(filename):
        raise IOError('Unable to locate file {}'.format(filename))

    with open(filename) as fh:
        json_data = json.load(fh)

    if json_data.get('medium_type') is None and force is None:
        raise LookupError('Unspecified medium type')

    if force is None:
        medium_class = __MEDIUMCLASSES_MAP.get(json_data['medium_type'])
    else:
        medium_class = force
    if medium_class is None:
        raise ValueError('Medium type is not known')
    else:
        medium = medium_class()
        medium.from_dict(json_data)
        return medium


