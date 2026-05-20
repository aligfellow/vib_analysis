"""Smoke tests for graphrc API."""

import numpy as np
import pytest

from graphrc import __citation__, __version__
from graphrc.convert import _make_amplitudes, validate_n_frames


def test_version():
    """Version is defined."""
    assert __version__


def test_citation():
    """Citation contains package name."""
    assert "graphRC" in __citation__


def test_make_amplitudes_default():
    """The 20-frame default reproduces the original hardcoded amplitude list."""
    expected = [
        0.0, -0.2, -0.4, -0.6, -0.8, -1.0, -0.8, -0.6, -0.4, -0.2,
        0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2,
    ]  # fmt: skip
    assert np.allclose(_make_amplitudes(20), expected)
    assert len(_make_amplitudes(40)) == 40


def test_validate_n_frames():
    """n_frames must be a positive multiple of 4."""
    assert validate_n_frames(20) == 20
    for bad in (0, 7, -4):
        with pytest.raises(ValueError, match="multiple of 4"):
            validate_n_frames(bad)
