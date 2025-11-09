from src import utils
from tabulate import tabulate

print(tabulate(
	[[1, "Generate Coins"], [2, "Transfer Coins"]], tablefmt="psql"))
choice = int(input("Choice: "))
if Choice == 1:
	utils.start()
elif Choice == 2:
	utils.transfer_coins()
