#!/bin/sh

##### STANDARD SET OF SHELL ROUTINES USEFUL FOR CALLING WITHIN A SHELL SCRIPT OR SCRIPTS
#
# USAGE:	. <full path>/standard_routines.sh
#
		#ESTABLISH SHELL CONFIGURATION VARIABLES

if [ -z "$SHELL_ID" ]
   then SHELL_ID=`basename $0`  ; export SHELL_ID
fi
THIS_SHELL=`basename $0`

      #ESTABLISH LOG_FILE VARIABLE AND ORDER OF PREFERENCE
      #  1. Put in $HOME/log directory.
      #  2. Put in working directory.
      #  3. Application overrides and specifies directory using environment setting.

if [ -z "$LOG_FILE" ]
   then LOG_FILE=`echo $SHELL_ID | sed -e 's/\.[A-Z,a-z]*$//' -e 's/$/.log/' `
   if [ -d $HOME/log ]
      then LOG_FILE="$HOME/log/$LOG_FILE"
      else LOG_FILE="$HOME/$LOG_FILE"
   fi
fi
export LOG_FILE

THIS_LOG=`echo $THIS_SHELL | sed -e 's/\.[A-Z,a-z]*$//' -e 's/$/.log/' `
if [ -d $HOME/log ]
   then THIS_LOG="$HOME/log/$THIS_LOG"
   else THIS_LOG="$HOME/$THIS_LOG"
fi

      #ESTABLISH INI_FILE VARIABLE AND ORDER OF PREFERENCE
      #  1. Put in $HOME/ini directory
      #  2. Put in working directory
      #  3. Application overrides and specifies directory

if [ -z "$INI_FILE" ]
   then INI_FILE=`echo $SHELL_ID | sed -e 's/\.[A-Z,a-z]*$//' -e 's/$/.ini/' `
   if [ -d $HOME/ini ]
      then INI_FILE="$HOME/ini/$INI_FILE"
      else INI_FILE="$HOME/$INI_FILE"
   fi
fi
export INI_FILE

THIS_INI=`echo $THIS_SHELL | sed -e 's/\.[A-Z,a-z]*$//' -e 's/$/.ini/' `
if [ -d $HOME/ini ]
   then THIS_INI="$HOME/ini/$THIS_INI"
   else THIS_INI="$HOME/ini/$THIS_INI"
fi

      #CREATE STANDARD FILE NAME and LOCATION FOR OUTPUT REDIRECT
      #  1. Put in $HOME/log directory or
      #  2. Put in $HOME or
      #  3. Application overrides and specifies directory

if [ -z "$OUTPUT_FILE" ]
   then OUTPUT_FILE=`echo $SHELL_ID | sed -e 's/\.[A-Z,a-z]*$//' -e 's/$/.stdout/' `
   if [ -d $HOME/log ]
      then OUTPUT_FILE="$HOME/log/$OUTPUT_FILE"
      else OUTPUT_FILE="$HOME/$OUTPUT_FILE"
   fi
fi
export OUTPUT_FILE

      #CREATE STANDARD FILE NAME and LOCATION FOR DATA STORAGE FILE
      #  1. Put in $HOME/data directory or
      #  2. Put in $HOME or
      #  3. Application overrides and specifies directory

if [ -z "$DATA_FILE" ]
   then DATA_FILE=`echo $SHELL_ID | sed -e 's/\.[A-Z,a-z]*$//' -e 's/$/.dat/' `
   if [ -d $HOME/data ]
      then DATA_FILE="$HOME/log/$DATA_FILE"
      else DATA_FILE="$HOME/$DATA_FILE"
   fi
fi
export DATA_FILE

CONDITION=NORMAL
OSVER=`uname -r | cut -c1-3`
if [ $OSVER -gt 4 ]  #ADD /usr/ucb TO END OF PATH
   then PATH="$PATH:/usr/ucb"
        export PATH
fi
DATECMD="date '+%y/%m/%d %T'"
SERVER=`uname -n`
USERNAME=`whoami`
MAIL_LIST=$USERNAME

# Define APP_HOME ... home directory of the application invocation

RUN_DIR=`dirname $0`
if [ "${RUN_DIR}" = "." ]
then
  CURR_PATH=`pwd`
else
  cd ${RUN_DIR}
  CURR_PATH=`pwd`
fi
field1=`echo $CURR_PATH|cut -d'/' -f2`
field2=`echo $CURR_PATH|cut -d'/' -f3`
field3=`echo $CURR_PATH|cut -d'/' -f4`
case "${field1}" in
  "home"|"vol"|"supp"|"devl"|"alpha"|"beta"|"prod") base=$field1
                                                    app=$field2;;
                                                 *) base=$field2
						    app=$field3;;
esac
APP_HOME="/${base}/${app}";     export APP_HOME

                # DECLARE COMMON SUBROUTINES

cleanup()
{
echo "`eval $DATECMD`-${SHELL_ID}:${THIS_SHELL}-CLEANING UP and EXITING....${CONDITION}" >> $LOG_FILE
}

trap 'CONDITION=KILLED;cleanup;exit 5' 1 2 3 15


# This routine mails a message
# The only parameter it takes is the message to mail
# It requires the variable MAIL_LIST in the environment
# to hold a list of ids to receive email messages.
 
MailMessage ()
{
if [ -n "$MAIL_LIST" ]
   then echo "`eval $DATECMD`-${SHELL_ID}:${THIS_SHELL}-($$)-$1" | mail -s "Message from $SHELL_ID." $MAIL_LIST
   else LogMessage "List of ids not defined in environment variable MAIL_LIST. Cannot send message."
fi
}
 

# This routine logs messages to the log file
# The only parameter it takes is the message to put in the log file
 
LogMessage ()  ### GLOBAL LOG FILE FOR INITIAL CALLING SCRIPT
{
   echo "`eval $DATECMD`-${SHELL_ID}:${THIS_SHELL}-($$)-$1" >> $LOG_FILE
}

ThisLog()  ### LOCAL LOG FILE FOR THIS SHELL SCRIPT
{
   echo "`eval $DATECMD`-${SHELL_ID}:${THIS_SHELL}-($$)-$1" >> $THIS_LOG
}

Usage()
{
   echo "$THIS_SHELL $1"
}
