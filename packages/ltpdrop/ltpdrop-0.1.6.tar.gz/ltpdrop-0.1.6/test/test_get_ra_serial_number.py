import unittest

def get_ra_serial_number(data):
    """This function returns the RA serial number of the segment, it takes as input an unanalyzed segment"""
    # Initialize the index at the start of the 2nd field
    index = 1

    # Skip over the 2nd and 3rd fields session id and engine
    for _ in range(2):
        while data[index] & 0x80:  # While the most significant bit is set
            index += 1
        index += 1  # Skip over the last byte of the field
    index+=1 # Plus 1 is required to skip the extension count field
    value = 0
    for byte in data[index:]:  # index is at the start of the offset field
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            break
    return value

class TestGetRSSerialNumber(unittest.TestCase):
    def test_get_checkpoint_serial_number(self):
        # Tes
        hex_string = "090103008817"
        segment= bytes.fromhex(hex_string)
        self.assertEqual(get_ra_serial_number(segment), 1047)
        # Test with a segment where the  serial number is 0xd25f
        hex_string = "090281d9dba25300d25f"
        segment= bytes.fromhex(hex_string)
        self.assertEqual(get_ra_serial_number(segment), 10591)
       