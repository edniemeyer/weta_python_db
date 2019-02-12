#!/usr/bin/python

import sys, getopt, csv

from operator import itemgetter

from itertools import groupby

def main(argv):
	select=''
	order=''
	filtr=''
	groupBy=''
	try:
		opts, args = getopt.getopt(argv,"s:f:o:g:")
	except getopt.GetoptError:
		print 'query.py -s <columns> -o <columns> -f <column>=<value>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-s":
			select = arg
		elif opt == "-o":
			order = arg
		elif opt == "-f":
			filtr = arg
		elif opt == "-g":
			groupBy = arg
	with open("db.csv","r") as file:
		data = csv.DictReader(file, delimiter=",")
		data = list(data)
		result = []

		if order!='':
			cols = order.split(",")
			data.sort(key=itemgetter(*cols))
		if filtr!='':
			col,val = filtr.split("=")
			data = filter(lambda filtered: filtered[col] == val, data)
		if select!='':
			cols = select.split(",")

			cols_select=[]
			cols_aggregate={}

			for i in cols:
				cols_select.append(i.split(':')[0])
				if ':' in i:
					key, agg = i.split(':')
					cols_aggregate[key] = agg
			
			for row in data:
				result.append({k: row[k] for k in cols_select})
			print result
		
		grouped=[]
		if groupBy!='':
			result.sort(key=itemgetter(groupBy))
			for k,v in groupby(result,key=lambda x:x[groupBy]):
				grouped.append(list(v))
			for group in grouped:
				#sum
				#print sum(int(item['SHOT']) for item in group)
				#min
				#print min(int(item['SHOT']) for item in group)
				#max
				#print max(int(item['SHOT']) for item in group)
				#count
				print len(set(int(item['SHOT']) for item in group))
				#collect
				print list(set(int(item['SHOT']) for item in group))


if __name__ == "__main__":
   main(sys.argv[1:])


