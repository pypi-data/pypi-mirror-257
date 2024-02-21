"""Stream provides"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from io import TextIOWrapper
from typing import TextIO


class Stream(TextIOWrapper):
  """Stream is a wrapper for the TextIOWrapper class that captures the
  output."""

  def __init__(self, stream: TextIO) -> None:
    TextIOWrapper.__init__(self, stream.buffer, write_through=True)
    self.captureList = []

  def write(self, s) -> int:
    """Reimplementation of the write method to capture the output."""
    self.captureList.append(s)
    return TextIOWrapper.write(self, s)

  def read(self, n=-1) -> str:
    """Reimplementation of the read method to capture the output."""
    s = TextIOWrapper.read(self, n)
    self.captureList.append(s)
    return s

  def collect(self) -> list[str]:
    """Returns the captured output as a list of strings."""
    return self.captureList
