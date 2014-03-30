test: oneyear firstplace.net
	./oneyear | sort -n

oneyear: oneyear.c
	gcc oneyear.c -lfann -o oneyear

oneyear.c: oneyear.py ../dat/Teams.csv
	tail -n +2 ../dat/Teams.csv | ./oneyear.py > t
	mv t oneyear.c

firstplace.net: firstplace.dat firstplace
	./firstplace

firstplace.dat: ../dat/Teams.csv extract_data.py
	tail -n +2 ../dat/Teams.csv | ./extract_data.py > t
	mv t firstplace.dat

../dat/Teams.csv: ../dat/lahman-csv_2014-02-14.tgz
	(cd ../dat ; tar xf ../dat/lahman-csv_2014-02-14.tgz Teams.csv)

firstplace: firstplace.c
	gcc firstplace.c -lfann -o firstplace

xor: xor.c
	gcc xor.c -lfann -o xor

clean:
	rm -f oneyear
	rm -f firstplace
	rm -f xor
	rm -f oneyear.c
	rm -rf *.net
	rm -rf *.dat
