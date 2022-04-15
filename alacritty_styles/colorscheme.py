from os.path import isfile

from click import UsageError, echo, echo_via_pager, style
from requests import get
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

y = YAML()


def download_colorschemes(url):
    echo(style("Requesting themes..."))
    colorschemes = y.load(get(url).text)

    return colorschemes


def apply_colorscheme(colorschemes, config_path, theme):
    if not isfile(config_path):
        raise UsageError("Could not find default configuration file")

    # Include the file
    with open(config_path, 'r+') as f:
        content = y.load(f)
        if type(content) != CommentedMap:
            content = CommentedMap()
        content["colors"] = colorschemes["schemes"][theme]
        f.seek(0)
        y.dump(content, f)
        f.truncate()


def list_available_themes(colorschemes):
    themes_page = [
        style("-> ", fg="green") + x.title().replace("_", " ")
        for x in colorschemes["schemes"]
    ]
    echo_via_pager(style("Available Themes: \n\n", fg="red") + "\n".join(themes_page))


def is_theme_available(colorschemes, theme):
    if theme not in colorschemes["schemes"]:
        theme = theme.replace("_", " ").title()
        raise UsageError(f"{theme} is not available")
