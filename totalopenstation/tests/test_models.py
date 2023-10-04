import serial
import time
import typing

import pytest

from totalopenstation.models import Connector
from totalopenstation.models import zeiss_elta_r55

@pytest.fixture
def zeiss_data():
    with open(
            "sample_data/zeiss_elta_r55/zeiss_elta_r55-REC_500.tops",
            "rb",
            buffering=0
        ) as testdata:
        return testdata.read() 

@pytest.mark.parametrize("baudrate", [ (4800), (9600), (19200), (38400) ])
def test_download(zeiss_data, baudrate): # noqa
        conn = Connector("loop://", baudrate=baudrate) # noqa
        conn.ser.write(zeiss_data)
        conn.download()
        assert conn.result == zeiss_data


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
