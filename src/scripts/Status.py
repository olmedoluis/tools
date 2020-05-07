#!/usr/bin/python3

import os
import subprocess
import Messages


def getStatus():
    STATUS_MATCHES = {"##": "branch", " M": "modified", "M ": "added",
                      "??": "untracked", "": "unknown",
                      "R ": "renamed", "A ": "added", "AM": "added",
                      " D": "deleted", "MM": "added"}

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
    messages = Messages.MESSAGES
    print()

    if "branch" in status:
        branch_name = status.pop("branch")[0]
        print(messages["branch"].format(branch_name))

    if len(status) == 0:
        print(messages["clean"])
        return

    for change_name in status:
        changes = status[change_name]

        print(messages[change_name])
        for change in changes:
            print(messages["change"].format(change))

    print()


def Router(leftKeys):
    showStatus()
