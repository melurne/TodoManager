import click

@click.group()
def cli() :
    click.echo("Hello")

@cli.command()
def test() :
    click.echo('Test')
