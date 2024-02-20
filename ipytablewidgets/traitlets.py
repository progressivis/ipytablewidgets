# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

from traitlets import TraitType, Undefined
from . import SourceAdapter


class TableType(TraitType):

    """
    A SourceAdapter instance trait type.
    """

    info_text = "a sourceAdapter instance trait type"

    klass = SourceAdapter

    def validate(self, obj, value):
        assert value is None or isinstance(value, SourceAdapter)
        return value

    def set(self, obj, value):
        new_value = self._validate(obj, value)
        old_value = obj._trait_values.get(self.name, self.default_value)
        obj._trait_values[self.name] = new_value
        if (
                (old_value is None and new_value is not None)
                or (old_value is Undefined and new_value is not Undefined)
                or (old_value.is_touched or new_value.is_touched)
                or not old_value._equals_no_touch_mode(new_value)
        ):
            obj._notify_trait(self.name, old_value, new_value)

    def __init__(self, default_value=Undefined, **kwargs):
        if default_value is not None and default_value is not Undefined:
            assert isinstance(default_value, self.klass)
        super().__init__(default_value=default_value, **kwargs)
