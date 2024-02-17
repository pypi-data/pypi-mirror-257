""" Report class """
import os
import time

import xlsxwriter

from .col import ReportDataType
from .format import ReportFormat
from .page import ReportPage


class Report:
  """
  Report definition
  ---
  Attributes
    - name : Report name. The exported name will have an timestamp to prevent duplicity in our servers.
    - pages : List of pages to append into report
    - export_format : Format to export the report
  """

  def __init__(
    self,
    name: str,
    pages: list[ReportPage],
    export_format: ReportFormat,
  ) -> None:
    self.name = name
    self.pages = pages
    self.export_format = export_format

  @property
  def filename(self) -> str:
    """ Report filename """
    return f'{self.name}_{int(time.time() * 1000)}.xlsx'

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'Report(name={self.name}, pages={self.pages}, export_format={self.export_format})'

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def export(self, path, export_format: ReportFormat = None) -> str:
    """ Export report to file """
    if export_format:
      if export_format == ReportFormat.MICROSOFT_EXCEL:
        return self._export_xlsx(path)
      elif export_format == ReportFormat.JSON:
        return self._export_json()
      else:
        raise AttributeError(f'Unsupported export format: {export_format}')

    if self.export_format == ReportFormat.MICROSOFT_EXCEL:
      return self._export_xlsx(path)
    elif self.export_format == ReportFormat.JSON:
      return self._export_json()
    else:
      raise AttributeError(f'Unsupported export format: {self.export_format}')

  def export_as_json(self) -> dict:
    """ Returns the report as a JSON dict"""
    return self._export_json()

  def _export_json(self) -> dict:
    """ Returns a JSON dict of the report"""
    json_pages = []
    for page in self.pages:
      headers = []
      for header in page.headers:
        headers.append({
          'content': header.content,
          'text_color': header.text_color,
          'color': header.color,
        })
      rows = []
      for row in page.rows:
        cells = []
        for cell in row.content:
          cells.append({
            'content': cell.content,
            'text_color': cell.text_color,
            'color': cell.color,
            'data_type': cell.data_type.value,
          })
        rows.append({
          'content': cells,
          'compact': row.compact,
        })
      json_pages.append({
        'name': page.name,
        'headers': headers,
        'rows': rows,
      })

    return {
      'name': self.name,
      'pages': json_pages,
    }

  def _export_xlsx(self, path) -> str:
    """ Export to Microsoft Excel (.xslx) """

    full_path = os.path.join(path, self.filename)
    book = xlsxwriter.Workbook(full_path)

    for page in self.pages:
      sheet = book.add_worksheet(page.name[0:31].replace('[', '').replace(']', ''))
      if page.freeze_header:
        sheet.freeze_panes(1, 0)

      for i, header in enumerate(page.headers):
        style = book.add_format({
          'align': header.align.value,
          'font_color': header.text_color,
          'bg_color': header.color,
          'valign': 'vcenter',
          'font_size': 14,
          'top': 1,
          'left': 1,
          'right': 1,
          'bottom': 1,
          'font_name': 'Microsoft YaHei Light'
        })
        sheet.write(0, i, header.content, style)
        sheet.set_column(i, i, header.width)

      for i, row in enumerate(page.rows):
        for j, cell in enumerate(row.content):
          style = {
            'align': cell.align.value,
            'font_color': cell.text_color,
            'bg_color': cell.color,
            'bold': cell.bold,
            'valign': 'vcenter',
            'font_size': 10,
            'top': 1,
            'left': 1,
            'right': 1,
            'bottom': 1,
            'font_name': 'Microsoft YaHei Light'
          }

          if cell.data_type == ReportDataType.BOOL:
            value = 'Yes' if cell.value else 'No'
          elif cell.data_type == ReportDataType.DATETIME:
            value = cell.content.strftime(cell.datetime_format)
          elif cell.data_type == ReportDataType.INT:
            value = int(cell.content)
          elif cell.data_type == ReportDataType.FLOAT:
            value = float(cell.content)
            style.update({'num_format': '0.00'})
          elif cell.data_type == ReportDataType.CURRENCY:
            value = float(cell.content)
            style.update(
              {'num_format': f'"{cell.currency_symbol}" * #,##0.00;[Red]"{cell.currency_symbol}" * #,##0.00'})
          else:
            value = cell.content

          sheet.write(i + 1, j, value, book.add_format(style))

          if row.compact:
            sheet.set_row(i + 1, None, None, {'level': 1, 'hidden': True})
          else:
            sheet.set_row(i + 1, None, None, {'collapsed': True})
    book.close()

    return full_path
