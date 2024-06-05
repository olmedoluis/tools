#!/bin/bash

function stage() {
    source "$TOOLS_PATH/constants/colors.sh"
    source "$TOOLS_PATH/lib/user-interaction.sh"
    source "$TOOLS_PATH/lib/array.sh"
    source "$TOOLS_PATH/lib/number.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local files=($(git diff --name-only) $(git ls-files --others --exclude-standard) $(git diff --name-only --diff-filter=U))
    
    local matches=()
    if [[ ${#files} != 0 ]]; then
        for file in "${files[@]}"; do
            for file_pattern in $@; do
                if [[ "${file}" =~ "${file_pattern}" ]]; then
                    matches+=("$file")
                    break
                fi
            done
        done
    else
        echo -e "${RED}${IERR}No files to stage.${END_COLOR}"
        return 1
    fi
    
    if [[ ${#files[@]} == "${#matches[@]}" || ${#matches[@]} == 1 ]]; then
        echo -e "${IINFO}Staging files."
        for file in "${matches[@]}"; do
            git add -- $file > /dev/null 2>&1
            echo -e "${TAB}${IDOT}${CYAN}${IADD}$file.${END_COLOR}"
        done
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}${#matches[@]} File(s) staged.${END_COLOR}"
        return 0
    fi
    if [[ ${#files[@]} == 1 && "$#" == 0 ]]; then
        echo -e "${IINFO}Staging files."
        for file in "${files[@]}"; do
            git add -- $file > /dev/null 2>&1
            echo -e "${TAB}${IDOT}${CYAN}${IADD}$file.${END_COLOR}"
        done
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}${#files[@]} File(s) staged.${END_COLOR}"
        return 0
    fi
    
    if [[ "$#" == 0 ]]; then
        matches+=("${files[@]}")
    fi
    if [[ "${#matches[@]}" == 0 ]]; then
        echo -e "${RED}${IERR}File matches not found.${END_COLOR}"
        return 1
    fi
    
    echo -e "${IINFO}Selection of files needed."
    local staged_files=()
    while [ true ]; do
        local colored_matches=()
        for file in "${matches[@]}"; do
            if some "$file" "${staged_files[@]}"; then
                colored_matches+=("${GREEN}$file${END_COLOR}")
            else
                colored_matches+=("$file")
            fi
        done
        
        local option=""
        echo -e "${TAB}${ISTAR}${BLUE}${IINFO}Please choose an option ([number]/a/s/q/h):${END_COLOR}"
        show_options "${colored_matches[@]}"
        read -p $"${TAB}${IDOT}${IINP}" option
        
        case $option in
            a)
                staged_files=("${matches[@]}")
                echo -e "${TAB}${GREEN}${ISTAR}${IOK}All files will be staged.${END_COLOR}"
                break
            ;;
            s)
                echo -e "${TAB}${GREEN}${ISTAR}${IOK}Selected files will be staged.${END_COLOR}"
                break
            ;;
            q)
                echo -e "${TAB}${YELLOW}${ISTAR}${IWARN}No files will be staged.${END_COLOR}"
                return 0
            ;;
            h)
                echo -e "${TAB}${ISTAR}${IINFO}Available options:"
                echo -e "${DTAB}${ISTAR}([number]): File option index."
                echo -e "${DTAB}${ISTAR}(a): Stage all files."
                echo -e "${DTAB}${ISTAR}(s): Save."
                echo -e "${DTAB}${ISTAR}(q): Leave."
                echo -e "${DTAB}${ISTAR}(h): Help me."
                continue
            ;;
            *)
                if ! is_number "$option"; then
                    echo -e "${TAB}${RED}${ISTAR}${IERR}Unknown option.${END_COLOR}"
                    return 1
                fi
                
                option=${matches[((--option))]}
                
                if ! some "$option" "${matches[@]}"; then
                    echo -e "${TAB}${RED}${ISTAR}${IERR}Unknown option.${END_COLOR}"
                    return 1
                fi
                
                if some "$option" "${staged_files[@]}"; then
                    local new_staged_files=($(filter "$option" "${staged_files[@]}"))
                    
                    staged_files=("${new_staged_files[@]}")
                    echo -e "${TAB}${YELLOW}${ISTAR}${IOK}File will be ignored.${END_COLOR}"
                else
                    staged_files+=("$option")
                    echo -e "${TAB}${GREEN}${ISTAR}${IOK}File will be staged.${END_COLOR}"
                fi
            ;;
        esac
    done
    
    echo -e "${IINFO}Staging files."
    for file in "${staged_files[@]}"; do
        git add -- $file > /dev/null 2>&1
        echo -e "${TAB}${IDOT}${CYAN}${IADD}$file${END_COLOR}."
    done
    
    echo -e "${TAB}${ISTAR}${GREEN}${IOK}${#staged_files[@]} File(s) staged.${END_COLOR}"
}
