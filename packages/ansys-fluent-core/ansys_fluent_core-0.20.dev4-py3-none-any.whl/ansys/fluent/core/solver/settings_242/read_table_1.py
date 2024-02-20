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

from .file_name_6 import file_name as file_name_cls
class read_table(Command):
    """
    3D Reading table command.
    
    Parameters
    ----------
        file_name : str
            Set file name in the 3D table-reading command.
    
    """

    fluent_name = "read-table"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

