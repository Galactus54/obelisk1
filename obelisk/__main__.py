import logging

import click
import obelisk

from pathlib import Path

logger = logging.getLogger(__name__)


@click.command()
@click.option("-c", "--convert", is_flag=True,
              help="convert file (currently the only mode)")
@click.option("-i", "--input", prompt="Input filepath: ",
              help="Input filepath. Will prompt the user if empty")
@click.option("-d", "--destination", prompt="Destination filepath: ",
              help="Output directory. WIll prompt the user if empty. Will create if it doesn't exist.")
def main(convert, input, destination):
    if convert:
        splitter = obelisk.FileSplitter(input, destination)
        splitter.process_input()
        logger.info("Conversion completed!")
    else:
        logger.error("Directives besides 'convert' are not implemented!")


if __name__ == "__main__":
    main()
