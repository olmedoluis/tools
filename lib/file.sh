function get_file_number() {
    local file_path="$1"
    local search="$2"
    
    local result="$(grep -nE "$search" "$file_path" | cut -d: -f1 | tail -n 1)"
    
    if [[ -z "$result" ]]; then
        return 1
    else
        echo "$result"
    fi
}