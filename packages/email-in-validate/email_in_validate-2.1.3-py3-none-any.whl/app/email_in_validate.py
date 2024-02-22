import re
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('email')
def validate(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        click.echo(f'{email} is a valid email address.')
    else:
        click.echo(f'{email} is not a valid email address.')

if __name__ == "__main__":
    cli()
