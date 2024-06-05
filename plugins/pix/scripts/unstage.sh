#!/bin/bash

function unstage() {
    source "$TOOLS_PATH/constants/colors.sh"
    source "$TOOLS_PATH/lib/user-interaction.sh"
    source "$TOOLS_PATH/lib/array.sh"
    source "$TOOLS_PATH/lib/number.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local files=($(git diff --cached --name-only))
    
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
        echo -e "${RED}${IERR}No files to unstage.${END_COLOR}"
        return 1
    fi
    
    if [[ ${#files[@]} == "${#matches[@]}" || ${#matches[@]} == 1 ]]; then
        echo -e "${IINFO}Unstaging files."
        for file in "${matches[@]}"; do
            git reset -- $file > /dev/null 2>&1
            echo -e "${TAB}${IDOT}${CYAN}${ILESS}$file${END_COLOR}."
        done
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}${#matches[@]} File(s) unstaged.${END_COLOR}"
        return 0
    fi
    if [[ ${#files[@]} == 1 && "$#" == 0 ]]; then
        echo -e "${IINFO}Unstaging files."
        for file in "${files[@]}"; do
            git reset -- $file > /dev/null 2>&1
            echo -e "${TAB}${IDOT}${CYAN}${ILESS}$file.${END_COLOR}"
        done
        
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}${#files[@]} File(s) unstaged.${END_COLOR}"
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
    local unstaged_files=()
    while [ true ]; do
        local colored_matches=()
        for file in "${matches[@]}"; do
            if some "$file" "${unstaged_files[@]}"; then
                colored_matches+=("${RED}$file${END_COLOR}")
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
                unstaged_files=("${matches[@]}")
                echo -e "${TAB}${GREEN}${ISTAR}${IOK}All files will be unstaged.${END_COLOR}"
                break
            ;;
            s)
                echo -e "${TAB}${GREEN}${ISTAR}${IOK}Selected files will be unstaged.${END_COLOR}"
                break
            ;;
            q)
                echo -e "${TAB}${YELLOW}${ISTAR}${IWARN}No files will be unstaged.${END_COLOR}"
                return 0
            ;;
            h)
                echo -e "${TAB}${ISTAR}${IINFO}Available options:"
                echo -e "${DTAB}${ISTAR}([number]): File option index."
                echo -e "${DTAB}${ISTAR}(a): Unstage all files."
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
                
                if some "$option" "${unstaged_files[@]}"; then
                    local new_unstaged_files=($(filter "$option" "${unstaged_files[@]}"))
                    
                    unstaged_files=("${new_unstaged_files[@]}")
                    echo -e "${TAB}${YELLOW}${ISTAR}${IOK}File will be ignored.${END_COLOR}"
                else
                    unstaged_files+=("$option")
                    echo -e "${TAB}${GREEN}${ISTAR}${IOK}File will be unstaged.${END_COLOR}"
                fi
            ;;
        esac
    done
    
    echo -e "${IINFO}Unstaging files."
    for file in "${unstaged_files[@]}"; do
        git reset -- $file > /dev/null 2>&1
        echo -e "${TAB}${IDOT}${CYAN}${ILESS}$file${END_COLOR}."
    done
    
    echo -e "${TAB}${ISTAR}${GREEN}${IOK}${#unstaged_files[@]} File(s) unstaged.${END_COLOR}"
}
