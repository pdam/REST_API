import pytest



def pytest_addoption(parser):
    parser.addoption("--switch", action="store", default="aquarius05",
        help="Switch name")

@pytest.fixture
def switch(request):
    return request.config.getoption("--switch")

