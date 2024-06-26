function create-plugin() {
    source "$TOOLS_PATH/constants/colors.sh"
    source "$TOOLS_PATH/lib/array.sh"
    source "$TOOLS_PATH/lib/string.sh"
    
    local plugin_names_taken=$(ls -l "$TOOLS_PATH/plugins" | grep "^d" | awk '{print $NF}')
    local plugin_name=""
    echo -e "${TAB}${ISTAR}${BLUE}${IINFO}Please type a name ([string]):${END_COLOR}"
    read -p $"${TAB}${IDOT}${IINP}" plugin_name
    
    if some "$plugin_name" "${plugin_names_taken[@]}" || command -v $plugin_name &> /dev/null; then
        echo -e "${TAB}${ISTAR}${RED}${IERR}Name already taken.${END_COLOR}"
        return 1
    else
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Name is available.${END_COLOR}"
    fi
    
    echo -e "${IINFO}Setting up files."
    local TEMP_DIR="$(pwd)"
    
    local plugin_dir="$TEMP_DIR/$plugin_name"
    local plugin_scripts_dir="$plugin_dir/scripts"
    local plugin_temp_dir="$plugin_dir/temp"
    
    local plugin_json_path="$plugin_dir/config.json"
    local plugin_main_path="$plugin_dir/main.sh"
    local plugin_script_test_path="$plugin_scripts_dir/test.sh"
    
    local slash="/"
    local normal_slash="\/"
    
    echo -e "${TAB}${IDOT}${IINFO}Creating folders."
    mkdir -p "$plugin_dir"
    mkdir -p "$plugin_scripts_dir"
    mkdir -p "$plugin_temp_dir"
    
    echo -e "${TAB}${IDOT}${IINFO}Copying templates."
    cat "$TOOLS_PATH/templates/config_json.template" > "$plugin_json_path"
    cat "$TOOLS_PATH/templates/main_sh.template" > "$plugin_main_path"
    cat "$TOOLS_PATH/templates/script_test.template" > "$plugin_script_test_path"
    
    echo -e "${TAB}${IDOT}${IINFO}Completing templates."
    sed -i "s/{plugin_name}/$(replace "$plugin_name" $slash  $normal_slash)/g" "$plugin_json_path"
    sed -i "s/{plugin_name}/$(replace "$plugin_name" $slash  $normal_slash)/g" "$plugin_main_path"
    sed -i "s/{plugin_dir}/$(replace "$plugin_dir" $slash  $normal_slash)/g" "$plugin_main_path"
    sed -i "s/{plugin_temp_dir}/$(replace "$plugin_temp_dir" $slash  $normal_slash)/g" "$plugin_main_path"
    sed -i "s/{plugin_json_path}/$(replace "$plugin_json_path" $slash  $normal_slash)/g" "$plugin_main_path"
    
    echo -e "${TAB}${ISTAR}${GREEN}${IOK}Plugin created.${END_COLOR}"
}