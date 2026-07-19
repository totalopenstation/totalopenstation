import re
import unittest

from totalopenstation.formats.leica_gsi import FormatParser
from totalopenstation.models.wild_t1000 import collect_wild_t1000_data

# Recorded from a Wild T1000, so it carries only the word indexes the
# instrument actually sends (11, 21, 22, 31, 32) — see issue #168.
SAMPLE = 'sample_data/leica_gsi/RILIEVO.gsi'


class FakeT1000:
    '''A Wild T1000 replaying recorded GSI blocks.

    It sends one record per '?' request, each being a data block followed by
    a 'w' status line, and stops responding once the blocks run out.

    Args:
        blocks: the GSI data blocks to replay.
        stale: bytes already buffered when the download starts.
        echo: whether the link echoes our own request back at us.
    '''

    def __init__(self, blocks, stale=b'', echo=False):
        self.blocks = list(blocks)
        self.buf = bytearray(stale)
        self.echo = echo
        self.timeout = 1.0
        self.started = False

    def reset_input_buffer(self):
        self.buf.clear()

    def _emit(self):
        if self.blocks:
            self.buf.extend(self.blocks.pop(0) + b'\r\nw\r\n')

    def readline(self):
        if not self.started:
            self.started = True
            self._emit()
        idx = self.buf.find(b'\n')
        if idx == -1:
            return b''
        line, self.buf = bytes(self.buf[:idx + 1]), self.buf[idx + 1:]
        return line

    def write(self, data):
        assert data == b'?\r\n'
        if self.echo:
            self.buf.extend(b'?\r\n')
        self._emit()

    def flush(self):
        pass


class TestWildT1000Connector(unittest.TestCase):

    def setUp(self):
        # Recorded files terminate blocks with CR, LF or both, so split on
        # any run of them rather than assuming one flavour.
        with open(SAMPLE, 'rb') as testdata:
            lines = re.split(b'[\r\n]+', testdata.read())
        self.blocks = [line for line in lines if line.strip()]

    def download(self, **kwargs):
        return collect_wild_t1000_data(FakeT1000(self.blocks, **kwargs))

    def records(self, **kwargs):
        data = self.download(**kwargs)
        return [line for line in data.split(b'\r\n') if line.strip()]

    def test_all_records(self):
        self.assertEqual(self.records(), self.blocks)

    def test_status_lines_are_not_data(self):
        data = self.download()
        # Assert we got something first: 'w' is absent from an empty
        # download too, which would make this pass for the wrong reason.
        self.assertTrue(data)
        self.assertNotIn(b'w', data)

    def test_stale_byte_does_not_shift_records(self):
        # A leftover '?' used to shift every data line onto the discarded
        # status line, yielding a download of nothing but 'w'.
        self.assertEqual(self.records(stale=b'?\r\n'), self.blocks)

    def test_echoed_request_is_ignored(self):
        self.assertEqual(self.records(echo=True), self.blocks)

    def test_noisy_start(self):
        noise = b'\x00\r\nw\r\n?\r\n'
        self.assertEqual(self.records(stale=noise), self.blocks)

    def test_downloaded_data_is_parseable(self):
        # The download is only useful if the GSI parser accepts it, so cover
        # the seam between the two rather than each half alone. The expected
        # values match TestLeicaGSIOldParser, which reads the same file from
        # disk instead of over the wire.
        fp = FormatParser(self.download().decode('ascii'))
        self.assertEqual(len(fp.points), len(self.blocks))
        point = fp.points[2]
        self.assertEqual(point.id, 3)
        self.assertEqual(point.desc, 'PT')
        self.assertEqual(point.point_name, '102')
        self.assertAlmostEqual(point.geometry.x, 4.49963916)
        self.assertAlmostEqual(point.geometry.y, -2.51722711)
        self.assertAlmostEqual(point.geometry.z, -0.30665937)


if __name__ == '__main__':
    unittest.main()
