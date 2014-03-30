results: ../results/2013-prediction.txt \
		../results/2012-prediction.txt \
		../results/2011-prediction.txt

../results/2013-prediction.txt: 2013 firstplace.net
	./2013 | sort -n > t
	mv t ../results/2013-prediction.txt 

2013: 2013.c
	gcc 2013.c -lfann -o 2013

2013.c: oneyear.py ../dat/Teams.csv extract_data.py
	tail -n +2 ../dat/Teams.csv | ./oneyear.py 2013 > t
	mv t 2013.c

../results/2012-prediction.txt: 2012 firstplace.net
	./2012 | sort -n > t
	mv t ../results/2012-prediction.txt 

2012: 2012.c
	gcc 2012.c -lfann -o 2012

2012.c: oneyear.py ../dat/Teams.csv extract_data.py
	tail -n +2 ../dat/Teams.csv | ./oneyear.py 2012 > t
	mv t 2012.c

../results/2011-prediction.txt: 2011 firstplace.net
	./2011 | sort -n > t
	mv t ../results/2011-prediction.txt 

2011: 2011.c
	gcc 2011.c -lfann -o 2011

2011.c: oneyear.py ../dat/Teams.csv extract_data.py
	tail -n +2 ../dat/Teams.csv | ./oneyear.py 2011 > t
	mv t 2011.c

firstplace.net: firstplace.dat firstplace
	./firstplace

firstplace.dat: ../dat/Teams.csv extract_data.py
	tail -n +2 ../dat/Teams.csv | ./extract_data.py > t
	mv t firstplace.dat

../dat/Teams.csv: ../dat/lahman-csv_2014-02-14.tgz
	(cd ../dat ; tar xf ../dat/lahman-csv_2014-02-14.tgz Teams.csv)
	touch ../dat/lahman-csv_2014-02-14.tgz

firstplace: firstplace.c
	gcc firstplace.c -lfann -o firstplace

xor: xor.c
	gcc xor.c -lfann -o xor

clean:
	rm -f 2012
	rm -f 2012.c
	rm -f 2013
	rm -f 2013.c
	rm -f firstplace
	rm -f xor
	rm -rf *.net
	rm -rf *.dat
