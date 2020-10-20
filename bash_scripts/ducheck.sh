CHECKDIR=${CHECKDIR:-"/Users/dbmoore"}
MINBYTES=${MINBYTES:-500000}
echo $CHECKDIR "...." $MINBYTES
du -k $CHECKDIR | awk '{if ($1 > 500000) printf "%9d ----> %s\n",$1,$2}'

