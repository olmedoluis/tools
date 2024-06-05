function get_indentation() {
    local value="$1"
    local indentation="${value%%[^[:space:]]*}"
    
    echo "$indentation"
    return 0
}
