from scrapers import scraper, utilities

games = scraper.get_games("BC6H1WZE")
print(utilities.format_data(games))