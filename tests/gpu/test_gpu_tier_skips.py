# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import pytest

pytestmark = pytest.mark.gpu


def test_gl_context_is_available(qapp):
    """Sanity check that the gpu tier runs only with a real GL context."""
    from conftest import gl_available

    assert gl_available()
