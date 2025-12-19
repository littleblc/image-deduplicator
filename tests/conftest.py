"""Pytest configuration and shared fixtures."""

import pytest
from hypothesis import settings, Verbosity

# Configure hypothesis for property-based testing
# Run at least 100 iterations as specified in the design document
settings.register_profile("default", max_examples=100, verbosity=Verbosity.normal)
settings.load_profile("default")
