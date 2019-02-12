import csv

# opening data file and putting it into a Dict
with open("data.txt","r") as file:
	data = csv.DictReader(file, delimiter="|")
	new_data=[]
	for row in data:
		row.update({"id":row['PROJECT']+row['SHOT']+row['VERSION']})
		new_data.append(row)
	#map(lambda d: d['PROJECT']+d['SHOT']+d['VERSION'], data)
	new_data_unique = {v["id"]:v for v in new_data}.values()



with open("db.csv","w",) as output:
	fieldnames = ['id','PROJECT','SHOT','VERSION','STATUS','FINISH_DATE','INTERNAL_BID','CREATED_DATE']
	writer = csv.DictWriter(output, fieldnames=fieldnames)
	writer.writeheader()
	for row in new_data_unique:
		writer.writerow(row)
