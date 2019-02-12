import csv

# opening data file and putting it into a Dict
with open("data.txt","r") as data:
	reader = csv.DictReader(data, delimiter="|")
	for row in reader:
		print row

