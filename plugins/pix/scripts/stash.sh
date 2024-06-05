#!/bin/bash

function stash() {
    source "$TOOLS_PATH/constants/colors.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    staged_files_stringified=$(git diff --cached --name-only)
    staged_files_count=$(git diff --cached --name-only | wc -l)
    
    if [ "$staged_files_count" -gt 0 ]; then
        echo -e "${IINFO}Saving staged file(s) in stash storage."
        git stash push --quiet $staged_files_stringified > /dev/null 2>&1
        
        echo -e "${TAB}${IDOT}${GREEN}${IOK}$staged_files_count file(s) saved in stash storage.${END_COLOR}"
    else
        echo -e "${RED}${IERR}No files staged to save in stash storage.${END_COLOR}"
    fi
}
