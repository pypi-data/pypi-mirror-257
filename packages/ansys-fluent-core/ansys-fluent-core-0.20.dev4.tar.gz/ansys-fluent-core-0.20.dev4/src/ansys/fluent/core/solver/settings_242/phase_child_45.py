#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
)

from .ai import ai as ai_cls
from .aj import aj as aj_cls
from .ak import ak as ak_cls
from .x_origin import x_origin as x_origin_cls
from .y_origin import y_origin as y_origin_cls
from .z_origin import z_origin as z_origin_cls
from .shift_x import shift_x as shift_x_cls
from .shift_y import shift_y as shift_y_cls
from .shift_z import shift_z as shift_z_cls
from .periodic import periodic as periodic_cls
from .geometry_2 import geometry as geometry_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['ai', 'aj', 'ak', 'x_origin', 'y_origin', 'z_origin', 'shift_x',
         'shift_y', 'shift_z', 'periodic', 'geometry']

    _child_classes = dict(
        ai=ai_cls,
        aj=aj_cls,
        ak=ak_cls,
        x_origin=x_origin_cls,
        y_origin=y_origin_cls,
        z_origin=z_origin_cls,
        shift_x=shift_x_cls,
        shift_y=shift_y_cls,
        shift_z=shift_z_cls,
        periodic=periodic_cls,
        geometry=geometry_cls,
    )

