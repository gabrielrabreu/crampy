import unittest


def create_test_suite() -> unittest.TestSuite:
    test_suite = unittest.defaultTestLoader.discover(
        start_dir="utests",
        pattern="test_*.py"
    )
    return test_suite


if __name__ == "__main__":
    suite = create_test_suite()
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
