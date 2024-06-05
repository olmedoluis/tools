#!/bin/bash

function read_json_value(){
    local file_path="$1"
    local from="$2"
    
    local raw_value=$(cat $file_path | jq -r ".$from")
    local raw_value_sanitazed="$(echo "$raw_value")"
    
    echo "$raw_value_sanitazed"
}

function read_json_array(){
    local file_path="$1"
    local from="$2"
    
    local raw_array=($(cat $file_path | jq -r ".$from"))
    
    for item in "${raw_array[@]}"; do
        local item_sanitazed="$(echo "$item")"
        
        echo "$item_sanitazed"
    done
}

function read_json_object_keys(){
    local file_path="$1"
    local from="$2"
    
    local raw_keys=($(cat $file_path | jq -r ".$from | keys_unsorted[]"))
    
    for raw_key in "${raw_keys[@]}"; do
        local raw_key_sanitazed="$(echo "$raw_key")"
        
        echo "$raw_key_sanitazed"
    done
}

function read_json_object_values(){
    local file_path="$1"
    local from="$2"
    
    local raw_values=($(cat $file_path | jq -r ".$from | values[]"))
    
    for raw_value in "${raw_values[@]}"; do
        local raw_value_sanitazed="$(echo "$raw_value")"
        
        echo "$raw_value_sanitazed"
    done
}