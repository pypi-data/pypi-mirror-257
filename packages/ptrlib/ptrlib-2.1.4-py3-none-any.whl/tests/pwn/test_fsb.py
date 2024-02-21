import unittest
import os
from ptrlib import Process, fsb
from logging import getLogger, FATAL

_is_windows = os.name == 'nt'


class TestFSB(unittest.TestCase):
    def setUp(self):
        getLogger("ptrlib").setLevel(FATAL)
        if _is_windows:
            # TODO: Implement test for Windows
            self.skipTest("This test has not been implemented for Windows yet")

    def test_fsb32(self):
        # test 1
        result = True
        for i in range(3):
            p = Process("./tests/test.bin/test_fsb.x86")
            p.recvuntil(": ")
            target = int(p.recvline(), 16)
            payload = fsb(
                pos = 4,
                writes = {target: 0xdeadbeef},
                bs = 1,
                bits = 32
            )
            p.sendline(payload + b'XXXXXXXX')
            p.recvuntil("XXXXXXXX\n")
            result |= b'OK' in p.recvline()
            p.close()
        self.assertEqual(result, True)

        # test 2
        result = True
        for i in range(3):
            p = Process("./tests/test.bin/test_fsb.x86")
            p.recvuntil(": ")
            target = int(p.recvline(), 16)
            payload = fsb(
                pos = 4,
                writes = {target: 0xdeadbeef},
                bs = 1,
                bits = 32,
                rear = True
            )
            p.sendline(payload + b'XXXXXXXX')
            p.recvuntil("XXXXXXXX\n")
            result |= b'OK' in p.recvline()
            p.close()
        self.assertEqual(result, True)

    def test_fsb64(self):
        # test 3
        result = True
        for i in range(3):
            p = Process("./tests/test.bin/test_fsb.x64")
            p.recvuntil(": ")
            target = int(p.recvline(), 16)
            payload = fsb(
                pos = 6,
                writes = {target: 0xdeadbeef},
                bs = 1,
                bits = 64
            )
            p.sendline(payload)
            result |= b'OK' in p.recvuntil("OK")
            p.close()
        self.assertEqual(result, True)
