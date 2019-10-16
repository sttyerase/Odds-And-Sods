## bash script to comb the output of the history command for invocations of a particular command, e.g., ssh.
## if no argument to this script is provided on the command line, the default execution searches
## for invocations of ssh.
## currently using this script in bash on Fedora 30 and MacOS.

TARG=${1:-"ssh"}  ## DEFAULT SEARCH IF NO $1
/usr/bin/clear
history | grep --color=auto "^...... $TARG"

