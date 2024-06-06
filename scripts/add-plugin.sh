#!/bin/bash

function add-plugin() {
    source $TOOLS_PATH/constants/colors.sh
    source $TOOLS_PATH/lib/string.sh
    source $TOOLS_PATH/lib/json.sh
    
    local PLUGIN_DIRECTORY="$1"
    local PLUGIN_BASENAME="$(basename "$PLUGIN_DIRECTORY")"
    local PLUGIN_CONFIG="$PLUGIN_DIRECTORY/config.json"
    
    local BASH_PROFILE="$HOME/.bash_profile"
    
    if ! [[ -d "$PLUGIN_DIRECTORY" ]]; then
        echo -e "${RED}${IERR}Plugin directory do not exist.${END_COLOR}"
        return 1
    fi
    
    if ! [[ -f "$PLUGIN_CONFIG" ]]; then
        echo -e "${RED}${IERR}Plugin directory has missing JSON file.${END_COLOR}"
        return 1
    fi
    
    
    local plugin_name="$(read_json_value "$PLUGIN_CONFIG" "name")"
    local plugin_version="$(read_json_value "$PLUGIN_CONFIG" "version")"
    
    echo -e "${IINFO}Setting up $plugin_name@$plugin_version in tools."
    if ! [[ -d $TOOLS_PATH/plugins/$plugin_name ]]; then
        mkdir -p "$TOOLS_PATH/plugins/$plugin_name"
    else
        rm -rf "$TOOLS_PATH/plugins/$plugin_name"
        mkdir -p "$TOOLS_PATH/plugins/$plugin_name"
    fi
    
    cp -r "$PLUGIN_DIRECTORY" "$TOOLS_PATH/plugins"
    mv "$TOOLS_PATH/plugins/$PLUGIN_BASENAME" "$TOOLS_PATH/plugins/$plugin_name"
    echo -e "${TAB}${IDOT}${GREEN}${IOK}Plugin is ready.${END_COLOR}"
    
    
    local plugins=($(ls -l "$TOOLS_PATH/plugins" | grep '^d' | awk '{print $NF}'))
    
    > "$TOOLS_PATH/plugins/init.sh"
    for plugin in "${plugins[@]}"; do
        echo -e "source \"\$TOOLS_PATH/plugins/$plugin/main.sh\"" >> "$TOOLS_PATH/plugins/init.sh"
    done
    echo -e "" >> "$TOOLS_PATH/plugins/init.sh"
    echo -e "${TAB}${IDOT}${GREEN}${IOK}Plugin initialization is ready.${END_COLOR}"
    
    
    local line=""
    local plugin_main_file=()
    while IFS= read -r line; do
        if [[ $line =~ "local PLUGIN_PATH" ]]; then
            local indentation="$(get_indentation "$line")"
            local formatted_line="$indentation""local PLUGIN_PATH=\"\$TOOLS_PATH/plugins/$plugin_name\""
            
            plugin_main_file+=("$formatted_line")
            continue
        fi
        if [[ $line =~ "local PLUGIN_TEMP_PATH" ]]; then
            local indentation="$(get_indentation "$line")"
            local formatted_line="$indentation""local PLUGIN_TEMP_PATH=\"\$TOOLS_PATH/temp/$plugin_name\""
            
            plugin_main_file+=("$formatted_line")
            continue
        fi
        
        plugin_main_file+=("$line")
    done < <(cat "$TOOLS_PATH/plugins/$plugin_name/main.sh")
    
    > "$TOOLS_PATH/plugins/$plugin_name/main.sh"
    for line in "${plugin_main_file[@]}"; do
        echo -e "$line" >> "$TOOLS_PATH/plugins/$plugin_name/main.sh"
    done
    echo -e "${TAB}${IDOT}${GREEN}${IOK}Plugin paths are ready.${END_COLOR}"
    
    if ! [[ -d "$TOOLS_PATH/temp" ]]; then
        mkdir "$TOOLS_PATH/temp"
    fi
    if ! [[ -d "$TOOLS_PATH/temp/$plugin_name" ]]; then
        mkdir "$TOOLS_PATH/temp/$plugin_name"
    fi
    
    if [[ -d "$TOOLS_PATH/plugins/$plugin_name/temp" ]]; then
        rm -rf "$TOOLS_PATH/plugins/$plugin_name/temp"
    fi
    
    if [[ -d "$TOOLS_PATH/temp/$plugin_name" ]]; then
        rm -rf "$TOOLS_PATH/temp/$plugin_name"
    fi
    
    mkdir "$TOOLS_PATH/temp/$plugin_name"
    echo -e "${TAB}${IDOT}${GREEN}${IOK}Plugin temp folder is ready.${END_COLOR}"
    
    source "$BASH_PROFILE"
}