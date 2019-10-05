## bash script to comb the command history for executions of a particular command, e.g., ssh.
## default execution searches for invocations of ssh.
## 

TARG=${1:-"ssh"}
/usr/bin/clear
history | grep --color=auto "^...... $TARG "

