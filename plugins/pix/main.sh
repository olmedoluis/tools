#!/bin/bash

function pix() {
    local PLUGIN_PATH="$TOOLS_PATH/plugins/pix"
    local PLUGIN_TEMP_PATH="$TOOLS_PATH/temp/pix"
    local PLUGIN_CONFIG_PATH=$PLUGIN_PATH/config.json
    
    local sub_command=$1
    
    case $sub_command in
        status)
            source "$PLUGIN_PATH/scripts/status.sh"
            
            status ${@:2}
        ;;
        
        stash-in)
            source "$PLUGIN_PATH/scripts/stash-in.sh"
            
            stash-in ${@:2}
        ;;
        
        stage)
            source "$PLUGIN_PATH/scripts/stage.sh"
            
            stage ${@:2}
        ;;
        
        undo)
            source "$PLUGIN_PATH/scripts/undo.sh"
            
            undo ${@:2}
        ;;
        
        stash-pop)
            source "$PLUGIN_PATH/scripts/stash-pop.sh"
            
            stash-pop ${@:2}
        ;;
        
        branch)
            source "$PLUGIN_PATH/scripts/branch.sh"
            
            branch "$PLUGIN_CONFIG_PATH" ${@:2}
        ;;
        
        examinate)
            source "$PLUGIN_PATH/scripts/examinate.sh"
            
            examinate $PLUGIN_TEMP_PATH ${@:2}
        ;;
        
        commit)
            source "$PLUGIN_PATH/scripts/commit.sh"
            
            commit "$PLUGIN_CONFIG_PATH" ${@:2}
        ;;
        
        unstage)
            source "$PLUGIN_PATH/scripts/unstage.sh"
            
            unstage ${@:2}
        ;;
        
        *)
            source "$TOOLS_PATH/constants/colors.sh"
            
            echo -e "${RED}${IERR}Unknown route.${END_COLOR}"
        ;;
    esac
}
