from traitlets import (TraitType, TraitError,
                       Any as OriginalAny,
                       Bool as OriginalBool,
                       Float as OriginalFloat,
                       Unicode as OriginalUnicode)
from astropy import units as u
from matplotlib import colors

# We inherit the original trait classes to make sure that the docstrings are set

class Any(OriginalAny):

    def __init__(self, *args, **kwargs):
        super(Any, self).__init__(*args, **kwargs)
        if self.help:
            self.__doc__ = self.help

class Bool(OriginalBool):

    def __init__(self, *args, **kwargs):
        super(Bool, self).__init__(*args, **kwargs)
        if self.help:
            self.__doc__ = self.help


class Float(OriginalFloat):

    def __init__(self, *args, **kwargs):
        super(Float, self).__init__(*args, **kwargs)
        if self.help:
            self.__doc__ = self.help


class Unicode(OriginalUnicode):

    def __init__(self, *args, **kwargs):
        super(Unicode, self).__init__(*args, **kwargs)
        if self.help:
            self.__doc__ = self.help


class AstropyQuantity(TraitType):

    default = 0 * u.one
    info_text = '\'Custom trait to handle astropy quantities with units\''

    def __init__(self, *args, **kwargs):
        super(AstropyQuantity, self).__init__(*args, **kwargs)
        if self.help:
            self.__doc__ = self.help

    def validate(self, obj, value):
        if isinstance(value, u.Quantity):
            return value
        self.error(obj, value)


class Color(TraitType):

    def __init__(self, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        if self.help:
            self.__doc__ = self.help

    def validate(self, obj, value):
        if isinstance(value, str) or (isinstance(value, tuple) and len(value) == 3):
            return colors.to_hex(value)
        else:
            if hasattr(obj, 'opacity'):
                raise TraitError('color must be a string or a tuple of 3 or 4 floats')
            else:
                raise TraitError('color must be a string or a tuple of 3 floats')


class ColorWithOpacity(Color):

    def validate(self, obj, value):
        if isinstance(value, tuple) and len(value) == 4:
            obj.opacity = value[-1]
            value = value[:3]
        return super(ColorWithOpacity, self).validate(obj, value)
