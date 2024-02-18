"""Utility to produce desired device."""
import logging

from mobly.controllers import android_device
from bttc.mobly_android_device_lib.services import sl4a_service

from snippet_uiautomator import uiautomator
from typing import TypeAlias, Union


GeneralDevice: TypeAlias = android_device.AndroidDevice


def get(
    ad: Union[GeneralDevice, str],
    init_mbs: bool = False,
    init_sl4a: bool = False,
    init_snippet_uiautomator: bool = False) -> GeneralDevice:
  """Produces desired device.

  Args:
    init_mbs: True to register service `snippets` in produced device.
    init_sl4a: True to register service `sl4a` in produced device.

  Returns:
    The produced device object.
  """
  device: GeneralDevice | None = None
  if isinstance(ad, str):
    device = android_device.create([{'serial': ad}])[0]
  else:
    device = ad

  if all([
      (init_mbs or init_snippet_uiautomator),
      'snippets' not in device.services.list_live_services()]):
    logging.info('Register service "mbs" in device=%s...', device)
    device.load_snippet(
        'mbs',
        'com.google.android.mobly.snippet.bundled')

  if init_sl4a and not device.services.has_service_by_name('sl4a'):
    logging.info('Registering service "sl4a" in device=%s...', device)
    device.services.register('sl4a', sl4a_service.Sl4aService)

  if all([
      init_snippet_uiautomator,
      'uiautomator' not in device.services.list_live_services()]):
    device.services.register(
        'uiautomator', uiautomator.UiAutomatorService)

  logging.info(
      '%s has registered service(s): %s',
      device, device.services.list_live_services())

  return device
