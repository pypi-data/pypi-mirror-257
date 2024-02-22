import click

from .functions import *


CONTEXT_SETTINGS = dict(
		help_option_names = [
			'-h',
			'--help'
		]
)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./main.tex",
        show_default=True,
        help="Input file path"
        )
def main(inputfile):
    first_dict = process_file(inputfile)
    answer_key_first_dict = process_answer_key(first_dict)
    contents = open(inputfile, 'r').read()
    answer_key_second_dict = process_second_enumerate(contents)

    generate_answer_key(answer_key_first_dict, answer_key_second_dict)















