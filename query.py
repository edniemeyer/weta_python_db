#!/usr/bin/python

import sys, getopt, csv

def main(argv):
	select=''
	order=''
	filtr=''
	try:
		opts, args = getopt.getopt(argv,"s:f:o:")
	except getopt.GetoptError:
		print 'query.py -s <columns> -o <columns>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-s":
			select = arg
		elif opt == "-o":
			order = arg
		elif opt == "-f":
			filtr = arg
	with open("db.csv","r") as file:
		data = csv.DictReader(file, delimiter=",")
		if filtr!='':
			col,val=filtr.split("=")
			data=filter(lambda filtered: filtered[col] == val, data)
		if select!='':
			cols = select.split(",")
			for row in data:
				print {k: row[k] for k in cols}


if __name__ == "__main__":
   main(sys.argv[1:])


