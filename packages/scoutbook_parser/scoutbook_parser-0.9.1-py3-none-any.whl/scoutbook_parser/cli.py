import click
from scoutbook_parser.parser import Parser


@click.command()
@click.option(
    "-t",
    "--output-type",
    default="yaml",
    help="output type, options are yaml (default), toml, and json",
)
@click.option(
    "-o",
    "--outfile",
    type=click.Path(dir_okay=False, writable=True),
    help='output filename, default is "output" with the extension',
)
@click.option(
    "-p",
    "--input_personal",
    type=click.Path(exists=True, dir_okay=False),
    help="input filename for personal data (optional)",
)
@click.argument(
    "input_advancement",
    type=click.Path(exists=True, dir_okay=False),
)
def main(output_type=None, outfile=None, input_personal=None, input_advancement=None):
    if output_type:
        pass
    elif not outfile:
        output_type = "yaml"
    elif outfile[-4:].lower() in ('json', 'yaml', 'toml'):
        output_type = outfile[-4:].lower()
    parser = Parser(
        input_personal=input_personal,
        input_advancement=input_advancement,
        outfile=outfile,
        file_format=output_type,
    )

    if outfile:
        parser.dump()
    else:
        print(parser.dumps())


if __name__ == "__main__":
    main()
