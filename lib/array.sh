function some {
    local search="$1"
    local array=("${@:2}")
    
    for value in "${array[@]}"; do
        if [[ "$value" == "$search" ]]; then
            return 0
        fi
    done
    
    return 1
}

function filter {
    local search="$1"
    local array=("${@:2}")
    local new_array=()
    
    for value in "${array[@]}"; do
        if [[ "$value" != "$search" ]]; then
            new_array+=("$value")
        fi
    done
    
    echo "${new_array[@]}"
}