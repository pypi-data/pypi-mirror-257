"""Dream provides customizable encapsulation of the standard output
stream. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from enum import Flag
from typing import Callable, Any, Self

from vistutils.dirs import Stream, getProjectRoot
from vistutils.fields import TypedField, AbstractField, CallField
from vistutils.parse import maybe


class RunStatus(Flag):
  """RunStatus provides flags for the status of the main function"""
  WAITING = 0
  RETURNED = 1

  def __bool__(self, ) -> bool:
    return True if self is RunStatus.RETURNED else False


class DO(AbstractField):
  """Provides a field that returns the owner after a function has been
  applied to it."""

  def __init__(self, setName: str = None) -> None:
    AbstractField.__init__(self, )
    self.__set_name__ = setName
    self.__field_owner__ = None
    self.__field_name__ = None

  def __prepare_owner__(self, owner: type) -> type:
    """Implementation of the abstract method"""
    if not hasattr(owner, '_latestDo'):
      setattr(owner, '_latestDo', self)
    return owner

  def __get__(self, instance: Any, owner: type) -> Any:
    return self.__field_owner__

  def __set__(self, instance: Any, value: Any) -> Any:
    if self.__set_name__ is not None:
      setattr(self.__field_owner__, self.__set_name__, value)
    return self.__field_owner__


class Dream:
  """Dream provides customizable encapsulation of the standard output
  stream. """
  strIn = Stream(sys.stdin, )
  strOut = Stream(sys.stdout, )
  strErr = Stream(sys.stderr, )

  __default_log_dir__ = None
  __in_log_path__ = os.path.join(getProjectRoot(), 'latest_in.log')
  __out_log_path__ = os.path.join(getProjectRoot(), 'latest_out.log')
  __err_log_path__ = os.path.join(getProjectRoot(), 'latest_err.log')

  mainFunc = CallField(supportInit=True)
  inLogFile = TypedField(str, __in_log_path__)
  outLogFile = TypedField(str, __out_log_path__)
  errLogFile = TypedField(str, __err_log_path__)
  _recursionFlag = TypedField(bool, False)

  IN = DO('inLogFile')
  OUT = DO('outLogFile')
  ERR = DO('errLogFile')

  def __init__(self, mainFunc: Callable, *args, **kwargs) -> None:
    self.__main_function__ = mainFunc
    setattr(mainFunc, '__run_status__', RunStatus.WAITING)
    self.__out_lines__ = []
    self.__err_lines__ = []
    self.__in_lines__ = []
    self.__return_value__ = type('Awaiting', (), {'__name__': 'Awaiting'})
    self.__positional_args__ = [*args, ]
    self.__keyword_args__ = dict(**kwargs, )

  def _getArgs(self) -> list:
    """Returns the positional arguments"""
    return [*self.__positional_args__, ]

  def _getKwargs(self) -> dict:
    """Returns the keyword arguments"""
    return dict(**self.__keyword_args__)

  def dispatchMain(self, ) -> None:
    """Dispatches the main function"""
    args, kwargs = self._getArgs(), self._getKwargs()
    self.__return_value__ = self.__main_function__(*args, **kwargs)
    setattr(self.__main_function__, '__run_status__', RunStatus.RETURNED)

  def _defaultLogDir(self, ) -> str:
    """Getter-function for the default log directory"""
    if self.__default_log_dir__ is None:
      return getProjectRoot()
    if os.path.isabs(self.__default_log_dir__):
      return self.__default_log_dir__
    e = """The default log directory must be defined absolutely."""
    raise NotADirectoryError(e)

  def _outLogPath(self, **kwargs) -> str:
    """Getter-function for the out log path"""
    if os.path.isabs(self.outLogFile):
      return self.outLogFile
    if kwargs.get('_recursion', False):
      raise RecursionError
    self.outLogFile = os.path.join(self._defaultLogDir(), self.outLogFile)
    return self._outLogPath(_recursion=True)

  def _inLogPath(self, **kwargs) -> str:
    """Getter-function for the in log path"""
    if os.path.isabs(self.inLogFile):
      return self.inLogFile
    if kwargs.get('_recursion', False):
      raise RecursionError
    self.inLogFile = os.path.join(self._defaultLogDir(), self.inLogFile)
    return self._inLogPath(_recursion=True)

  def _errLogPath(self, **kwargs) -> str:
    """Getter-function for the err log path"""
    if os.path.isabs(self.errLogFile):
      return self.errLogFile
    if kwargs.get('_recursion', False):
      raise RecursionError
    self.errLogFile = os.path.join(self._defaultLogDir(), self.errLogFile)
    return self._errLogPath(_recursion=True)

  def __enter__(self) -> Self:
    sys.stdin = self.strIn
    sys.stdout = self.strOut
    sys.stderr = self.strErr
    return self

  def __exit__(self, exc_type, exc_value, traceback) -> None:
    errors = []
    try:
      self.dispatchMain()
    except Exception as exception:
      if exc_type is None:
        raise exception
      raise exc_type from exception
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    with open(self._inLogPath(), 'w') as f:
      f.writelines(self.strIn.collect())
    with open(self._outLogPath(), 'w') as f:
      f.writelines(self.strOut.collect())
    with open(self._errLogPath(), 'w') as f:
      f.writelines(self.strErr.collect())

  def __matmul__(self, environment: Any) -> Any:
    """Applies environment to the main function"""
    if isinstance(environment, dict):
      for key, value in environment.items():
        os.environ[key] = str(value).strip()
      self._recursionFlag = False
      return self
    if isinstance(environment, str):
      if os.path.isfile(environment):
        data = {}
        with open(environment, 'r') as f:
          for line in f:
            if line.strip():
              if line[0] != '#' and len([c for c in line if c == '=']) == 1:
                key, value = line.split('=')
                data[key] = value
        if self._recursionFlag:
          raise RecursionError
        self._recursionFlag = True
        return self @ data
      if self._recursionFlag:
        raise FileNotFoundError(environment)
      self._recursionFlag = True
      return self @ os.path.join(self._defaultLogDir(), environment)
