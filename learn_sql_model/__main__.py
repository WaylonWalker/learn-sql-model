# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT

import typer

from .cli.app import main

if __name__ == "__main__":
    typer.run(main)
