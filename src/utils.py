import logging
from time import time
from json import load
from time import sleep
from src.library import amino
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

accounts = []
with open("accounts.json") as database:
	data = load(database)
	for account in data:
		accounts.append(account)

def login(
		client: amino.Amino,
		email: str,
		password: str) -> None:
	try:
		logger.info(f"Device ID: {client.device_id}")
		client.login(
			email=email, password=password, socket=False)
		logger.info(f"Logging in: {email}")
	except Exception as exception:
		logger.error(f"Login failed for {email}: {exception}")
        
        
def get_timers() -> dict:
	return {
		"start": int(time()),
		"end": int(time()) + 300
	}

def generate_coins(
		client: amino.Amino, ndc_id: int, email: str) -> None:
	timers = [get_timers() for _ in range(50)]
	client.send_active_object(ndc_id=ndc_id, timers=timers)
	logger.info(f"Generating coins for {email}")
	
def play_lottery(client: amino.Amino, ndc_id: int) -> None:
	try:
		response = client.lottery(ndc_id=ndc_id)["api:message"]
		logger.info(f"Lottery result: {response}")
	except Exception as exception:
		logger.error(f"Lottery error: {exception}")
		
def watch_ad(client: amino.Amino) -> None:
	try:
		response = client.watch_ad()["api:message"]
		logger.info(f"Ad watched: {response}")
	except Exception as exception:
		logger.error(f"Ad watch error: {exception}")
		
def transfer_coins(client: amino.Amino) -> None:
	link_info = client.get_from_code(
		input("Blog link: "))["linkInfoV2"]["extensions"]["linkInfo"]
	ndc_id, blog_id = link_info["ndcId"], link_info["objectId"]
	delay = int(input("Transfer delay in seconds: "))
	for account in accounts:
		client = amino.Amino()
		email = account["email"]
		password = account["password"]
		try:
			login(
				client=client, email=email, password=password)
			client.join_community(ndc_id=ndc_id)
			total_coins = client.get_wallet_info()["wallet"]["totalCoins"]
			logger.info(f"{email} has {total_coins} coins")
			amount = min(total_coins, 500)
			if amount > 0:
				response = client.send_coins_blog(
					ndc_id=ndc_id, blog_Id=blog_id, coins=amount)["api:message"]
				logger.info(f"Transferred {amount} coins | Response: {response}")
			sleep(delay)
		except Exception as exception:
			logger.error(f"Failed to transfer coins: {exception}")


def start_generator(init_client: amino.Amino) -> None:
	ndc_id = init_client.get_from_code(
		input("Community link: "))["linkInfoV2"]["extensions"]["community"]["ndcId"]
	delay = int(input("Generation delay in seconds: "))
	for account in accounts:
		account_client = amino.Amino()
		email = account["email"]
		password = account["password"]
		try:
			login(
				client=account_client, email=email, password=password)
			watch_ad(client=account_client)
			play_lottery(client=account_client, ndc_id=ndc_id)
			with ThreadPoolExecutor(max_workers=10) as executor:
				for _ in range(25):
					executor.submit(generate_coins, account_client, ndc_id, email)
			sleep(delay)
		except Exception as exception:
			logger.error(f"Error in main process {exception}")
