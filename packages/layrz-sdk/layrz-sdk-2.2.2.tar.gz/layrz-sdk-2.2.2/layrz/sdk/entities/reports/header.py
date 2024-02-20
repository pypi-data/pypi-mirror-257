""" Report header """
from ..formatting.text_align import TextAlignment


class ReportHeader:
  """
  Report header definition
  ---
  Attributes
    - content : Display name
    - width : Column width in points (pt)
    - color : Cell color
    - text_color : Text color
    - align : Text Alignment
  """

  def __init__(
    self,
    content: str,
    width: int = 10,
    color: str = '#ffffff',
    text_color: str = '#000000',
    align: TextAlignment = TextAlignment.CENTER,
  ) -> None:
    self.content = content
    self.width = width
    self.color = color
    self.text_color = text_color
    self.align = align

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'ReportHeader(content={self.content}, width={self.width}, color={self.color}, ' +\
           f'text_color={self.text_color}, align={self.align})'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
