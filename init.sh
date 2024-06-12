#!/bin/bash

function tools-init () {
    local BASHRC="$HOME/.bashrc"
    
    local INSTALL_SCRIPT_PATH=$(readlink -f "$0")
    local TOOLS_PATH=$(dirname "$INSTALL_SCRIPT_PATH")
    
    source $TOOLS_PATH/constants/colors.sh
    source $TOOLS_PATH/lib/string.sh
    source $TOOLS_PATH/lib/file.sh
    
    echo -e "${IINFO}Setting up path variables."
    local old_tools_path_line="$(get_file_number "$BASHRC" '^.*TOOLS_PATH=.*$')"
    local old_main_source_line="$(get_file_number "$BASHRC" '^.*source.*\/tools\/main.sh"$')"
    local slash="/"
    local normal_slash="\/"
    
    if [[ -n $old_tools_path_line ]]; then
        local line=$(sed -n "${old_tools_path_line}p" "$BASHRC")
        local identation="$(get_indentation $line)"
        
        sed -i "${old_tools_path_line}s#.*#TOOLS_PATH=\"$TOOLS_PATH\"#" "$BASHRC"
        echo -e "${TAB}${IDOT}${YELLOW}${IWARN}Tools path is updated.${END_COLOR}"
    fi
    
    if [[ -n $old_main_source_line ]]; then
        local line=$(sed -n "${old_main_source_line}p" "$BASHRC")
        local identation="$(get_indentation $line)"
        
        sed -i "${old_main_source_line}s#.*#source \"$TOOLS_PATH\/main.sh\"#" "$BASHRC"
        echo -e "${TAB}${IDOT}${YELLOW}${IWARN}Main Tools source is updated.${END_COLOR}"
    fi
    
    if ! grep -q "TOOLS VARIABLES" "$BASHRC"; then
        echo -e "" >> "$BASHRC"
        echo -e "# [TOOLS VARIABLES]" >> "$BASHRC"
        echo -e "TOOLS_PATH=\"$TOOLS_PATH\"" >> "$BASHRC"
        echo -e "source \"$TOOLS_PATH/main.sh\"" >> "$BASHRC"
        echo -e "# [TOOLS VARIABLES]" >> "$BASHRC"
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Tools variables added.${END_COLOR}"
    else
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Tools variables set up.${END_COLOR}"
    fi
    
    source "$BASHRC"
    
    if ! [[ -d "$TOOLS_PATH/temp" ]]; then
        mkdir "$TOOLS_PATH/temp"
    fi
    if ! [[ -d "$TOOLS_PATH/temp/tools" ]]; then
        mkdir "$TOOLS_PATH/temp/tools"
    fi
    rm -rf "$TOOLS_PATH/temp/tools/*"
    
    local built_in_plugins=$(ls -l "$TOOLS_PATH/plugins" | grep "^d" | awk '{print $NF}')
    for plugin_name in "${built_in_plugins[@]}"; do
        rm -rf "$TOOLS_PATH/temp/tools/$plugin_name"
        rm -rf "$TOOLS_PATH/temp/$plugin_name"
        mv "$TOOLS_PATH/plugins/$plugin_name" "$TOOLS_PATH/temp/tools"
        
        tools add-plugin "$TOOLS_PATH/temp/tools/$plugin_name"
    done
    
    source "$BASHRC"
    
    return 0
}

tools-init $0