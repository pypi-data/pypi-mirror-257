# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023-2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from .._base_opts_params import IntRange
from .._decorators import cli_command, catch_and_log_and_exit, cli_argument, cli_option, cli_flag


@cli_command(__file__, short_help="&(fu)sion-&(dra)in, remote image generation neural network")
@cli_argument("prompt", type=str, required=True, nargs=-1)
@cli_option(
    "-s",
    "--style",
    help="Select picture style. List of supported styles can be seen with '-v'.",
    default="DEFAULT",
    show_default=True,
)
@cli_option(
    "-n",
    "--times",
    type=IntRange(1),
    default=1,
    show_default=True,
    help="How many times each prompt should be queried.",
)
@cli_option(
    "-T",
    "--threads",
    type=IntRange(0),
    default=0,
    help="How many threads to perform API calls with (0=auto).",
)
@cli_flag(
    "-k", "--keep", help="Keep image origins (default is to delete them and keep composite only)."
)
@cli_flag("-R", "--no-retry", help="Do not repeat failed (censored) queries.")
@cli_flag("-S", "--stdin", help="Ignore 'PROMPT'S arguments and read from standard input instead.")
@catch_and_log_and_exit
class invoker:
    """
    Query a remote service with 'PROMPT'S describing what should be on the
    picture, and fetch the result picture(s). Several arguments in quotes
    will be treated as separate 'PROMPT'S:\n\n

        text2img \\"Prompt number one\\" \\"Prompt number two\\"\n\n

    When '-S' is provided, the arguments are ignored completely, and standard
    input is read instead; expected format is one prompt per line. If a word
    starts with a hyphen \\"-\\", it is treated like 'negative' prompt.\n\n

    Total amount of result pictures is *P* * *N*, where *P* is prompts amount,
    and *N* is an argument of '--times' option (1 if omitted). Argument of
    '--threads' option does not influence picture amount, rather it controls
    how many jobs will be executed in parallel. There is an embedded retry
    mechanism, which will query the same prompt several times if the service
    answers with a placheolder and "'censored'" flag; this behaviour can be
    switched off with '--no-retry' flag.\n\n

    Remote service is https://fusionbrain.ai.
    """

    def __init__(self, **kwargs):
        from es7s.cmd.fudra import action

        action(**kwargs)
