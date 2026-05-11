#!/usr/bin/env python3


if not (__name__ == "__main__"):
	print("c_main.py is not a module!")
	quit(1)


import database


def _validate_input(answer:str) -> tuple[int, str, str, int, float]:
	items = answer.split(",")
	if len(items) != 5:
		raise ValueError
	id = int(items[0])
	first_name = items[1].lower().strip()
	last_name = items[2].lower().strip()
	dependants = int(items[3])
	hours = float(items[4])
	if not str(id) in database.get_database():
		raise ValueError
	if hours < 0:
		raise ValueError
	if dependants < 0:
		raise ValueError
	return (id, first_name, last_name, dependants, hours)


print("")
database.print_database()
print("")


running = True
while running:
	print("Enter information in the following format, or \"end\" to quit:")
	print("ID, First Name, Last Name, Dependants, Hours worked")
	print("Records with the same ID will be overwritten")
	data:tuple[int, str, str, int, float] = (0, "", "", 0, 0.0)
	retry = True
	while retry:
		answer = input(f"{len(database.session_data)} records > ")
		print("")
		if answer.lower().strip() == "end":
			print("")
			retry = False
			running = False
		else:
			try:
				data = _validate_input(answer)
			except:
				print("Input had bad format or invalid data! Try again.")
			else:
				retry = False
	if running:
		to_add = True
		if data[4] > 40:
			print("Hours worked is >40! This will pay out overtime.")
			print("Do you want to (c) Continue, or (d) Discard?")
			if not (input(">").lower().strip() == "c"):
				to_add = False
		if to_add:
			try:
				database.store_session_record(data[0], data[1], data[2], data[3], data[4])
				print("")
			except ValueError:
				print("Aborted\n")


if len(database.session_data) > 0:
	answer = input("Enter name of CSV file to save >")
	while not answer.isalnum():
		print("Filename must be alphanumeric!")
		answer = input("Enter name of CSV file to save >")
	database.write_csv(answer)
else:
	print("There were no records, so the CSV file will not be written.")