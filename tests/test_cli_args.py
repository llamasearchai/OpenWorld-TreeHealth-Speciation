from typer.testing import CliRunner
from openworld_tshm.cli import app


runner = CliRunner()


def test_process_demo_arg_validation():
    res = runner.invoke(app, ["process-demo", "0", "0"])
    assert res.exit_code != 0


