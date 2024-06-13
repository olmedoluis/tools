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
        pattern=$(read_json_array $CONFIG_FILE branch_rules.pattern)
        
        create_form "$CONFIG_FILE" "branch_rules.form" "$pattern"
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Branch template completed.${END_COLOR}"
    fi
    
    echo -e "${IINFO}Please validate the output before creation."
    echo -e "${TAB}${ISTAR}${MAGENTA}${IBRCH}${pattern}${END_COLOR}"
    
    local validation=""
    echo -e "${TAB}${ISTAR}${BLUE}${IINFO}Should it be created? (y/n)${END_COLOR}"
    read -p $"${TAB}${IDOT}${IINP}" validation
    
    if [[ "${validation}" =~ "y" ]]; then
        git checkout -b $pattern > /dev/null 2>&1
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Branch creation completed.${END_COLOR}"
    else
        echo -e "${TAB}${ISTAR}${RED}${IERR}Branch creation canceled.${END_COLOR}"
        return 1
    fi
}