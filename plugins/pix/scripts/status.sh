#!/bin/bash

function status() {
    source "$TOOLS_PATH/constants/colors.sh"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}${IERR}Not a git repository.${END_COLOR}"
        return 1
    fi
    
    local current_branch_name="$(git symbolic-ref --short -q HEAD)"
    local staged_files=($(git diff --cached --name-only))
    local modified_files=($(git diff --name-only))
    local untracked_files=($(git ls-files --others --exclude-standard))
    local conflicted_files=($(git diff --name-only --diff-filter=U))
    
    echo -e "${MAGENTA}${IBRCH}${current_branch_name}${END_COLOR}"
    if [[ ${#conflicted_files} != 0 ]]; then
        for file in "${conflicted_files[@]}"; do
            echo -e "${TAB}· ${BLUE}${ICONF}${file}${END_COLOR}"
        done
        
        return 0
    fi
    
    if [[ ${#staged_files} != 0 ]]; then
        for file in "${staged_files[@]}"; do
            echo -e "${TAB}· ${GREEN}${IADD}${file}${END_COLOR}"
        done
    fi
    
    if [[ ${#modified_files} != 0 ]]; then
        for file in "${modified_files[@]}"; do
            echo -e "${TAB}· ${YELLOW}${IMOD}${file}${END_COLOR}"
        done
    fi
    
    if [[ ${#untracked_files} != 0 ]]; then
        for file in "${untracked_files[@]}"; do
            echo -e "${TAB}· ${RED}${IUNTR}${file}${END_COLOR}"
        done
    fi
    
    if [[ ${#staged_files[@]} -eq 0 && ${#modified_files[@]} -eq 0 && ${#untracked_files[@]} -eq 0 ]]; then
        echo -e "${TAB}· ${GREEN}${IOK}Nothing to commit, working tree clean.${END_COLOR}"
    fi
}
