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
    local pattern="$2"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}${IERR}Config JSON file not found.${END_COLOR}"
        return 1
    fi
    
    if [[ -z $pattern ]]; then
        echo -e "${IINFO}Creating form."
        pattern=$(read_json_array "$CONFIG_FILE" "commit_rules.pattern")
        pattern="${pattern[@]}"
        
        create_form "$CONFIG_FILE" "commit_rules.form" "$pattern"
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Commit form completed.${END_COLOR}"
        echo -e "${IINFO}Creating commit."
    else
        echo -e "${IINFO}Commiting changes."
    fi
    
    echo -e "${TAB}${IDOT}${CYAN}${ICMT}${pattern}${END_COLOR}"
    
    if git commit --no-verify -m "$pattern" > /dev/null 2>&1; then
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Changes commited.${END_COLOR}"
    else
        echo -e "${TAB}${ISTAR}${RED}${IERR}Commit failed.${END_COLOR}"
        return 1
    fi
}
