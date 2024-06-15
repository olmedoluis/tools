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
    local pattern="${@:2}"
    
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
    
    local commit_info="$(git commit --no-verify -m "$pattern")"
    
    local files_change_count="$(echo "$commit_info" | grep -oP '\d+(?= files changed)|\d+(?= file changed)')"
    local insertions="$(echo "$commit_info" | grep -oP '\d+(?= insertions\(\+\))|\d+(?= insertion\(\+\))')"
    local deletions="$(echo "$commit_info" | grep -oP '\d+(?= deletions\(\-\))|\d+(?= deletion\(\-\))')"
    local files_created_count="$(echo "$commit_info" | grep -c 'create mode')"
    local files_renamed="$(echo "$commit_info" | grep -c 'rename ')"
    
    files_change_count=${files_change_count:-"0"}
    insertions=${insertions:-"0"}
    deletions=${deletions:-"0"}
    files_created_count=${files_created_count:-"0"}
    files_renamed=${files_renamed:-"0"}
    
    local additions=""
    local file_counters=""
    
    if [[ $insertions != "" ]]; then
        additions+="${GREEN}${IPLUS}${insertions}${END_COLOR} "
    fi
    if [[ $deletions != "" ]]; then
        additions+="${RED}${ILESS}${deletions}${END_COLOR} "
    fi
    if [[ $files_change_count != "" ]]; then
        file_counters+="${YELLOW}${IMOD}${files_change_count}${END_COLOR} "
    fi
    if [[ $files_created_count != "" ]]; then
        file_counters+="${CYAN}${IUNTR}${files_created_count}${END_COLOR} "
    fi
    if [[ $files_renamed != "" ]]; then
        file_counters+="${BLUE}${IRNM}${files_renamed}${END_COLOR} "
    fi
    echo -e "${TAB}${IDOT}${file_counters}${END_COLOR}"
    echo -e "${TAB}${IDOT}${additions}${END_COLOR}"
    echo -e "${TAB}${ISTAR}${GREEN}${IOK}Changes commited.${END_COLOR}"
}
