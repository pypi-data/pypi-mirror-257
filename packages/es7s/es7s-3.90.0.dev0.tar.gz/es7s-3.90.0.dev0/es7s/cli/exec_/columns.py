# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._base_opts_params import CMDTRAIT_ADAPTIVE
from .._decorators import (
    catch_and_log_and_exit,
    cli_argument,
    cli_command,
    cli_flag,
)


@cli_command(__file__, "SGR-aware text to columns splitter", traits=[CMDTRAIT_ADAPTIVE])
@cli_argument("file", type=click.File(mode="r"), required=False)
@cli_flag("-d", "--demo", help="Ignore FILE argument and use built-in example text as input.")
@cli_flag("-X", "--rows-first", help="Fill table horizontally rather than vertically.")
@catch_and_log_and_exit
def invoker(*args, **kwargs):
    """
    Read text from given FILE and display it split into columns. If FILE is omitted
    or equals to ''-'', read standard input instead.\n\n

    Amount of columns is determined automatically depending on original lines maximum
    length and @A terminal width.
    """
    from es7s.cmd.columns import action

    action(**kwargs)
