#!/usr/bin/python3

import os
import subprocess
import StatusMessages


def getStatus():
    STATUS_MATCHES = {"##": "branch", " M": "modified", "M ": "added",
                      "??": "untracked", "": "unknown",
                      "R ": "renamed", "A ": "added", "AM": "added"}

    status_data = subprocess.run(
        ["git", "status", "-sb"], stdout=subprocess.PIPE).stdout
    status_data = str(status_data)[2:-3].split("\\n")

    status = {}
    for change in status_data:
        prefix = change[:2]
        content = change[3:]
        change_name = STATUS_MATCHES[prefix]
        if change_name in status:
            status[change_name].append(content)
        else:
            status[change_name] = [content]

    return status


def showStatus():
    status = getStatus()
    messages = StatusMessages.MESSAGES
    print()

    for change_name in status:
        changes = status[change_name]

        if change_name == "branch":
            branch_name = changes[0]
            print(messages["branch"].format(branch_name))
            continue

        print(messages[change_name])
        for change in changes:
            print("\t", change)
        print()


if __name__ == "__main__":
    showStatus()
    pass
