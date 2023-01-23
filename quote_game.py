import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice


BASE_URL = "http://quotes.toscrape.com"

def scrape_quotes():
	all_quotes = []
	url = "/page/1"
	print("Grabbing quotes.. please wait warmly until it is ready.")
	while url:
		res = requests.get(f"{BASE_URL}{url}")
		soup = BeautifulSoup(res.text, "html.parser")
		quotes = soup.find_all(class_="quote")
		for quote in quotes:
			all_quotes.append({
				"text":quote.find(class_="text").get_text(),
				"author":quote.find(class_="author").get_text(),
				"bio_ref":quote.find("a")["href"]
				})

		next_btn = soup.find(class_='next')
		url = next_btn.find("a")["href"] if next_btn else None
		sleep(2)
		return all_quotes

def run_game(quotes):
	quote = choice(quotes)
	remaining_guesses = 4
	print("Here is a quote: ")
	print(quote["text"])
	guess = ''
	while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
		print(quote['author'])
		guess = input(f"Who said this quote? You have {remaining_guesses} guess(es) left.\n")
		if guess.lower() == quote["author"].lower():
			print("That is correct.")
			break
		remaining_guesses -= 1
		if  remaining_guesses == 3:
			res = requests.get(f"{BASE_URL}{quote['bio_ref']}")
			soup = BeautifulSoup(res.text, "html.parser")
			birthdate = soup.find(class_="author-born-date").get_text()
			birthplace = soup.find(class_=	'author-born-location').get_text()
			print(f"Here is a hint: This author was born {birthplace} on {birthdate}.")
		elif remaining_guesses == 2:
			print(f"Here's another hint: The author\'s first name starts with {quote['author'][0]}.")
		elif remaining_guesses == 1:
			last_initial = quote['author'].split(" ")[1][0]
			print(f"Here's another hint: The author\'s last name starts with {last_initial}.")
		else:
			print(f"No remaining guesses! The correct answer was {quote['author']}.")

	user_in = ''
	while user_in.lower() not in ('y', 'yes', 'n' ,'no'):
		user_in = input("Would you like to play again? (y/n)? ")
	if user_in.lower() in ('yes', 'y'):
		return run_game(quotes)
	else:
		print("Thank you for playing.")

quotes = scrape_quotes()
run_game(quotes)