from learn_sql_model.console import console


def verbose_callback(value: bool) -> None:
    if value:
        console.quiet = False
