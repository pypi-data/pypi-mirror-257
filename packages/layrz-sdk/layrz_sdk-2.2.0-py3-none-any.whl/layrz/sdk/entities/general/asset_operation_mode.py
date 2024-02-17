""" Asset Operation Mode """
from enum import Enum


class AssetOperationMode(Enum):
  """
  Asset Operation mode definition
  It's an enum of the operation mode of the asset.
  """
  SINGLE = 'SINGLE'
  MULTIPLE = 'MULTIPLE'
  ASSETMULTIPLE = 'ASSETMULTIPLE'
  DISCONNECTED = 'DISCONNECTED'
  FAILOVER = 'FAILOVER'

  @property
  def _readable(self) -> str:
    """ Readable """
    return self.value

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
