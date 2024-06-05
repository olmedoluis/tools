#!/bin/bash

show_options() {
    for (( i=1; i<=$#; i++ )); do
        echo -e "${DTAB}$i. ${!i}"
    done
}