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
		print 'query.py -s <columns> -o <columns> -f <column>=<value> -g <column>'
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
			if 'AND' in filtr:
				data = and_clause(data,filtr)

			elif 'OR' in filtr:
				data = or_clause(data,filtr)
			else:
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
		
		grouped=[]
		if groupBy!='':
			result.sort(key=itemgetter(groupBy))
			for k,v in groupby(result,key=lambda x:x[groupBy]):
				grouped.append(list(v))

			#cleaning result so we can get a new result with aggregate and group by
			result=[]
			for group in grouped:
				for col, aggregate in cols_aggregate.items():
					#using float so it works with all columns that have numbers
					if aggregate == 'sum':
						group[0][col] = sum(float(item[col]) for item in group)
					if aggregate == 'min':
						group[0][col] = min(float(item[col]) for item in group)
					if aggregate == 'max':
						group[0][col] =  max(float(item[col]) for item in group)
					#using set on the next two methods as it needs to be distinct values
					if aggregate == 'count':
						group[0]['count'] =  len(set(item[col] for item in group))
					if aggregate == 'collect':
						group[0]['collect'] =  list(set(item[col] for item in group))
				result.append(group[0])

		print result


#function to be used on filter function and apply OR to all elements in list
def apply_or(filtered, cols, vals):
	if len(cols) > 1:
		return filtered[cols[0]] == vals[0] or apply_or(filtered,cols[1:],vals[1:])
	else:
		return filtered[cols[0]] == vals[0]

#function to be used on filter function and apply AND to all elements in list
def apply_and(filtered, cols, vals):
	if len(cols) > 1:
		return filtered[cols[0]] == vals[0] and apply_and(filtered,cols[1:],vals[1:])
	else:
		return filtered[cols[0]] == vals[0]

#function used to execute OR query statements
def or_clause(data,clause):
	or_cols = clause.split(" OR ")
	cols = []
	vals = []
	for i in or_cols:
		col, val = i.split("=")
		cols.append(col)
		vals.append(val)
	data = (filter(lambda filtered: apply_or(filtered,cols,vals), data))
	return data

#function used to execute AND query statements, also handling OR query statements
def and_clause(data,clause):
	and_cols = clause.split(" AND ")
	cols = []
	vals = []
	for i in and_cols:
		if 'OR' in i:
			data = or_clause(data,i)
		else:
			col,val = i.split("=")
			cols.append(col)
			vals.append(val)

	data = filter(lambda filtered: apply_and(filtered,cols,vals), data)
	return data

if __name__ == "__main__":
   main(sys.argv[1:])


