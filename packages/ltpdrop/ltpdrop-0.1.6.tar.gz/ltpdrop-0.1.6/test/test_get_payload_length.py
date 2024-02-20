import unittest

def get_payload_length(data):

    # Initialize the index at the start of the 2nd field
    index = 1

    # Skip over the 2nd and 3rd fields session id and engine, then over extension count field and client service ID
    # and then over offset field
    for _ in range(3):
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

class TestGetPayloadLength(unittest.TestCase):
    def test_get_payload_length(self):
        
        # Test case 1: session id requires 2 bytes, offset 1 byte long, length 1 byte long
        data = bytearray([0x01, 0x01, 0x02, 0x00, 0x01,0x00,0x07])
        self.assertEqual(get_payload_length(data), 7)

        # Test case 2: session id require more than 2 bytes, offset 1 bytes long, length 1 byte long
        data = bytearray([0x01, 0x02,0x81,0xd9,0xdb, 0xa2, 0x53,0x00, 0x01,0x00,0x53])
        self.assertEqual(get_payload_length(data), 83)
        
        # Test case 3: session id requires 2 bytes, offset more 2 byte long, length 1 byte long
        data = bytearray([0x01, 0x01, 0x02, 0x00, 0x01,0x81,0x00,0x77])
        self.assertEqual(get_payload_length(data), 119)
        
        # Test case 4: session id requires 2 bytes, offset more 2 byte long, length 2 byte long
        data = bytearray([0x01, 0x01, 0x02, 0x00, 0x01,0x81,0x00,0x81,0x00])
        self.assertEqual(get_payload_length(data), 128)

        # Test case 5: session id require more than 2 bytes, offset 2 bytes long
        data = bytearray([0x01, 0x02,0x81,0xd9,0xdb, 0xa2, 0x53, 0x00,0x01,0x81,0x00, 0x88,0x00])
if __name__ == '__main__':
    unittest.main()