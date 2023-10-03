import serial
import unittest
import time
import typing

import pytest

from totalopenstation.models import Connector
from totalopenstation.models import zeiss_elta_r55


class TestModelSerialInputZeiss(unittest.TestCase):
    def setUp(self):
        with open(
            "sample_data/zeiss_elta_r55/zeiss_elta_r55-REC_500.tops",
            "rb",
            buffering=1
        ) as testdata:
            self.testdata = testdata.read() 
            print(len(self.testdata))

    @pytest.mark.parametrize(
             "baudrate", [ 4800, 9600, 19200, 38400 ]
    )
    def test_download(self, baudrate):
        conn = Connector("loop://", baudrate=baudrate)
        conn.ser.write(self.testdata)
        conn.download()
        assert conn.result == self.testdata


# class TestAutoSave(unittest.TestCase):
#     def test_autosave(self):
#         autosave_timestamp = int(time.time())
#         autosave_filename = f"autosave-{autosave_timestamp}.tops"

#         with open(autosave_filename, "ab") as autosave:
#             result = []  # type: typing.List[bytes]
#             while s.in_waiting > 0:
#                 line = s.readline()
#                 autosave.write(line)
#                 result.append(line)
#                 print(line)
