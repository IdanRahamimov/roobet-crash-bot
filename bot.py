from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys, time

URL = 'https://roobet.com/crash'

class Adict():
	def __init__(self):
		# Options is our setting for the webdriver.
		# We will use Google Chrome.
		options = webdriver.ChromeOptions()

		# Path to your chrome profile.
		# This line make it so chrome will use your profile info which mean that when you open a website
		# that you have already signed into you will not need to sign in again and the website will remeber you.
		# But its also make it so that you have to close Chrome before running the bot.
		options.add_argument(r"user-data-dir=C:\\Users\\s\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")

		# To use Chrome driver with selenium we need to download ChromeDriverManager from the internet.
		# Your Google Chrome have to be up to date.
		# To update open Google Chrome click the 3 dots at the top right, click settings and then click About Chrome
		self.driver = uc.Chrome(options=options, service=Service(ChromeDriverManager().install()))


	def open_web(self):
		try:
			self.driver.get(URL)
			time.sleep(4)
		except TimeoutException:
			self.driver.close()
			time.sleep(1)
			self.driver = webdriver.Chrome(options=options, executable_path=r"C:\\chromedriver_win32\\chromedriver.exe")
			self.driver.get(URL)
		except WebDriverException as e:
			if "version" in e:
				print(e)
				input("Press any key to close program")
			else:
				print("close your Google Chrome")
				input("Press any key to close program")

	# Return the 3 last results of Crash.
	def get_last_results(self):
		soup = BeautifulSoup(self.driver.page_source, "html.parser")
		body = soup.find("body")
		div = body.find("div")
		roo195 = div.find_all("div", class_="roo195")
		last_results = []
		if roo195:
			for i in range(3):
				text = roo195[i].find("span", class_="MuiButton-label").text
				result = float(text.replace("x", ""))
				last_results.append(result)
			
			return last_results
		else:
			return None

	# Get your account Balance
	def get_balance(self):
		soup = BeautifulSoup(self.driver.page_source, "html.parser")
		body = soup.find("body")
		div = body.find("div")
		roo237 = div.find_all("div", class_="roo237")
		return float(roo237[0].getText().replace("$", ""))

	def edit_bet(self, bet=1):
		bet_input_elements = self.driver.find_elements(By.XPATH, '//input[@type="number"]')
		
		for _ in range(len(bet_input_elements[0].get_attribute('value'))):
			bet_input_elements[0].send_keys(Keys.BACK_SPACE)
		
		bet_input_elements[0].send_keys(bet)

	def set_auto_cashout(self):
		bet_input_elements = self.driver.find_elements(By.XPATH, '//input[@type="number"]')
		
		for _ in range(len(bet_input_elements[1].get_attribute('value'))):
			bet_input_elements[1].send_keys(Keys.BACK_SPACE)
		
		bet_input_elements[1].send_keys(1.2)

	def submit_bet(self):
		bclass = "MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedSecondary MuiButton-fullWidth"
		submit_button = self.driver.find_element(By.XPATH, f'//button[@class="{bclass}"]')
		submit_button.click()
		print("submited")

def tactic_1(bob, results):
	if results[0] <= 1.2 and results[1] <= 1.2 and results[2] <= 1.2:
		#gamble
		balance = get_balance()
		# betting 10% of total balance
		bet = round(balance/10, 2)
		print("balance",balance)
		print("betting",bet)
		bob.edit_bet(bet=bet)
		bob.submit_bet()

def main():
	try:
		bob = Adict()
		bob.open_web()
		bob.edit_bet()
		bob.set_auto_cashout()
		last_results = []
		while(True):
			results = bob.get_last_results()
			if results:
				if results != last_results:
					last_results = results
					#tactic_1(bob, results)
			time.sleep(1)
	except WebDriverException as e:
		if "version" in str(e):
			print(e)
		else:
			print("close your Google Chrome")
		input("Press any key to close program")
	except Exception as e:
		if "os.PathLike" in str(e):
			print("download Google Chrome and update the options.add_argument in line 37")
		else:
			print(e)
		input("Press any key to close program")

if __name__ == '__main__':
	main()