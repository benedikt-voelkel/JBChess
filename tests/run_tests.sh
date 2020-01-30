#!/bin/bash -e

set -o pipefail


[[ $# == 0 ]] && { echo "ERROR: Arguments required"; exit 1; }

FILES=
CURRENT_ARG=
TESTS=


while [[ $# -gt 0 ]]
do
    case "$1" in
        pylint)
            TESTS+="test-pylint "
            CURRENT_ARG=
            ;;
        --files)
            CURRENT_ARG="files"
            ;;
        *)
            if [[ "$CURRENT_ARG" == "files" ]]
            then
                FILES+="$1 "
                TESTS+="blah "
            else
                echo "ERROR: Unkown argument $1"
                exit 1
            fi
    esac
    shift
done

for t in $TESTS
do
    echo
    echo "TEST $t"
    echo
    for f in $FILES
    do
        echo "$f"
    done
    echo
done
