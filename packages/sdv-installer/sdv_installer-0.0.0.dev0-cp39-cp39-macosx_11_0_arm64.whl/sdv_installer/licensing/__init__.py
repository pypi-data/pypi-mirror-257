"""Licensing module."""

from sdv_installer.licensing.authentication import (
    authenticate, authenticate_license_key, read_license_key)

__all__ = (
    'authenticate',
    'authenticate_license_key',
    'read_license_key'
)
