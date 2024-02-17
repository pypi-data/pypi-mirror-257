from typing import Union
from silx.utils.enum import Enum as _Enum


class SourceType(_Enum):
    SPALLATION_NEUTRON = "Spallation Neutron Source"
    PULSED_REACTOR_NEUTRON_SOURCE = "Pulsed Reactor Neutron Source"
    REACTOR_NEUTRON_SOURCE = "Reactor Neutron Source"
    SYNCHROTRON_X_RAY_SOURCE = "Synchrotron X-ray Source"
    PULSED_MUON_SOURCE = "Pulsed Muon Source"
    ROTATING_ANODE_X_RAY = "Rotating Anode X-ray"
    FIXED_TUBE_X_RAY = "Fixed Tube X-ray"
    UV_LASER = "UV Laser"
    FREE_ELECTRON_LASER = "Free-Electron Laser"
    OPTICAL_LASER = "Optical Laser"
    ION_SOURCE = "Ion Source"
    UV_PLASMA_SOURCE = "UV Plasma Source"
    METAL_JET_X_RAY = "Metal Jet X-ray"


class Source:
    """Information regarding the x-ray storage ring/facility"""

    def __init__(self, name=None, type=None):
        self._name = name
        self._type = type

    @property
    def name(self) -> Union[None, str]:
        return self._name

    @name.setter
    def name(self, name: Union[str, None]):
        if not isinstance(name, (str, type(None))):
            raise TypeError("name is expected to be None or a str")
        self._name = name

    @property
    def type(self) -> Union[None, SourceType]:
        return self._type

    @type.setter
    def type(self, type_: Union[None, str, SourceType]):
        if type_ is None:
            self._type = None
        else:
            type_ = SourceType.from_value(type_)
            self._type = type_

    def __str__(self):
        return f"source (name: {self.name}, type: {self.type})"
