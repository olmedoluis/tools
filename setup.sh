#!/bin/bash

# Get current file directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
CURRENTDIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"

PIXDIR="$CURRENTDIR/scripts/Pix.py"
PIXALIAS="alias pxb=$PIXDIR"

echo
# Enable to execute pix program
[ ! -x $PIXDIR ] && echo " Enable to execute" && chmod +x $PIXDIR

# Set up command shortcut for bash
BASH=~/.bash_aliases
if test -f "$BASH" && ! cat ~/.bash_aliases | grep "alias pxb=$PIXDIR" &>/dev/null; then
  echo " Setting up bash shortcut.."
  echo $PIXALIAS >>${BASH}
fi

# Set up command shortcut for ZSH
ZSH=~/.zshrc
if test -f "$ZSH" && ! cat ~/.zshrc | grep "alias pxb=$PIXDIR" &>/dev/null; then
  echo " Setting up zsh shortcut.."
  echo $PIXALIAS >>${ZSH}
  source $ZSH &>/dev/null
  echo
fi

echo " Pix has been installed!"
echo
