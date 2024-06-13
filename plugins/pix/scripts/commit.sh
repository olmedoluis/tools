#!/bin/bash

function commit() {
    source "$TOOLS_PATH/constants/colors.sh"
    source "$TOOLS_PATH/lib/user-interaction.sh"
    source "$TOOLS_PATH/lib/json.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local CONFIG_FILE=$1
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}${IERR}Config JSON file not found.${END_COLOR}"
        return 1
    fi
    
    local pattern=($(read_json_array $CONFIG_FILE commit_rules.pattern))
    pattern="${pattern[@]}"
    
    echo -e "${IINFO}Creating form."
    create_form "$CONFIG_FILE" "commit_rules.form" "$pattern"
    echo -e "${TAB}⋆ ${GREEN}${IOK}Commit template completed.${END_COLOR}"
    
    echo -e "${IINFO}Saving changes."
    echo -e "${TAB}⋆ ${MAGENTA}${IBRCH}${pattern}${END_COLOR}"
    
    git commit -no-verify -m "$pattern" > /dev/null 2>&1
    echo -e "${TAB}⋆ ${GREEN}${IOK}Staged changes commited.${END_COLOR}"
}
