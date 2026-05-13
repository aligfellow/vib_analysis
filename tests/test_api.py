"""Smoke tests for graphrc API."""

from pathlib import Path

import numpy as np
import pytest

from graphrc import __citation__, __version__
from graphrc.api import load_trajectory
from graphrc.convert import _make_amplitudes

DATA_DIR = Path(__file__).parent.parent / "examples" / "data"
TEST_FILE = str(DATA_DIR / "sn2.v000.xyz")


def test_version():
    """Version is defined."""
    assert __version__


def test_citation():
    """Citation contains package name."""
    assert "graphRC" in __citation__


def test_make_amplitudes_default():
    """Default 20-frame sequence matches the original hardcoded list."""
    expected = [
        0.0,
        -0.2,
        -0.4,
        -0.6,
        -0.8,
        -1.0,
        -0.8,
        -0.6,
        -0.4,
        -0.2,
        0.0,
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        0.8,
        0.6,
        0.4,
        0.2,
    ]
    assert np.allclose(_make_amplitudes(20), expected)


@pytest.mark.parametrize("n", [8, 20, 40, 100])
def test_make_amplitudes_shape_and_range(n):
    """Amplitudes cover [-1, 1], start and midpoint at 0, and have the right length."""
    a = _make_amplitudes(n)
    assert len(a) == n
    assert np.isclose(a[0], 0.0)
    assert np.isclose(a[n // 2], 0.0)
    assert np.isclose(a.min(), -1.0)
    assert np.isclose(a.max(), 1.0)


@pytest.mark.parametrize("n", [-5, -1, 0, 1, 2, 3])
def test_make_amplitudes_invalid(n):
    """n_frames below 4 raises ValueError."""
    with pytest.raises(ValueError, match="at least 4"):
        _make_amplitudes(n)


@pytest.mark.parametrize("n", [9, 11])
def test_make_amplitudes_odd_rounds_up(n):
    """Odd n_frames is rounded up to even with a warning."""
    with pytest.warns(UserWarning, match=str(n)):
        a = _make_amplitudes(n)
    assert len(a) == n + 1
    assert np.isclose(a[0], 0.0)
    assert np.isclose(a[(n + 1) // 2], 0.0)
    assert np.isclose(a.min(), -1.0)
    assert np.isclose(a.max(), 1.0)


def test_load_trajectory_xyz_ignores_n_frames():
    """XYZ input: frame count comes from the file, n_frames has no effect."""
    result_default = load_trajectory(TEST_FILE, save_to_disk=False)
    result_custom = load_trajectory(TEST_FILE, n_frames=40, save_to_disk=False)
    assert len(result_default["frames"]) == len(result_custom["frames"])
