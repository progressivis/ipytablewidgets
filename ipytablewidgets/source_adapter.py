# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

from abc import ABCMeta, abstractmethod, abstractproperty


class SourceAdapter(metaclass=ABCMeta):
    def __init__(self, source, columns=None, compression=None, touch_mode=True):
        self._source = source
        self._columns = columns
        self._compression = compression
        self._touched = False
        self._touch_mode = touch_mode

    @property
    def is_touched(self):
        ret = self._touched
        self._touched = False
        return ret

    def touch(self):
        assert self._touch_mode
        self._touched = True

    def _equals_no_touch_mode(self, other):
        if self._touch_mode or other._touch_mode:
            return True
        return self.equals(other)

    @abstractproperty
    def columns(self):
        ...

    @abstractmethod
    def to_array(self, col):
        ...

    @abstractmethod
    def equals(self, other):
        ...


"""
    @classmethod
    @abstractmethod
    def create(cls, data):
        ...
"""
