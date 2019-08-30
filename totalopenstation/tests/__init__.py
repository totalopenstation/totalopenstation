import importlib

import pytest

from totalopenstation.output import BUILTIN_OUTPUT_FORMATS


class BaseTestOutput:
    '''This base class is inherited by all output test modules.

    pytest will not run the test here because the class name does not
    start with "test".

    Child classes must implement a setup fixture, marked as @pytest.fixture.
    '''

    @pytest.mark.parametrize(
        'output_format', [ of for of in BUILTIN_OUTPUT_FORMATS ]
    )
    def test_output_format(self, output_format, setup):
        tup = BUILTIN_OUTPUT_FORMATS[output_format]
        mod, cls, name = tup
        outputclass = getattr(importlib.import_module('totalopenstation.output.' + mod), cls)
        assert outputclass(self.fp.points).process()
