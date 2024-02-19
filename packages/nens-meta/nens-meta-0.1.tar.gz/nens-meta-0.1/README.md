# N&S "meta" repository

Modeled after https://github.com/plone/meta , it is a tool to keep lots of repositories up to date regarding minutia such as "editorconfig", "ruff", "pre-commit" and "github actions". Stuff that's often generated once with a cookiecutter and never afterwards modified, even though there's much goodness to be found in new settings.

The settings and config files go hand in hand with some recommended local settings in your development environment, like recommended vscode extensions.

The basic idea is **make it easy to write clean and neat and correct code without making the process irritating**. Installing vscode's "editorconfig" plugin once is hardly a chore. If a project's editorconfig file then prevents you from ever having to worry about lineendings, trailing spaces, indentation and other non-content-related stuff... that's a win.

Note that [our cookiecutter template](https://github.com/nens/cookiecutter-python-template) normally should have been the basis from which you started your project. But it might have been created by hand. Or it might have been a long time ago. "Meta" tries to fix up your project a bit.


## Installing/developing this project

For the basic instructions, see our own documentation. So:

    $ pip install tox
    $ tox -q


## TODO

- manifest.ini

- docker-compose

- Projectnummer

- testen met vscode

- version.txt (threedi-docs)

- `DJANGO_SETTINGS_MODULE = artifact_handler.developmentsettings` in tool:pytest?
