from learn_sql_model.console import console


def test_default_console_not_quiet(capsys):
    console.print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"


def test_default_console_is_quiet(capsys):
    console.quiet = True
    console.print("hello")
    captured = capsys.readouterr()
    assert captured.out == ""
