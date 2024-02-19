from __future__ import annotations
from typing import TYPE_CHECKING
import unittest

# pylint:disable=g-import-not-at-top
if TYPE_CHECKING:
  from ui_automator import ui_automator

# TODO(b/318771536): Check if a device is commissioned on GHA.
_commissioned: bool = False


class CommissionRegTest(unittest.TestCase):
  """Test class for running commission regression test."""

  def __init__(
      self,
      ui_automator: ui_automator.UIAutomator,
      test_name: str,
      device_name: str | None,
      pairing_code: str | None = None,
      gha_room: str | None = None,
  ) -> None:
    super().__init__(methodName=test_name)
    self.ui_automator = ui_automator
    self.device_name = device_name
    self.pairing_code = pairing_code
    self.gha_room = gha_room

  def test_commission(self) -> None:
    global _commissioned
    _commissioned = False
    self.ui_automator.commission_device(
        self.device_name, self.pairing_code, self.gha_room
    )
    # TODO(b/318771536): Check if a device is commissioned on GHA.
    _commissioned = True

  def test_decommission(self) -> None:
    if not _commissioned:
      self.skipTest('Device was not commissioned.')

    self.ui_automator.decommission_device(self.device_name)
