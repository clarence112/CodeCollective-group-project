from collections.abc import Callable
import json
import os
import calc


# consts
# Stores the path to the employee pay database.
EMP_DB:str = "./records/employee_pay_rates.json"
# Stores the header of the CSV file
CSV_HEAD:str = "ID,First Name,Last Name,Dependants,Hours,Gross pay,State tax,Fed tax,Net pay"


# vars
# Stores the spreadsheet data for this session
# ID: First, Last, Dependants, Hours, Gross pay, State tax, Fed tax, Net pay
session_data:dict[int, tuple[str, str, int, float, float, float, float, float]] = {}


# Verifies user input when filling out employee pay rates.
def _validate_db_input(to_validate:str) -> None:
	fields:list[str] = to_validate.split(",")
	assert len(fields) == 4, "Incorrect number of values!"
	try:
		int(fields[0].strip())
	except:
		assert False, "ID value was not int!"
	try:
		float(fields[3].strip())
	except:
		assert False, "Pay value was not float!"



# Fills out the database linking employee ID to payment.
# Should only be run when the database does not currently exist, or needs to be updated.
def regenerate_employee_database() -> None:
	print("Input employee info in the following order: \"ID[int], FIRST NAME[string], LAST NAME[string], PAY[float]\".")
	print("Enter \"end\" when done.")
	data:dict[int, tuple[str, str, float]] = {}
	while True:
		answer:str = input(f"{len(data.keys())} records >")
		if answer == "end":
			break

		try:
			_validate_db_input(answer)
		except AssertionError as e:
			print(e)
		else:
			fields:list[str] = answer.split(",")
			id:int = int(fields[0].strip())
			if id in data:
				print("Duplicate employee ID!")
			else:
				data[id] = (fields[1].strip().lower(), fields[2].strip().lower(), float(fields[3].strip()))
	
	database:str = json.dumps(data)
	print(os.path.dirname(EMP_DB))
	os.makedirs(os.path.dirname(EMP_DB), exist_ok=True)
	f = open(EMP_DB, "w")
	f.write(database)
	f.close()
	print(f"Wrote {len(data.keys())} records.")



# Find the employee's pay from their ID.
# The db_path and test_mode parameters should only be used for unit tests
def find_pay(id:int, name_first:str, name_last:str, db_path:str = EMP_DB, test_mode:bool = False) -> float:
	name_first = name_first.strip().lower()
	name_last = name_last.strip().lower()
	r_id:str = str(id) # For some reason, JSON does not support int dict keys
	f = open(db_path, "r")
	database = json.loads(f.read())
	f.close()
	if not isinstance(database, dict):
		raise TypeError("Employee database is not a dict!")
	if not (r_id in database.keys()):
		raise ValueError("Invalid employee ID!")
	record:tuple[str, str, float] = (str(database[r_id][0]), str(database[r_id][1]), float(database[r_id][2]))
	if (name_first == record[0]) and (name_last == record[1]):
		return record[2]
	elif test_mode:
		raise ValueError("Employee name does not match!")
	elif input("Employee name does not match ID on record. Use anyway? (y/n) >").strip().lower() == "y":
		return record[2]
	else:
		raise ValueError("Employee name does not match!")


# Output the spreadsheet to disk (CSV format)
# "test_mode" argument should only be used in unit tests, as it blocks writing.
def write_csv(filename:str, test_mode:bool = False) -> str:
	csv_dat:str = CSV_HEAD
	sd = session_data
	for i in sd:
		csv_dat += f"\r\n{i},{sd[i][0]},{sd[i][1]},{sd[i][2]},{sd[i][3]},{sd[i][4]},{sd[i][5]},{sd[i][6]},{sd[i][7]}"
	if not test_mode:
		print(csv_dat)
		f = open(f"{filename}.csv")
		f.write(csv_dat)
		f.close()
	return csv_dat


# Stores a line of pay info, to be written to disk later.
# Assumes hours have already been validated
# "db" and "test_mode" arguments should only be used in unit tests.
def store_session_record(id:int, name_first:str, name_last:str, deps:int, hours:float, db:str = EMP_DB, test_mode:bool = False) -> None:
	rate:float = find_pay(id, name_first, name_last, db, test_mode)
	gross:float = calc.calc_gross(hours, rate)
	state:float = calc.calc_state(gross)
	fed:float = calc.calc_fed(gross)
	net:float = calc.calc_net(gross)
	session_data[id] = (name_first, name_last, deps, hours, gross, state, fed, net)


# Unit tests on the _validate_db_input function
def _test_0() -> tuple[str, bool]:
	try:
		_validate_db_input("0, test, test, 25")
	except:
		return ("DB test valid data", False)
	else:
		return ("DB test valid data", True)
def _test_1() -> tuple[str, bool]:
	try:
		_validate_db_input("0, test, test, 25, a")
	except:
		return ("DB test invalid data 1", True)
	else:
		return ("DB test invalid data 1", False)
def _test_2() -> tuple[str, bool]:
	try:
		_validate_db_input("0, test, test, test")
	except:
		return ("DB test invalid data 2", True)
	else:
		return ("DB test invalid data 2", False)
# Unit tests on reading the database
TEST_DB:str = "./testdata/testdb.json"
def _test_3() -> tuple[str, bool]:
	try:
		find_pay(0, "test", "person", TEST_DB, True)
	except:
		return ("Read valid data (not found)", False)
	else:
		return ("Read valid data", find_pay(0, "test", "person", TEST_DB, True) == 1)
def _test_4() -> tuple[str, bool]:
	try:
		find_pay(1, "test", "person", TEST_DB, True)
	except:
		return ("Read invalid data", True)
	else:
		return ("Read invalid data", False)
def _test_5() -> tuple[str, bool]:
	try:
		find_pay(0, "person", "test", TEST_DB, True)
	except:
		return ("Read mismatched data", True)
	else:
		return ("Read mismatched data", False)
# Unit tests on writing CSV
def _test_6() -> tuple[str, bool]:
	store_session_record(0, "test", "person", 0, 10, TEST_DB, True)
	return ("Session data", session_data == {0: ("test", "person", 0, 10, 10.0, 0.56, 0.79, 8.65)})
def _test_7() -> tuple[str, bool]:
	output:str = write_csv("test", True)
	return ("Validate CSV content", output == "ID,First Name,Last Name,Dependants,Hours,Gross pay,State tax,Fed tax,Net pay\r\n0,test,person,0,10,10.0,0.56,0.79,8.65")


# Stores a list of functions to use as unit tests.
UNIT_TESTS:list[Callable[[], tuple[str, bool]]] = [
	_test_0,
	_test_1,
	_test_2,
	_test_3,
	_test_4,
	_test_5,
	_test_6,
	_test_7,
]


# Handle running the script directly.
if __name__ == "__main__":
	import sys
	if "--run-unit-tests" in sys.argv:
		stat:int = 0
		count:int = 0
		for i in UNIT_TESTS:
			result = i()
			if result[1]:
				print(f"Test {count}: {result[0]}: SUCCESS")
			else:
				print(f"Test {count}: {result[0]}: FAILED")
				stat += 1
			count += 1
		print(f"{stat} tests failed.")
		quit(stat)
	elif "--regen" in sys.argv:
		regenerate_employee_database()
		quit(0)
	else:
		print("This module is a library and is not meant to be run on its own.")
		print("Import this module to make use of it.")
		print("Or, you can run the script with \"--run-unit-tests\" to validate it.")
		quit(1)