function get_indentation() {
    local value="$1"
    local indentation="${value%%[^[:space:]]*}"
    
    echo "$indentation"
    return 0
}

function replace() {
    local original="$1"
    local from="$2"
    local to="$3"
    
    echo "${original//$from/$to}"
}