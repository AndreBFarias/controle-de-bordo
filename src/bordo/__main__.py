"""Ponto de entrada: python -m bordo."""

import sys


def main() -> None:
    """Entrada principal do Controle de Bordo."""
    from bordo import __version__

    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-V"):
        print(f"bordo {__version__}")
        sys.exit(0)

    try:
        from bordo.cli import app

        app()
    except ImportError:
        print(f"bordo {__version__}")
        print("CLI indisponível. Instale com: pip install controle-de-bordo[cli]")
        sys.exit(1)


if __name__ == "__main__":
    main()
