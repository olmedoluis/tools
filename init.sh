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
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Tools variables added.${END_COLOR}"
    else
        echo -e "${TAB}${ISTAR}${YELLOW}${IWARN}Tools variables already exist.${END_COLOR}"I
    fi
    
    source "$BASH_PROFILE"
    
    return 0
}

tools-init $0