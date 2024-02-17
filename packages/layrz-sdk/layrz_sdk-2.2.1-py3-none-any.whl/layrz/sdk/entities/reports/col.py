""" Report col """
from enum import Enum
from typing import Any

from ..formatting.text_align import TextAlignment


class ReportDataType(Enum):
  """
  Report date type
  """
  STR = 'str'
  INT = 'int'
  FLOAT = 'float'
  DATETIME = 'datetime'
  BOOL = 'bool'
  CURRENCY = 'currency'

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'ReportDataType.{self.value}'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable


class ReportCol:
  """
  Report col definition
  ---
  Attributes
    - content : Display content
    - color : Cell color
    - text_color : Text color
    - align : Text Alignment
    - data_type : Data type
    - datetime_format : Date time format
    - currency_symbol : Currency symbol
  """

  def __init__(
    self,
    content: Any,
    color: str = '#ffffff',
    text_color: str = '#000000',
    align: TextAlignment = TextAlignment.LEFT,
    data_type: ReportDataType = ReportDataType.STR,
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
    currency_symbol: str = '',
    bold: bool = False,
  ) -> None:
    self.content = content
    self.color = color
    self.text_color = text_color
    self.align = align
    self.data_type = data_type
    self.datetime_format = datetime_format
    self.currency_symbol = currency_symbol
    self.bold = bold

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'ReportCol(content={self.content}, color={self.color}, text_color={self.text_color}, '+\
           f'align={self.align}, data_type={self.data_type}, datetime_format={self.datetime_format}, ' +\
           f'currency_symbol={self.currency_symbol}, bold={self.bold})'

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable

  def __str__(self) -> str:
    """ Readable property """
    return self._readable
