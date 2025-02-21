# # settings/test_runner.py
#
# import unittest
# from unittest.runner import TextTestResult
#
#
# class CustomTextTestResult(unittest.TextTestResult):
#     def startTest(self, test):
#         super(TextTestResult, self).startTest(test)
#         if self.showAll:
#             self.stream.write(test._testMethodDoc)
#             self.stream.write(" ... ")
#             self.stream.flush()
#             self._newline = False
#
#
# class CustomTextTestRunner(unittest.TextTestRunner):
#
#     def __init__(self):
#         super(CustomTextTestRunner).__init__(resultclass=CustomTextTestResult)
#
#
# class TestCaseGroup(unittest.TestCase):
#
#     def test_method01(self):
#         """ 여기에 적힌 글자가 테스트 결과에 표시됩니다. """
#         self.assertEqual(1, 1)
#
#
# if __name__ == '__main__':
#     unittest.main(testRunner=CustomTextTestRunner)
