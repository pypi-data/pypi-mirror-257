# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.cli._decorators import cli_flag

from .._decorators import cli_command, cli_argument, catch_and_log_and_exit


@cli_command(__file__, "codepages display")
@cli_argument("input_cps", metavar='codepage', type=str, required=False, nargs=-1)
@cli_flag(
    "-a", "--all", help="Ignore CODEPAGE argument(s) and display all supported code pages at once."
)
@cli_flag("-l", "--list", help="Print supported code page list and exit.")
@cli_flag("-w", "--wide", help="Use wider table cells.")
@catch_and_log_and_exit
def invoker(**kwargs):
    """
    Display 0x00 - 0xFF bytes encoded in a specified CODEPAGE(s). If no CODEPAGE argument
    is provided, display *ascii* code page.
    """
    from es7s.cmd.grobocop import action

    action(**kwargs)
