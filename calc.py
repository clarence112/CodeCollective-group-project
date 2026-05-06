from collections.abc import Callable

# Consts
# Stores the state an federal tax rates
STATE:float = 0.056
FED:float = 0.079


# Clamps value within the range a-b
def clampf(value:float, a:float, b:float) -> float:
	maxv:float = max(a, b)
	minv:float = min(a, b)
	return min(maxv, max(minv, value))


# Returns the federal taxes to deduct
def calc_fed(gross:float) -> float:
	return round(gross * FED, 2)


# Returns the state taxes to deduct
def calc_state(gross:float) -> float:
	return round(gross * STATE, 2)


# Returns the gross pay based of the hours worked and hourly rate
def calc_gross(hours:float, rate:float) -> float:
	gross:float = 0.0
	gross += clampf(hours, 0, 40) * rate
	gross += max(hours - 40, 0) * (rate * 1.5)
	return round(gross, 2)


# Returns the net pay after deducting taxes
def calc_net(gross:float) -> float:
	net:float = gross
	net -= calc_fed(gross)
	net -= calc_state(gross)
	return round(net, 2)


# Unit tests
def _test_0() -> tuple[str, bool]:
	stat:bool = (clampf(5, 0, 10) == 5)
	stat = stat and (clampf(20, 0, 10) == 10)
	stat = stat and (clampf(-3, 0, 10) == 0)
	return ("Test clampf", stat)
def _test_1() -> tuple[str, bool]:
	return ("Test federal tax", calc_fed(50) == 3.95)
def _test_2() -> tuple[str, bool]:
	return ("Test state tax", calc_state(50) == 2.8)
def _test_3() -> tuple[str, bool]:
	return ("Test gross", calc_gross(60, 1) == 70)
def _test_4() -> tuple[str, bool]:
	return ("Test net", calc_net(50) == 43.25)


# Stores a list of functions to use as unit tests.
UNIT_TESTS:list[Callable[[], tuple[str, bool]]] = [
	_test_0,
	_test_1,
	_test_2,
	_test_3,
	_test_4,
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
	else:
		print("This module is a library and is not meant to be run on its own.")
		print("Import this module to make use of it.")
		print("Or, you can run the script with \"--run-unit-tests\" to validate it.")
		quit(1)