#!/bin/bash

show_options() {
    source "$TOOLS_PATH/constants/colors.sh"
    
    for (( i=1; i<=$#; i++ )); do
        echo -e "${DTAB}$i. ${!i}"
    done
}

create_form() {
    source "$TOOLS_PATH/constants/colors.sh"
    source "$TOOLS_PATH/lib/json.sh"
    
    local CONFIG_FILE="$1"
    local form="$2"
    local local_pattern="$3"
    
    for field_name in "${field_names[@]}"; do
        local title=$(read_json_value $CONFIG_FILE commit_rules.form.$field_name.title)
        local error=$(read_json_value $CONFIG_FILE commit_rules.form.$field_name.error)
        local type=$(read_json_value $CONFIG_FILE commit_rules.form.$field_name.type)
        local possible_values=()
        local field_value
        
        echo -e "${TAB}⋆ ${BLUE}${IINFO}${title}${END_COLOR}"
        
        if [ "$type" == "selection" ]; then
            possible_values=($(read_json_object_values $CONFIG_FILE commit_rules.form.${field_name}.values))
            
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
        
        echo -e "${TAB}⋆ ${IVAL}${YELLOW}${field_value}${END_COLOR}"
        
        local_pattern="${local_pattern//\{$field_name\}/$field_value}"
    done
    
    eval "pattern=\"$local_pattern\""
}
