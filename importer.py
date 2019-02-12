import csv

# opening data file and putting it into a Dict
with open("data.txt","r") as file:
	data = csv.DictReader(file, delimiter="|")
	new_data=[]
	for row in data:
		#making a new list of dicts adding an "id" that will make sure rows are unique by ['PROJECT']+['SHOT']+['VERSION']
		row.update({"id":row['PROJECT']+row['SHOT']+row['VERSION']})
		new_data.append(row)
	#making a set from the "id's" on the list of dicts so it won't have repeated "id"
	new_data_unique = {v["id"]:v for v in new_data}.values()



with open("db.csv","w") as output:
	fieldnames = ['id','PROJECT','SHOT','VERSION','STATUS','FINISH_DATE','INTERNAL_BID','CREATED_DATE']
	writer = csv.DictWriter(output, fieldnames=fieldnames)
	writer.writeheader()
	for row in new_data_unique:
		writer.writerow(row)
