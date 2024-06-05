# Tools

This repository contains a collection of scripts designed to simplify the creation of CMD scripts with a user-friendly UI, primarily tailored for git-bash/windows environments. These tools streamline various git operations, enhancing workflow efficiency.

## Technologies

The following technologies are utilized within the project:

- [jq](https://jqlang.github.io/jq) - Version 1.7.1
- [git](https://www.git-scm.com/) - Version 2.32.0.windows.1

## Installation

To install **Tools**, follow these steps:

1. Clone the repository:

   ```bash
   $ git clone https://github.com/olmedoluis/tools.git
   ```

2. Navigate to the cloned directory:

   ```bash
   $ cd tools
   ```

3. Run the initialization script:

   ```bash
   $ ./init.sh
   ```

## Usage

### Tools

- **add-plugin**: This command adds a plugin to the plugins folder and automatically updates paths to the main folder.

  ```
  $ tools add-plugin path/to/plugin-folder
  ```

### PIX (Built-in Plugin)

PIX provides a minimalist UI for various git operations:

- **stage**: Extends file search by properties, allowing for direct staging of files.

  ```
  $ pix stage [any-file-pattern]
  ```

- **unstage**: Extends file search by properties, enabling direct unstaging of files.

  ```
  $ pix unstage [any-file-pattern]
  ```

- **undo**: Extends file search by properties, allowing for direct undoing of file modifications. Untracked files will be deleted.

  ```
  $ pix undo [any-file-pattern]
  ```

- **examine**: Provides a minimalist UI for `git add -p`, allowing users to choose what to do with each file hunk.

  ```
  $ pix examine
  ```

- **stash**: Utilizes a minimalist UI for `git stash`, stashing changes of staged files only.

  ```
  $ pix stash
  ```

- **pop**: Provides a minimalist UI for `git pop`.

  ```
  $ pix pop
  ```

- **status**: Offers a minimalist UI for `git status`.

  ```
  $ pix status
  ```

- **branch**: Presents a customizable form for branch creation. Configuration available in [config.json](./plugins/pix/config.json).

  ```
  $ pix branch
  ```

- **commit**: Presents a customizable form for commit creation. Configuration available in [config.json](./plugins/pix/config.json).

  ```
  $ pix commit
  ```
