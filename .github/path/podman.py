#! /usr/bin/env python3.11

"""
Podman wrapper that turns on caching forcefully. This is to be used for builds in GitHub Actions.
"""
import os
import shlex
import shutil
import subprocess
import sys


def main():
    args = []
    for arg in sys.argv:
        if arg == '--no-cache':
            continue
        args.append(arg)
    # https://github.com/containers/podman/issues/22044
    if len(sys.argv) > 1 and sys.argv[1] in ("build", "run"):
        args.append("--network=slirp4netns")
    if len(sys.argv) > 1 and sys.argv[1] == "build" and "CACHE_IMAGE" in os.environ:
        args.append("--layers")
        args.append(f"--cache-from={os.environ['CACHE_IMAGE']}")
        # todo: conditionally, don't do this for PRs?
        args.append(f"--cache-to={os.environ['CACHE_IMAGE']}")

    print("+", shlex.join(args))
    ret = subprocess.call(executable="/home/linuxbrew/.linuxbrew/bin/podman", args=args)

    exit(ret)


if __name__ == '__main__':
    main()
