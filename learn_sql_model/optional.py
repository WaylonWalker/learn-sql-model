import textwrap


def _optional_import_(
    module: str,
    name: str = None,
    group: str = None,
    package="learn_sql_model",
):
    """
    lazily throws import errors only then the optional import is used, and
    includes a group install command for the user to install all dependencies
    for the requested feature.
    """
    import importlib

    try:
        module = importlib.import_module(module)
        return module if name is None else getattr(module, name)
    except ImportError as e:
        msg = textwrap.dedent(
            f"""
        "pip install '{package}[{group}]'" package to make use of this feature
        Alternatively "pip install '{package}[all]'" package to install all optional dependencies
        """
        )
        import_error = e

        class _failed_import:
            """
            Lazily throw an import error.  Errors should be thrown whether the
            user tries to call the module, get an attubute from the module, or
            getitem from the module.

            """

            def _failed_import(self, *args):
                raise ImportError(msg) from import_error

            def __call__(self, *args):
                """
                Throw error if the user tries to call the module i.e
                _optional_import_('dummy')()
                """
                self._failed_import(*args)

            def __getattr__(self, name):
                """
                Throw error if the user tries to get an attribute from the
                module i.e _optional_import_('dummy').dummy.
                """
                if name == "_failed_import":
                    return object.__getattribute__(self, name)
                self._failed_import()

            def __getitem__(self, name):
                """
                Throw error if the user tries to get an item from the module
                i.e _optional_import_('dummy')['dummy']
                """
                self._failed_import()

        return _failed_import()
