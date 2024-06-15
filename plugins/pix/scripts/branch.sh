#!/bin/bash

function branch() {
    source "$TOOLS_PATH/constants/colors.sh"
    source "$TOOLS_PATH/lib/user-interaction.sh"
    source "$TOOLS_PATH/lib/json.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local CONFIG_FILE="$1"
    local pattern="$2"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}${IERR}Config JSON file not found.${END_COLOR}"
        return 1
    fi
    
    if [[ -z $pattern ]]; then
        echo -e "${IINFO}Creating form."
        pattern=$(read_json_array "$CONFIG_FILE" "branch_rules.pattern")
        
        create_form "$CONFIG_FILE" "branch_rules.form" "$pattern"
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Branch form completed.${END_COLOR}"
        echo -e "${IINFO}Creating branch."
    else
        echo -e "${IINFO}Creating given branch."
    fi
    
    echo -e "${TAB}${IDOT}${MAGENTA}${IBRCH}${pattern}${END_COLOR}"
    
    if git rev-parse --verify "$pattern" >/dev/null 2>&1; then
        echo -e "${TAB}${ISTAR}${RED}${IERR}Branch name already exists.${END_COLOR}"
        return 1
    fi
    
    if git checkout -b $pattern > /dev/null 2>&1; then
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Branch creation completed.${END_COLOR}"
    else
        echo -e "${TAB}${ISTAR}${RED}${IERR}Branch creation failed.${END_COLOR}"
        return 1
    fi
}