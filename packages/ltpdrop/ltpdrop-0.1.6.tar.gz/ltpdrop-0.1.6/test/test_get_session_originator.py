import unittest

def get_session_originator(data):
    value = 0
    for byte in data[1:]:  # Skip the first element
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            break
    return value


class TestGetSessionOriginator(unittest.TestCase):
    def test_get_session_originator(self):
        # Test with a segment where the second byte is 0x80
        segment = bytearray([0x00, 0x81, 0x00])
        self.assertEqual(get_session_originator(segment), 128 )

        # Test with a segment where the second byte is 0x01
        segment = bytearray([0x00, 0x01])
        self.assertEqual(get_session_originator(segment), 1)

        # Test with a segment where the second byte is 0xFF
        segment = bytearray([0x00, 0xFF, 0x01])
        self.assertEqual(get_session_originator(segment), 16257)

        segment = bytearray([0x00, 0x02, 0x81, 0xd9, 0xdb, 0xa2, 0x53, 0x00])
        self.assertEqual(get_session_originator(segment), 2)

if __name__ == '__main__':
    unittest.main()