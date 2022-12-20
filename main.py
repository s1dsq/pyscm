#!/usr/bin/env python3

import sys

from pyscm.pyscm import interpret_from_file, run_repl

if __name__ == "__main__":
    if len(sys.argv) > 1:
        interpret_from_file(sys.argv[1])
    else:
        run_repl()
