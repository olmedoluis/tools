function get_diff_blocks() {
    local  diff_blocks=()
    local diff_block=""
    
    while IFS= read -r line; do
        if [[ $line == diff* ]]; then
            if [ -n "$diff_block" ]; then
                diff_blocks+=("$diff_block")
            fi
            diff_block="$line\n"
        else
            diff_block="$diff_block$line\n"
        fi
    done < <(git diff)
    
    if [ -n "$diff_block" ]; then
        diff_blocks+=("$diff_block")
    fi
    
    echo "${diff_blocks[@]}"
}
