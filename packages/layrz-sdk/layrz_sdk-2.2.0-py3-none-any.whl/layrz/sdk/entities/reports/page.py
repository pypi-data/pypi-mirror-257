""" Report page """
from .header import ReportHeader
from .row import ReportRow


class ReportPage:
  """
  Report page definition
  ---
  Attributes
    - name : Name of the page. Length should be less than 60 characters
    - headers : Headers of the page
    - rows : Rows of the page
  """

  def __init__(
    self,
    name: str,
    headers: list[ReportHeader],
    rows: list[ReportRow],
    freeze_header: bool = False,
  ) -> None:
    self.name = name
    self.headers = headers
    self.rows = rows
    self.freeze_header = freeze_header

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'ReportPage(name={self.name}, headers={self.headers}, rows={self.rows})'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
