#!/usr/bin/python3

import sys
import GitRoutes


def isGitShortcut(keyword):
    routes = GitRoutes.ROUTES

    for entity in routes.values():
        for mainKey in entity["keys"]:
            if mainKey == keyword:
                return keyword

        for alias in entity["alias"]:
            if alias == keyword:
                return keyword

    return False


if __name__ == "__main__":
    arg = sys.argv[1:]

    for key in arg:
        print("is git key", isGitShortcut(key))

        if key == isGitShortcut(key):
            print("getting status")
