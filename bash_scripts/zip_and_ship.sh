#! /bin/bash

USAGE="
   Usage: `basename $0` -m <dest machine> -s <source dir> -d <dest directory> 
"
## INITIAL ENVIRONMENT
DEBUG=${DEBUG:-"false"}
CURRENT_DIR=`pwd`
SOURCE_DIR=${SOURCE_DIR:-`pwd` }
DIR_NAME=`basename $SOURCE_DIR`
OUTPUT_FILE_NAME="${DIR_NAME}`date +'%Y%m%d'`.tgz"
DEST_MACHINE=
DEST_DIR=

## PARSE COMMAND LINE OPTIONS
while getopts ":s:d:m:" opt; do
    case "${opt}" in
        s)
        SOURCE_DIR=$OPTARG
        ;;
        m)
        DEST_MACHINE=$OPTARG
        ;;
        d)
        DEST_DIR=$OPTARG
        ;;
    esac
done
DEST_URI="${DEST_MACHINE}:${DEST_DIR}"

## IF DEBUG PRINT OUT INITIAL VARIABLE VALUES
if [ $DEBUG = "true" ]
    then printf "CURRENT:               $CURRENT_DIR
SOURCE DIRECTORY:      $SOURCE_DIR
DESTINATION MACHINE:   $DEST_MACHINE
DESTINATION DIRECTORY: $DEST_DIR
DESTINATION URI:       $DEST_URI
TARGET FILE NAME:      $OUTPUT_FILE_NAME
"
fi

## TEST VARIABLE VALUES AND EXIT IF INCORRECT
if [ "$DEST_MACHINE" = "" ]; then echo "DESTINATION MACHINE UNDEFINED: $DEST_MACHINE. Exiting now. " ; echo $USAGE ; exit 2; fi
if [ "$DEST_DIR" = "" ]; then echo "DESTINATION DIRECTORY UNDEFINED: $DEST_DIR. Exiting now. " ; echo $USAGE ; exit 3; fi

## CREATE ARCHIVE AND SHIP TO REMOTE SYSTEM
tar tgzf $OUTPUT_FILE_NAME $SOURCE_DIR
scp $OUTPUT_FILE_NAME $DEST_URI


