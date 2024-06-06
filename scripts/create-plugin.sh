function create-plugin() {
    source "$TOOLS_PATH/constants/colors.sh"
    
    local plugin_name="$1"
    
    if [[ -z "$plugin_name" ]]; then
        echo -e "${RED}${IERR}Missing plugin name.${END_COLOR}"
        return 1
    fi
}