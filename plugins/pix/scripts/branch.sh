#!/bin/bash

function branch() {
    source "$TOOLS_PATH/constants/colors.sh"
    source $TOOLS_PATH/lib/user-interaction.sh
    source $TOOLS_PATH/lib/json.sh
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local CONFIG_FILE=$1
    
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}${IERR}Config JSON file not found.${END_COLOR}"
        return 1
    fi
    
    local pattern=$(read_json_array $CONFIG_FILE branch_rules.pattern)
    local field_names=($(read_json_object_keys $CONFIG_FILE branch_rules.form))
    
    echo -e "${IINFO}Creating form."
    for field_name in "${field_names[@]}"; do
        local title=$(read_json_value $CONFIG_FILE branch_rules.form.$field_name.title)
        local error=$(read_json_value $CONFIG_FILE branch_rules.form.$field_name.error)
        local type=$(read_json_value $CONFIG_FILE branch_rules.form.$field_name.type)
        local possible_values=()
        local field_value
        
        echo -e "${TAB}${ISTAR}${BLUE}${IINFO}${title}${END_COLOR}"
        
        if [ "$type" == "selection" ]; then
            possible_values=($(read_json_object_values $CONFIG_FILE branch_rules.form.${field_name}.values))
            
            show_options ${possible_values[@]}
        fi
        
        read -p $"${TAB}${IDOT}${IINP}" field_value
        
        if [ "$type" == "selection" ]; then
            field_value=${possible_values[((--field_value))]}
            
            if ! [[ "${possible_values[@]}" =~ $field_value ]]; then
                echo -e "${RED}${IERR}$error.${END_COLOR}"
                return 1
            fi
        else
            if [ -z "$field_value" ]; then
                echo -e "${RED}${IERR}$error.${END_COLOR}"
                return 1
            fi
            
            field_value="$(echo "$field_value" | tr ' ' '-')"
        fi
        
        echo -e "${TAB}${IDOT}${IVAL}${YELLOW}${field_value}${END_COLOR}"
        
        pattern="${pattern//\{$field_name\}/$field_value}"
    done
    echo -e "${TAB}${ISTAR}${GREEN}${IOK}Branch template completed.${END_COLOR}"
    
    echo -e "${IINFO}Please validate the output before creation."
    echo -e "${TAB}${ISTAR}${MAGENTA}${IBRCH}${pattern}${END_COLOR}"
    
    local validation="n"
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