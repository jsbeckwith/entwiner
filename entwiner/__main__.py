"""Entwiner CLI."""

import click

from . import build

BATCH_SIZE = 10000


@click.command()
@click.argument("infiles", nargs=-1, type=click.Path("r"))
@click.argument("outfile")
@click.option("--precision", default=7)
@click.option("--changes-sign", multiple=True)
def entwiner(infiles, outfile, precision, changes_sign):
    click.echo("Creating database and importing edges...")
    build.create_graph(
        infiles,
        outfile,
        precision=precision,
        batch_size=BATCH_SIZE,
        changes_sign=changes_sign,
    )
    click.echo("Done!")


if __name__ == "__main__":
    entwiner()
