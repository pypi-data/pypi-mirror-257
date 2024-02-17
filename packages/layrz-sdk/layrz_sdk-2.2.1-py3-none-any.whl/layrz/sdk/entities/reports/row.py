""" Report row """

from .col import ReportCol


class ReportRow:
  """
  Report row definition

  Available attributes
  --------------------
    content (list(ReportCol)): Cols to display
    height (float): Height of the cell, in points (pt)
    compact (bool): Compact mode
  """

  def __init__(
    self,
    content: list[ReportCol],
    height: float = 14,
    compact: bool = False,
  ) -> None:
    """ Constructor """
    self.content = content
    self.height = height
    self.compact = compact

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'ReportRow(content={self.content}, height={self.height}, compact={self.compact})'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
