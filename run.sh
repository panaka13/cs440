#!/bin/bash
for i in {1..100}
do
	cmd="python3.7 Main.py"
	$cmd >> output.txt
	echo $i
done
