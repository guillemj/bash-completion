import pytest

from conftest import assert_bash_exec


@pytest.mark.bashcomp(cmd=None)
class TestUnitGetFirstArg:
    @pytest.fixture(scope="class")
    def functions(self, bash):
        assert_bash_exec(
            bash,
            '_comp__test_unit() { local -a "words=$1"; local cword=$2 arg=; shift 2; _comp_get_first_arg "$@" && printf "%s\\n" "$arg"; return 0; }',
        )

    def test_1(self, bash, functions):
        assert_bash_exec(bash, "_comp__test_unit '()' 0")

    def test_2(self, bash, functions):
        output = assert_bash_exec(
            bash, '_comp__test_unit "(a b)" 2', want_output=None
        ).strip()
        assert output == "b"

    def test_3(self, bash, functions):
        output = assert_bash_exec(
            bash, '_comp__test_unit "(a bc)" 2', want_output=None
        ).strip()
        assert output == "bc"

    def test_4(self, bash, functions):
        output = assert_bash_exec(
            bash, '_comp__test_unit "(a b c)" 2', want_output=None
        ).strip()
        assert output == "b"

    def test_5(self, bash, functions):
        """Neither of the current word and the command name should be picked
        as the first argument"""
        output = assert_bash_exec(
            bash, '_comp__test_unit "(a b c)" 1', want_output=None
        ).strip()
        assert output == ""

    def test_6(self, bash, functions):
        """Options starting with - should not be picked as the first
        argument"""
        output = assert_bash_exec(
            bash, '_comp__test_unit "(a -b -c d e)" 4', want_output=None
        ).strip()
        assert output == "d"
