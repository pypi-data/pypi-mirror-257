def pytest_configure(config):
    config.addinivalue_line("markers", "compile: Run compile tests.")
    config.addinivalue_line("markers", "profile: Run profile tests.")
    config.addinivalue_line("markers", "inference: Run inference tests.")
