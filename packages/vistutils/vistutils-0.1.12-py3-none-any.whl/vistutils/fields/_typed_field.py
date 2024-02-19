"""TypedField provides a strongly typed descriptor class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from logging import warning
from typing import Any, Callable

from vistutils.fields import AbstractField
from vistutils.waitaminute import typeMsg


class TypedField(AbstractField):
  """TypedField provides a strongly typed descriptor class"""

  @classmethod
  def _parseArgs(cls, *args, **kwargs) -> dict:
    """Parses the positional arguments"""
    defVal = kwargs.get('defVal', None)
    valType = kwargs.get('valType', None)
    if defVal is not None and valType is not None:
      if args:
        w = """The TypedField constructor received keyword arguments 
        defining both the default value and the value type. The additional 
        positional arguments are ignored."""
        warning(w)
      return {'defVal': defVal, 'valType': valType}
    if defVal is not None and valType is None:
      return {'defVal': defVal, 'valType': type(defVal)}
    if valType is not None and defVal is None:
      if isinstance(valType, type):
        for arg in args:
          if isinstance(arg, type):
            w = """The TypedField constructor received both a positional 
            argument and a keyword argument defining the value type. The 
            positional argument is ignored."""
            warning(w)
          if isinstance(arg, valType):
            return {'defVal': arg, 'valType': valType}
        else:
          return {'valType': valType, 'defVal': None}
      else:
        e = typeMsg('valType', valType, type)
        raise TypeError(e)
    #  defVal is None and valType is None
    if len(args) == 1:
      if isinstance(args[0], type):
        return {'valType': args[0], 'defVal': None}
      return {'defVal': args[0], 'valType': type(args[0])}
    if len(args) == 2:
      typeArg, defValArg = None, None
      for arg in args:
        if isinstance(arg, type):
          if typeArg is not None:
            e = """The TypedField constructor received two positional 
            arguments, but both are types. This ambiguity is prohibited."""
            raise TypeError(e)
          typeArg = arg
        else:
          if defValArg is not None:
            e = """The TypedField constructor received two positional 
            arguments, neither of which are types. This ambiguity is 
            prohibited."""
            raise TypeError(e)
          defValArg = arg
      if isinstance(defValArg, typeArg):
        return {'defVal': defValArg, 'valType': typeArg}
      e = typeMsg('defVal', defValArg, typeArg)
      raise TypeError(e)
    if len(args) > 2:
      e = """The TypedField constructor received more than two positional 
      arguments. This is prohibited."""
      raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    self.__field_index__ = None
    self.__support_init__ = kwargs.get('supportInit', False)
    AbstractField.__init__(self, *args)
    _parsed = self._parseArgs(*args, **kwargs)
    self.__value_type__ = _parsed.get('valType', None)
    if self.__value_type__ is None:
      raise ValueError('No value type defined')
    self.__def_value__ = _parsed.get('defVal', None)

  def getType(self, ) -> tuple[type]:
    """Getter-function for the type"""
    return self.__value_type__,

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Get the value of the field"""
    pvtName = self._getPrivateName()
    if instance is None:
      return self.__get__(owner, owner)
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    if kwargs.get('_recursion', False):
      raise RecursionError
    setattr(instance, pvtName, self.__def_value__)
    return self.__get__(instance, owner, _recursion=True)

  def __set__(self, instance: object, value: Any) -> None:
    """Set the value of the field"""
    pvtName = self._getPrivateName()
    valType = self.getType()
    if isinstance(value, valType):
      setattr(instance, pvtName, value)
    else:
      e = typeMsg('value', value, *valType)
      raise TypeError(e)

  def __delete__(self, instance: object) -> None:
    """Delete the value of the field"""
    pvtName = self._getPrivateName()
    if hasattr(instance, pvtName):
      delattr(instance, pvtName)
    else:
      raise AttributeError('No attribute named: %s' % pvtName)

  def __prepare_owner__(self, owner: type) -> type:
    """Hook into __init__ of owner"""
    if not hasattr(owner, '__typed_fields__'):
      setattr(owner, '__init__', self._preInitFactory(owner))
    existingFields = getattr(owner, '__typed_fields__', [])
    initFields = getattr(owner, '__init_fields__', [])
    self.__field_index__ = len(initFields)
    setattr(owner, '__typed_fields__', [self, *existingFields])
    if self.__support_init__:
      setattr(owner, '__init_fields__', [self, *initFields])

    return owner

  @staticmethod
  def _preInitFactory(owner) -> Callable:
    """Creates the pre-init hook"""
    existingInit = getattr(owner, '__init__', )

    def newInit(this, *args, **kwargs) -> None:
      """The pre-init hook"""
      initFields = getattr(owner, '__init_fields__', [])
      for (i, (field, arg)) in enumerate(zip(initFields, args)):
        field = initFields[i]
        name = field.__field_name__
        if name not in kwargs:
          field.__set__(this, arg)
      existingInit(this, *args, **kwargs)

    return newInit
