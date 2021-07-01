from enum import Enum


class ExperimentType(Enum):
    """This enumeration represents the list experiment type available."""

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
