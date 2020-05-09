#!/usr/bin/python3

import os
import subprocess
from Messages import getMessages

messages = getMessages()


def run(command=[]):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    output, error = process.communicate()

    if process.returncode != 0:
        if error.find("not a git repository") != -1:
            print(messages["notGitRepository"])
        exit()

    return output


def getStatus(messages):
    STATUS_MATCHES = {"#": "branch", "M": "modified",
                      "?": "untracked",
                      "R": "renamed", "A": "added",
                      "D": "deleted"}

    status_data = run(["git", "status", "-sb"])
    status_data = status_data.rstrip().split("\n")

    status = {}
    for change in status_data:
        prefix = change[:2]
        firstCode = change[0]
        secondCode = change[1]
        content = change[3:]
        change_name = ''

        if "R" in prefix:
            files = content.split(" -> ")
            oldFilePaths = files[0].split("/")
            newFilePaths = files[1].split("/")

            for index in range(0, len(oldFilePaths)):
                if not oldFilePaths[index] == newFilePaths[index]:
                    print(messages)
                    content = messages["renamed-modify"].format(
                        '/'.join(oldFilePaths[0:index]), '/'.join(newFilePaths[index:]))
                    break

        if firstCode.isalpha():
            change_name = STATUS_MATCHES["A"]
        else:
            change_name = STATUS_MATCHES[secondCode] if firstCode == ' ' else STATUS_MATCHES[firstCode]

        if not change_name in status:
            status[change_name] = []

        status[change_name].append(content)

    return status


def showStatus(messages):
    status = getStatus(messages)

    print()
    if "branch" in status:
        branch_name = status.pop("branch")[0]
        print(messages["branch"].format(branch_name))

    if len(status) == 0:
        print(messages["clean"])

    for change_name in status:
        changes = status[change_name]

        print(messages[f"{change_name}-title"])
        for change in changes:
            print(messages[change_name].format(change))

    print()


def Router(leftKeys):
    messages = getMessages()
    showStatus(messages)
