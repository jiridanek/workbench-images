#! /usr/bin/env python3.11

"""
Podman wrapper that turns on caching forcefully. This is to be used for builds in GitHub Actions.
"""
import os
import shlex
import subprocess
import sys


def main():
    args = []
    for arg in sys.argv:
        if arg == '--no-cache':
            continue
        args.append(arg)
    if len(sys.argv) > 1 and sys.argv[1] == "build" and "CACHE_IMAGE" in os.environ:
        args.append("--layers")
        args.append(f"--cache-from={os.environ['CACHE_IMAGE']}")
        # todo: conditionally, don't do this for PRs?
        args.append(f"--cache-to={os.environ['CACHE_IMAGE']}")

    print("+", shlex.join(args))
    subprocess.check_call(executable="/usr/bin/podman", args=args)


if __name__ == '__main__':
    main()
