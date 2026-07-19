#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: wild_t1000.py
# Copyright 2026 Carlo Pavan <carlopava@gmail.com>

# This file is part of Total Open Station.

# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.


from . import Connector

PROCEED = b'?\r\n'


def is_data_block(line):
    '''True if a received line is a GSI block rather than protocol chatter.

    GSI words start with a numeric word index (GSI-8) or ``*`` (GSI-16), while
    the status line and any echo of our own request are short and do not.
    '''

    stripped = line.strip()
    return len(stripped) > 4 and (stripped[:1].isdigit()
                                  or stripped[:1] == b'*')


def collect_wild_t1000_data(port, initial_timeout=60.0, record_timeout=5.0):
    '''Download GSI records from a Wild T1000.

    The instrument sends one record at a time and then waits. Each record is
    two CRLF-terminated lines: the GSI data block, followed by a short status
    line (observed as ``w``) which is not part of the data. The receiver asks
    for the next record by sending ``?``. This mirrors the BASIC listing in
    the instrument manual::

        50 LINE INPUT #1,A$
        60 LINE INPUT #1,B$
        80 PRINT #2,A$
        90 PRINT #1,"?"
        100 GOTO 50

    Handshaking is purely in-band: the manual's ``CS,DS,CD`` open options
    disable waiting on the modem control lines, so no RTS/CTS or DSR/DTR
    flow control is used.

    What comes down the wire is sparser than a modern GSI file. The
    instrument sends only the point number and the raw polar observation:

        11 point number, 21 horizontal angle, 22 zenith angle,
        31 slope distance, 32 horizontal distance, plus a leading 41 code
        block

    There is no station record and no reflector or instrument height, so
    WI 84-88 and the computed coordinates 81-83 are all absent. The GSI
    parser recognises this word index set as an old-style file and defaults
    the missing values to zero (see issue #168), which means heights come out
    relative to the line of sight and coordinates sit in a local frame
    centred on the station. That is a limit of what the T1000 transmits, not
    of the parsing: the missing values have to be supplied by hand afterwards.

    Args:
        port: an open serial-like object.
        initial_timeout: seconds to wait for the first record, i.e. how long
            the user has to start the transfer on the instrument.
        record_timeout: seconds to wait for each subsequent record before
            deciding the transfer has finished.

    Returns:
        bytes: the concatenated GSI data blocks, CRLF-terminated.
    '''

    records = []
    previous_timeout = port.timeout

    # Anything already buffered is stale: a leftover echo here would shift the
    # data lines onto the status lines for the whole transfer.
    port.reset_input_buffer()

    try:
        port.timeout = initial_timeout
        while True:
            line = port.readline()
            if not line:
                # Timed out: the instrument has nothing more to send.
                break

            if not is_data_block(line):
                # Status line ("w"), echo of our own "?", or blank. Skip it
                # rather than pairing lines positionally, so a stray byte
                # cannot misalign the rest of the transfer.
                continue

            records.append(line)
            port.write(PROCEED)
            port.flush()
            port.timeout = record_timeout

    finally:
        port.timeout = previous_timeout

    return b''.join(records)


class ModelConnector(Connector):

    def __init__(self, port):
        # Wild T1000 uses 2400 baud, 7 data bits, even parity, 2 stop bits
        Connector.__init__(self, port=port, baudrate=2400, bytesize=7,
                           parity='E', stopbits=2)

    def download(self):
        '''Download using the Wild T1000 request/response protocol.'''

        self.result = collect_wild_t1000_data(self)

    def fast_download(self):
        # The T1000 transfer is driven by us, so there is nothing to wait for
        # beyond the first record, which collect_wild_t1000_data handles.
        self.dl_started.set()
        self.download()
        self.dl_finished.set()
