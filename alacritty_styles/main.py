from os.path import expanduser, join

import click

from .colorscheme import (apply_colorscheme, download_colorschemes,
                          is_theme_available, list_available_themes)

repo = "eendroroy/alacritty-theme/"
github_raw = "https://raw.githubusercontent.com/" + repo + "master/schemes.yaml"
config_file = expanduser(join("~", ".config/alacritty/alacritty.yml"))


@click.command()
@click.argument("theme", nargs=1, required=False)
@click.option("--list-themes", is_flag=True, help="List available themes")
def cli(list_themes, theme):
    # Make sure to remove spaces and change to lowercase
    if theme or list_themes:
        colorschemes = download_colorschemes(github_raw)

    if list_themes and not theme:
        list_available_themes(colorschemes)
    elif theme:
        theme = theme.replace(" ", "_").lower()
        is_theme_available(colorschemes, theme)

        apply_colorscheme(colorschemes, config_file, theme)
    else:
        raise click.BadArgumentUsage("Need a parameter")


if __name__ == "__main__":
    cli()
