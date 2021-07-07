#############################################################################
#
#    Copyright (C) 2020 Martín Naya
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU  General Public License
#    along with this program.  If not, see < http:#www.gnu.org/licenses/ >.
#
#    Contact info:
#
#    Martín Naya < martin.naya@udc.es >
#############################################################################

from enum import Enum


class ExperimentType(Enum):
    """This enumeration represents the experiment types available: growth, nodev, rom"""

    growth = "growth"
    nodev = "nodev"
    rom = "rom"

    @staticmethod
    def get_from_value(value):
        if value == ExperimentType.growth.value:
            return ExperimentType.growth
        elif value == ExperimentType.nodev.value:
            return ExperimentType.nodev
        else:
            return ExperimentType.rom

    @staticmethod
    def get_types():
        return [ExperimentType.growth, ExperimentType.nodev, ExperimentType.rom]

    @staticmethod
    def get_types_str():
        return [ExperimentType.growth.value, ExperimentType.nodev.value, ExperimentType.rom.value]
