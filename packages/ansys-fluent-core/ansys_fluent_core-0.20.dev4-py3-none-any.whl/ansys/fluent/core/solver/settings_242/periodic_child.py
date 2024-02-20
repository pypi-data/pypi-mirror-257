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

from .name import name as name_cls
from .phase_18 import phase as phase_cls
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
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class periodic_child(Group):
    """
    'child_object_type' of periodic.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'ai', 'aj', 'ak', 'x_origin', 'y_origin',
         'z_origin', 'shift_x', 'shift_y', 'shift_z', 'periodic', 'geometry']

    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
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
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

