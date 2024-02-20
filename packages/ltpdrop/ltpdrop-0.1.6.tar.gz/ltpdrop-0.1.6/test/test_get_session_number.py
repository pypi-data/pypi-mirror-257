import unittest


def get_session_number(data):

    # Initialize the index at the start of the first byte
    index = 1

    # Skip over the 2nd field session originator engine
    for _ in range(1):
        while data[index] & 0x80:  # While the most significant bit is set
            index += 1
        index += 1  # Skip over the last byte of the field

    # 
    value = 0
    for byte in data[index:]:  # Start from the end of the session originator engine
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            break
    return value

class GetSessionNumberTest(unittest.TestCase):

    def test_get_session_number(self):

        # Test case 1: single byte session number
        data2 = [0x00,0x01,0x03,0x00]  # 0x81 = 10000001, 0x7F = 01111111
        self.assertEqual(get_session_number(data2), 3)
        
        # Test case 2: data with multi byte session number
        data1 = [0x00, 0x02, 0x81, 0xd9, 0xdb, 0xa2, 0x53, 0x00]
        self.assertEqual(get_session_number(data1), 456577363)

        # Test case 3: multi byte session originator, single byte session number
        data3 = [0x80, 0x81, 0x00, 0x70] 
        self.assertEqual(get_session_number(data3), 112)

        # Test case 4: multi byte session originator, multi byte session number
        data4 = [0xFF, 0x8F, 0x70, 0x81, 0x00] 
        self.assertEqual(get_session_number(data4), 128)

if __name__ == '__main__':
    unittest.main()