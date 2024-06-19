#!/bin/bash

function examinate() {
    source "$TOOLS_PATH/constants/colors.sh"
    
    local PLUGIN_TEMP_PATH=$1
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local file_paths=()
    local start_lines=()
    local code_blocks=()
    local code_block=""
    
    local colored_code_blocks=()
    local colored_code_block=""
    
    local metadata_blocks_per_patch=()
    local metadata_blocks=()
    local metadata_block=""
    
    local line=""
    
    local is_code="false"
    local last_file_path=""
    while IFS= read -r line; do
        line="${line//\\/\\\\}"
        
        if [[ $line =~ ^diff ]]; then
            is_code="false"
            
            if [ -n "$code_block" ]; then
                code_blocks+=("$code_block")
            fi
            if [ -n "$colored_code_block" ]; then
                colored_code_blocks+=("$colored_code_block")
            fi
            
            if [ -n "$metadata_block" ]; then
                metadata_blocks+=("$metadata_block")
            fi
            
            last_file_path="$(echo "$line" | awk '{print $3}')"
            file_paths+=("${last_file_path}")
            code_block=""
            colored_code_block=""
            metadata_block="$line\n"
            continue
        fi
        
        if [[ $line =~ ^@@ && $is_code == "false" ]]; then
            local formatted_line="${line/@@ [+|-][0-9]+,[0-9]+ [+|-][0-9]+,[0-9]+ @@/}"
            is_code="true"
            local second_field="${line#* }"
            local start_line="${second_field%%,*}"
            
            metadata_blocks_per_patch+=("$metadata_block")
            start_lines+=("$start_line")
            
            code_block="$line\n"
            continue
        fi
        
        if [[ $line =~ ^@@ && $is_code == "true" ]]; then
            local formatted_line="${line/@@ [+|-][0-9]+,[0-9]+ [+|-][0-9]+,[0-9]+ @@/}"
            local second_field="${line#* }"
            local start_line="${second_field%%,*}"
            
            start_lines+=("$start_line")
            file_paths+=("${last_file_path}")
            code_blocks+=("$code_block")
            colored_code_blocks+=("$colored_code_block")
            metadata_blocks_per_patch+=("$metadata_block")
            
            code_block="$line\n"
            colored_code_block=""
            continue
        fi
        
        if [[ $line =~ ^\+ && $is_code == "true" ]]; then
            local formatted_line=${line#"+"}
            
            code_block="$code_block$line\n"
            colored_code_block="$colored_code_block${TAB}${GREEN}${IPLUS}$formatted_line${END_COLOR}\n"
            continue
        fi
        if [[ $line =~ ^- && $is_code == "true" ]]; then
            local formatted_line=${line#"-"}
            
            code_block="$code_block$line\n"
            colored_code_block="$colored_code_block${TAB}${RED}${ILESS}$formatted_line${END_COLOR}\n"
            continue
        fi
        if [ $is_code == "true" ]; then
            code_block="$code_block$line\n"
            colored_code_block="$colored_code_block${TAB}·$line\n"
            continue
        fi
        
        if [ $is_code == "false" ]; then
            metadata_block+="$line\n"
        fi
    done < <(git diff-files -p)
    
    if [ -n "$metadata_block" ]; then
        metadata_blocks+=("$metadata_block")
    else
        echo -e "${RED}${IERR}No files to examinate.${END_COLOR}"
        return 1
    fi
    
    if [ -n "$code_block" ]; then
        code_blocks+=("$code_block")
    fi
    if [ -n "$colored_code_block" ]; then
        colored_code_blocks+=("$colored_code_block")
    fi
    
    local rest_of_path_staged=""
    local rest_of_path_ignored=""
    local has_quit="false"
    local staged_patch=""
    local ignored_patch=""
    local index=0
    for colored_code_block in "${colored_code_blocks[@]}"; do
        colored_code_block="${colored_code_block%\\n}"
        
        local file_path_raw="${file_paths[index]}"
        local start_line_raw="${start_lines[index]}"
        local metadata_block="${metadata_blocks_per_patch[index]}"
        local code_block="${code_blocks[index]}"
        
        local file_path=${file_path_raw#*/}
        local start_line=${start_line_raw#-}
        
        if [[ $rest_of_path_ignored == $file_path || $has_quit == "true" ]]; then
            ignored_patch+="$metadata_block$code_block"
            ((index++))
            continue
        fi
        if [[ $rest_of_path_staged == $file_path ]]; then
            staged_patch+="$metadata_block$code_block"
            ((index++))
            continue
        fi
        
        echo -e "${IINFO}On ${CYAN}${INEWS}$file_path:$start_line${END_COLOR}"
        echo -e "${TAB}·"
        echo -e "$colored_code_block"
        echo -e "${TAB}·"
        
        while [ true ]; do
            local validation=""
            echo -e "${TAB}${ISTAR}${BLUE}${IINFO}Stage this hunk? (y/n/a/d/s/q/h)${END_COLOR}"
            read -p $"${TAB}${IDOT}${IINP}" validation
            
            case $validation in
                y)
                    staged_patch+="$metadata_block$code_block"
                    echo -e "${TAB}${GREEN}${ISTAR}${IOK}Hunk will be staged.${END_COLOR}"
                ;;
                n)
                    ignored_patch+="$metadata_block$code_block"
                    echo -e "${TAB}${YELLOW}${ISTAR}${IWARN}Hunk will be ignored.${END_COLOR}"
                ;;
                a)
                    staged_patch+="$metadata_block$code_block"
                    rest_of_path_staged=$file_path
                    echo -e "${TAB}${GREEN}${ISTAR}${IWARN}Rest of hunks in file will be staged.${END_COLOR}"
                ;;
                d)
                    ignored_patch+="$metadata_block$code_block"
                    rest_of_path_ignored=$file_path
                    echo -e "${TAB}${YELLOW}${ISTAR}${IWARN}Rest of hunks in file will be ignored.${END_COLOR}"
                ;;
                s)
                    ignored_patch+="$metadata_block$code_block"
                    has_quit="true"
                    echo -e "${TAB}${GREEN}${ISTAR}${IOK}Selected hunks will be staged.${END_COLOR}"
                    break
                ;;
                q)
                    echo -e "${TAB}${YELLOW}${ISTAR}${IWARN}No hunks will be staged.${END_COLOR}"
                    return 0
                ;;
                h)
                    echo -e "${TAB}${ISTAR}${IINFO}Available options:"
                    echo -e "${DTAB}${ISTAR}(y): Stage hunk."
                    echo -e "${DTAB}${ISTAR}(n): Ignore hunk."
                    echo -e "${DTAB}${ISTAR}(a): Stage rest of hunks in file."
                    echo -e "${DTAB}${ISTAR}(d): Ignore rest of hunks in file."
                    echo -e "${DTAB}${ISTAR}(s): Save."
                    echo -e "${DTAB}${ISTAR}(q): Leave."
                    echo -e "${DTAB}${ISTAR}(h): Help me."
                    continue
                ;;
                *)
                    echo -e "${TAB}${RED}${ISTAR}${IERR}Unknown option.${END_COLOR}"
                    return 1
                ;;
            esac
            
            break
        done
        
        ((index++))
    done
    
    if [ -n "$staged_patch" ]; then
        git checkout . > /dev/null 2>&1
        echo -e "$staged_patch" > $PLUGIN_TEMP_PATH/.patch
        git apply $PLUGIN_TEMP_PATH/.patch > /dev/null 2>&1
        
        local modified_files=($(git diff --name-only))
        git add "${modified_files[@]}" > /dev/null 2>&1
        
        if [ -n "$ignored_patch" ]; then
            echo -e "$ignored_patch" > $PLUGIN_TEMP_PATH/.patch
            git apply $PLUGIN_TEMP_PATH/.patch > /dev/null 2>&1
        fi
        
        rm $PLUGIN_TEMP_PATH/.patch
        echo -e "${TAB}${GREEN}${ISTAR}${IOK}${#modified_files[@]} file(s) staged.${END_COLOR}"
    else
        echo -e "${TAB}${YELLOW}${ISTAR}${IWARN}No files has been staged.${END_COLOR}"
    fi
}
