#!/usr/bin/env python3
# console/manager.py

import click
from console.init import init  # import del gruppo 'init' da console/init.py

@click.group(
    help=(
        "Manager dei comandi custom.\n\n"
        "Usa:\n"
        "  ./manager.py <gruppo> <comando>\n"
        "Esempio:\n"
        "  ./manager.py init create_admin"
    )
)
def cli():
    """
    Punto di ingresso di tutti i sottocomandi.
    """
    # Non serve un 'pass' esplicito: la docstring basta a definire il gruppo
    ...

# Registriamo il gruppo “init” definito in console/init.py
cli.add_command(init)

if __name__ == "__main__":
    cli()
