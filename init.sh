#!/bin/bash

function tools-init () {
    local BASHRC="$HOME/.bashrc"
    
    local INSTALL_SCRIPT_PATH=$(readlink -f "$0")
    local TOOLS_PATH=$(dirname "$INSTALL_SCRIPT_PATH")
    
    source $TOOLS_PATH/constants/colors.sh
    
    echo -e "${IINFO}Setting up path variables."
    local line_to_add="source \"$TOOLS_PATH/main.sh\""
    
    if ! grep -q "TOOLS VARIABLES" "$BASHRC"; then
        echo -e "" >> "$BASHRC"
        echo -e "# [TOOLS VARIABLES]" >> "$BASHRC"
        echo -e "TOOLS_PATH=\"$TOOLS_PATH\"" >> "$BASHRC"
        echo -e "source \"$TOOLS_PATH/main.sh\"" >> "$BASHRC"
        echo -e "# [TOOLS VARIABLES]" >> "$BASHRC"
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Tools variables added.${END_COLOR}"
    else
        echo -e "${TAB}${ISTAR}${YELLOW}${IWARN}Tools variables already exist.${END_COLOR}"I
    fi
    
    source "$BASHRC"
    
    
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
    done
    
    source "$BASHRC"
    
    return 0
}

tools-init $0