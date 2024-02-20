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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .fixes_child import fixes_child

class pb_disc_components(ListObject[fixes_child]):
    """
    'pb_disc_components' child.
    """

    fluent_name = "pb-disc-components"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: fixes_child = fixes_child
    """
    child_object_type of pb_disc_components.
    """
