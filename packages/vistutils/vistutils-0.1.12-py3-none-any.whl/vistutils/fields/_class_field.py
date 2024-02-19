"""TypedField requires a strongly typed field."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable, Never

from vistutils.waitaminute import typeMsg

from vistutils.fields import AbstractField


class ClassField(AbstractField):
  """TypedField requires a strongly typed field."""

  def GET(self, callMeMaybe: Callable) -> Callable:
    """Decorates the intended getter function. The class body does not
    have access to the __get__ until after class creation time."""
    setattr(self, '__creator_function__', callMeMaybe)
    return callMeMaybe

  def __instantiate_inner_class__(self, instance: Any, owner: type) -> None:
    """Instantiates the inner class. """
    args, kwargs = self._getArgs(), self._getKwargs()
    creator = self._getCreatorFunction()
    pvtName = self._getPrivateName()
    innerInstance = creator(instance, owner, *args, **kwargs)
    setattr(instance, pvtName, innerInstance)

  def _getCreatorFunction(self) -> Callable:
    """Getter-function for creator function. Defaults to calling the inner
    class itself"""
    if self.__creator_function__ is None:
      def creator(*args, **kwargs) -> Any:
        """Fallback creator calling the function itself"""
        args, kwargs = self._getArgs(), self._getKwargs()
        innerClass = self._getInnerClass()
        return innerClass(*args, **kwargs)

      return creator
    if callable(self.__creator_function__):
      return self.__creator_function__
    e = typeMsg('__creator_function__', self.__creator_function__, Callable)
    raise TypeError(e)

  def _getInnerClass(self) -> type:
    """Getter-function for the inner-class"""
    return self.__inner_class__

  def __init__(self,
               innerClass: Any,
               *args, **kwargs) -> None:
    AbstractField.__init__(self, )
    self.__positional_arguments__ = [*args, ]
    self.__keyword_arguments__ = {**kwargs, }
    self.__inner_creator__ = None
    self.__inner_class__ = None
    self.__creator_function__ = None
    if innerClass is None:
      e = """Inner class must be specified explicitly!"""
      raise ValueError(e)
    if isinstance(innerClass, type):
      self.__inner_class__ = innerClass
    else:
      e = typeMsg('innerClass', innerClass, type)
      raise TypeError(e)
    if 'creator' in self.__keyword_arguments__:
      creator = self.__keyword_arguments__.get('creator')
      if callable(creator):
        self.__creator_function__ = creator
      else:
        e = typeMsg('__creator_function__', self.__creator_function__,
                    Callable)
        raise TypeError(e)

  def _getArgs(self) -> list:
    """Getter-function for the list containing the positional arguments
    given to the constructor. """
    return self.__positional_arguments__

  def _getKwargs(self, ) -> dict:
    """Getter-function for the dictionary containing the keyword
    arguments given to the constructor. """
    return self.__keyword_arguments__

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """Getter-function implementation"""
    pvtName = self._getPrivateName()
    if instance is None:
      return self.__inner_class__
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    if kwargs.get('_recursion', False):
      raise RecursionError
    self.__instantiate_inner_class__(instance, owner)
    return self.__get__(instance, owner, _recursion=True)

  def __set__(self, instance: Any, value: Any) -> Never:
    """Not yet implemented!"""
    raise NotImplementedError

  def __delete__(self, instance: Any, ) -> Never:
    """Not yet implemented!"""
    raise NotImplementedError
