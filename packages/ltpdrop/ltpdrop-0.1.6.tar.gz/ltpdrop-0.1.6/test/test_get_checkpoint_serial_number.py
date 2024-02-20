import unittest

def get_checkpoint_serial_number(data):
    """This function returns the checkpoint serial number of the segment, it takes as input an unanalyzed segment"""
    # Initialize the index at the start of the 2nd field
    index = 1

    # Skip over the 2nd and 3rd fields session id and engine, then over extension count field and client service ID
    # and then over offset and length field
    for _ in range(4):
        while data[index] & 0x80:  # While the most significant bit is set
            index += 1
        index += 1 # Skip over the last byte of the field
        if _ == 1:
            index+=2 # Plus two is require to skip the extension count fields and the client service ID field
    value = 0
    for byte in data[index:]:  # index is at the start of the length field
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            break
    return value

class TestGetCheckpointSerialNumber(unittest.TestCase):
    def test_get_checkpoint_serial_number(self):
        # Test with a segment where the checkpoint serial number is 0x01
        hex_string = "0301030001d000590100"
        segment= bytes.fromhex(hex_string)
        self.assertEqual(get_checkpoint_serial_number(segment), 1)
        # Test with a segment with multiple byte session ID and multiple byte checkpoint serial number
        hex_string = "010281d9dba2530001008769e406d25f"
        segment= bytes.fromhex(hex_string)
        self.assertEqual(get_checkpoint_serial_number(segment), 12806)