#!/bin/bash
if [ $# -eq 1 ]
then
	flake8 $1  > flake8.tmp
	mate $1 --clear-mark error
	while read p; do
		line="$(echo "$p" | cut -f 2- -d ':' | cut -f -2 -d ':')"
		mate $1 --line $line --set-mark error:"$p"
	done <flake8.tmp
	if [[ $(wc -l <flake8.tmp) -ge 2 ]]
	then
		mate $1
	else
		echo $1 has no style warnings
	fi
	rm flake8.tmp
else
	echo "marks all flake8 style warnings in file for viewing in textmate"
	echo usage: ./flake8.sh file.py
fi
