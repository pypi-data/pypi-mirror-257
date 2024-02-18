from click.testing import CliRunner
from llm.cli import cli
import llm


def test_embed_hazo():
    model = llm.get_embedding_model("hazo")
    floats = model.embed("hello world")
    assert len(floats) == 16
    assert all(isinstance(f, float) for f in floats)
    assert floats ==  [5.0, 5.0] + [0.0] * 14

def test_hazo_embed_multi(tmpdir):
    db_path = str(tmpdir / "test.db")
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "embed-multi",
            "-m",
            "hazo",
            "test",
            "-",
            "-d",
            db_path,
        ],
        input='[{"id": "a", "text": "abc"}]',
        catch_exceptions=False,
    )
    assert result.exit_code == 0
