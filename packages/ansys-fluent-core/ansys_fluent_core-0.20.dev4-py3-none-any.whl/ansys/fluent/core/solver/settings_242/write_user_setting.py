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

from .file_name_1_1 import file_name_1 as file_name_1_cls
class write_user_setting(Command):
    """
    Write the contents of the Modified Settings Summary table to a file.
    
    Parameters
    ----------
        file_name_1 : str
            'file_name' child.
    
    """

    fluent_name = "write-user-setting"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_1_cls,
    )

