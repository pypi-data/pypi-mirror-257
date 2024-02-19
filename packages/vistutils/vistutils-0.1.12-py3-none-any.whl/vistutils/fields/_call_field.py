"""CallField allows for dynamic addition of methods to a class."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import Callable, Any, Never

from vistutils.text import monoSpace
from vistutils.fields import AbstractField, TypedField
from vistutils.waitaminute import typeMsg


class CallField(TypedField):
  """CallField allows for dynamic addition of methods to a class."""

  def __init__(self, *args, **kwargs) -> None:
    TypedField.__init__(self, FunctionType)
    self.__inner_func__ = None
    self.__positional_args__ = []
    self.__keyword_args__ = dict(**kwargs, )
    for arg in args:
      if callable(arg) and self.__inner_func__ is None:
        self.__inner_func__ = arg
      else:
        self.__positional_args__.append(arg)

  def _getArgs(self) -> list:
    """Returns the positional arguments"""
    return [*self.__positional_args__, ]

  def _getKwargs(self) -> dict:
    """Returns the keyword arguments"""
    return dict(**self.__keyword_args__)

  def getType(self, ) -> tuple[type]:
    """Getter-function for the type"""
    types = (
      type(self.__get__),
      type(self._preInitFactory),
      type(lambda: None),
    )
    return (*[type_ for type_ in types if isinstance(type_, type)],)

  def __get__(self, instance: Any, owner: type, **kwargs) -> Callable:
    """Descriptor protocol"""
    if self.__inner_func__ is None:
      raise AttributeError('No function has been assigned to the CallField')
    innerName = getattr(self.__inner_func__, '__name__', )
    innerAnnotations = getattr(self.__inner_func__, '__annotations__', )
    args0 = self._getArgs()
    kwargs0 = self._getKwargs()
    if instance is None:
      def callMeMaybe(*args1, **kwargs1) -> Any:
        """Unbounded version of the function returned when accessed
        through the class."""
        args = [*args0, *args1]
        kwargs_ = dict(**kwargs0, **kwargs1)
        return self.__inner_func__(*args, **kwargs_)
    else:
      def callMeMaybe(*args1, **kwargs1) -> Any:
        """Bounded version of the function returned when accessed
        through the instance."""
        args = [*args0, *args1]
        kwargs_ = dict(**kwargs0, **kwargs1)
        return self.__inner_func__(instance, *args, **kwargs_)

    setattr(callMeMaybe, '__name__', innerName)
    setattr(callMeMaybe, '__annotations__', innerAnnotations)
    return callMeMaybe

  def __set__(self, instance: Any, value: Callable) -> None:
    """Descriptor protocol"""
    if not callable(value):
      e = typeMsg('value', value, Callable)
      raise TypeError(e)
    if self.__inner_func__ is not None:
      e = """The CallField has already been assigned a function. This 
      operation is not allowed."""
      raise AttributeError(monoSpace(e))
    self.__inner_func__ = value

  def __delete__(self, instance: Any) -> Never:
    """Illegal deleter function"""
    e = """The CallField is protected from deletion"""
    raise TypeError(e)
