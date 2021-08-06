# LTA's Source Code

Currently, the source code is divided as follows:

- `cli` module contains the main entrypoint for the CLI. See [cli](./cli.md).
- `parser` module that contains the `argparse` argument parser.
  Think of this as the CLI's structure.
  See [parser](./parser.md).
- `commands` sub-package that contains the functions used to handle inputs.
  See [commands](./commands.md).

```{toctree}
:hidden:
:maxdepth: 3

cli
parser
commands
```
