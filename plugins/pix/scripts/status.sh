#!/bin/bash

function status() {
    source "$TOOLS_PATH/constants/colors.sh"
    source "$TOOLS_PATH/lib/array.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local current_branch_name="$(git symbolic-ref --short -q HEAD)"
    local staged_files=($(git diff --cached --name-only))
    local modified_files=($(git diff --name-only))
    local untracked_files=($(git ls-files --others --exclude-standard))
    local conflicted_files=($(git diff --name-only --diff-filter=U))
    local renamed_files=($(git status -s | grep -oP "^R\s+.+?\s->\s\K.+$"))
    
    echo -e "${MAGENTA}${IBRCH}${current_branch_name}${END_COLOR}"
    if [[ ${#conflicted_files} != 0 ]]; then
        for file in "${conflicted_files[@]}"; do
            echo -e "${TAB}${IDOT}${BLUE}${ICONF}${file}${END_COLOR}"
        done
        
        return 0
    fi
    
    if [[ ${#staged_files} != 0 ]]; then
        if [[ -n $renamed_files ]]; then
            local original_renamed_files=($(git status -s | grep -oP "^R\s+\K.+?(?=\s+->)"))
            local renamed_files_index=0
        fi
        
        for file in "${staged_files[@]}"; do
            if some "$file" "${renamed_files[@]}"; then
                local original_file="${original_renamed_files[renamed_files_index]}"
                
                local prefix_length=0
                for (( i=0; i<${#original_file} && i<${#file}; i++ )); do
                    if [[ ${original_file:i:1} == ${file:i:1} ]]; then
                        (( prefix_length++ ))
                    else
                        break
                    fi
                done
                
                local static_file_part="${original_file:0:prefix_length}"
                local modified_file_part="${file:prefix_length}"
                
                echo -e "${TAB}${IDOT}${GREEN}${IRNM}${static_file_part}${YELLOW}${modified_file_part}${END_COLOR}"
                (( renamed_files_index++ ))
                
                continue
            fi
            
            echo -e "${TAB}${IDOT}${GREEN}${IADD}${file}${END_COLOR}"
        done
    fi
    
    if [[ ${#modified_files} != 0 ]]; then
        for file in "${modified_files[@]}"; do
            echo -e "${TAB}${IDOT}${YELLOW}${IMOD}${file}${END_COLOR}"
        done
    fi
    
    if [[ ${#untracked_files} != 0 ]]; then
        for file in "${untracked_files[@]}"; do
            echo -e "${TAB}${IDOT}${RED}${IUNTR}${file}${END_COLOR}"
        done
    fi
    
    if [[ ${#staged_files[@]} -eq 0 && ${#modified_files[@]} -eq 0 && ${#untracked_files[@]} -eq 0 ]]; then
        echo -e "${TAB}${ISTAR}${GREEN}${IOK}Nothing to commit, working tree clean.${END_COLOR}"
    fi
}
