import unittest
from verify_hdr_fallback import verify_hdr_fallback, verify_hdr_fallback_on_file

class VerifyHdrFallbacktTest(unittest.TestCase):
    def test_good_case(self):
        with open("./ffprobe-good-example.txt", 'r') as file:
            file_content = file.read()
        result = verify_hdr_fallback(file_content)
        self.assertEqual(result, True)

    def test_bad_case(self):
        with open("./ffprobe-bad-example.txt", 'r') as file:
            file_content = file.read()
        result = verify_hdr_fallback(file_content)
        self.assertEqual(result, False)

    def test_good_file(self):
        "These tests will fail unless you copy in a file that does not have the color issue"
        filename = "./ffprobe-good-file.mkv"
        result = verify_hdr_fallback_on_file(filename)
        self.assertEqual(result, True)

    def test_bad_file(self):
        "These tests will fail unless you copy in a file that has the color issue"
        filename = "./ffprobe-bad-file.mkv"
        result = verify_hdr_fallback_on_file(filename)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()