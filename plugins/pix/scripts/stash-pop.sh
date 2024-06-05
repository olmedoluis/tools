#!/bin/bash

function stash-pop() {
    source "$TOOLS_PATH/constants/colors.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    stash_count=$(git stash list | wc -l)
    
    if [ "$stash_count" -eq 0 ]; then
        echo -e "${RED}${IERR}There are no changes saved in the stash.${END_COLOR}"
        return 1
    fi
    
    echo -e "${IINFO}Applying the last saved change from the stash."
    git stash pop --quiet
    
    echo -e "${TAB}${IDOT}${GREEN}${IOK}Last stash change applied.${END_COLOR}"
}
