import click
import obelisk

from pathlib import Path


@click.command()
@click.option("--convert", default=True, help=".")
@click.option("--input", prompt="Input filepath: ", help=".")
@click.option("--destination", prompt="Destination filepath: ", help=".")
def main(convert, input, destination):
    if convert:
        splitter = obelisk.FileSplitter(Path(input), Path(destination))
        splitter.process_input()
    else:
        logger.error("Directives besides 'convert' are not implemented!")


if __name__ == "__main__":
    main()
