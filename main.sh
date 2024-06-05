#!/bin/bash

source "$TOOLS_PATH/plugins/init.sh"

function tools() {
    local sub_command=$1
    
    case $sub_command in
        add-plugin)
            source $TOOLS_PATH/scripts/add-plugin.sh
            
            add-plugin ${@:2}
        ;;
        
        *)
            source $TOOLS_PATH/constants/colors.sh
            
            echo -e "${RED}${IERR}Unknown route.${END_COLOR}"
        ;;
    esac
}
