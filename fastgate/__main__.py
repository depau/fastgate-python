import sys

if __name__ == "__main__":
    from fastgate import cli
    args = sys.argv[1:]

    this_module = 'fastgate'

    name = 'python -m ' + this_module

    sys.argv = [name] + args

    cli()