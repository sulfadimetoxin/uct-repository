import click

@click.group()
def uct_repository():
    """Enter CLI command for uct-repository"""
    pass


# TODO: your cli scripts
@uct_repository.command("hello_world")
def test_command():
    print("Hello world")