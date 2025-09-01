import unittest
import os
def main():
    print("Running all tests...")
    loader = unittest.TestLoader()
    tests = loader.discover('.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print("Some tests failed.")
    
if __name__ == "__main__":
    main()