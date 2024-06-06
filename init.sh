#!/bin/bash

function tools-init () {
    local BASH_PROFILE="$HOME/.bash_profile"
    
    local INSTALL_SCRIPT_PATH=$(readlink -f "$0")
    local TOOLS_PATH=$(dirname "$INSTALL_SCRIPT_PATH")
    
    source $TOOLS_PATH/constants/colors.sh
    
    echo -e "${IINFO}Setting up path variables."
    local line_to_add="source \"$TOOLS_PATH/main.sh\""
    
    if ! grep -q "TOOLS VARIABLES" "$BASH_PROFILE"; then
        echo -e "" >> "$BASH_PROFILE"
        echo -e "# [TOOLS VARIABLES]" >> "$BASH_PROFILE"
        echo -e "TOOLS_PATH=\"$TOOLS_PATH\"" >> "$BASH_PROFILE"
        echo -e "source \"$TOOLS_PATH/main.sh\"" >> "$BASH_PROFILE"
        echo -e "# [TOOLS VARIABLES]" >> "$BASH_PROFILE"
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Tools variables added.${END_COLOR}"
    else
        echo -e "${TAB}${ISTAR}${YELLOW}${IWARN}Tools variables already exist.${END_COLOR}"I
    fi
    
    source "$BASH_PROFILE"
    
    
    if ! [[ -d "$TOOLS_PATH/temp" ]]; then
        mkdir "$TOOLS_PATH/temp"
    fi
    if ! [[ -d "$TOOLS_PATH/temp/tools" ]]; then
        mkdir "$TOOLS_PATH/temp/tools"
    fi
    
    local built_in_plugins=$( ls -l "$TOOLS_PATH/plugins" | grep "^d" | awk '{print $NF}')
    for plugin_name in "${built_in_plugins[@]}"; do
        mv "$TOOLS_PATH/plugins/$plugin_name" "$TOOLS_PATH/temp/tools"
        tools add-plugin "$TOOLS_PATH/temp/tools/$plugin_name"
        rm -rf "$TOOLS_PATH/temp/tools/$plugin_name"
    done
    
    source "$BASH_PROFILE"
    
    return 0
}

tools-init $0