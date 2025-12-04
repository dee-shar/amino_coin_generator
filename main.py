from src import utils
from tabulate import tabulate

print(tabulate(
	[[1, "Generate Coins"], [2, "Transfer Coins"]], tablefmt="psql"))
choice = int(input("Choice: "))
if choice == 1:
	utils.start()
elif choice == 2:
	utils.send_coins()
