import pytest


class Test(object):

    @pytest.mark.complete("objcopy ")
    def test_(self, completion):
        assert completion.list