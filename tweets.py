def get_coordinates(location):
	from geopy.geocoders import Nominatim
	geolocator = Nominatim(user_agent='Twitter')
	try:
		coordinates = [geolocator.geocode(location).latitude, geolocator.geocode(location).longitude]
	except AttributeError:
		coordinates = None
	return coordinates


def geo_query(api, search_text, search_coordinates, search_radius='30mi'):
	import tweepy as tw
	from datetime import datetime
	from db import insert_data_into_db
	if search_coordinates:
		full_search = f'{search_text} geocode:{search_coordinates[0]},{search_coordinates[1]},{search_radius}'
	else:
		full_search = f'{search_text}'
	full_tweets = [tweet for tweet in
				   tw.Cursor(api.search, q=full_search, tweet_mode='extended', lang='en', count=5).items() if
				   (tweet.retweeted == False) & (tweet.full_text[:2] != 'RT')]
	tweets = [
		{'id': tweet.id, 'query': search_text, 'date': tweet.created_at.strftime("%Y-%m-%d"), 'text': tweet.full_text,
		 'username': tweet.user.name, 'screenName': tweet.user.screen_name, 'location': tweet.user.location,
		 'numberRetweets': tweet.retweet_count} for tweet in full_tweets]
	# tweets = [{'id': tweet.id,
	# 		   'query': search_text,
	# 		   'date': tweet.created_at,
	# 		   'text': tweet.full_text,
	# 		   'username': tweet.user.name,
	# 		   'screenName': tweet.user.screen_name,
	# 		   'location': tweet.user.location,
	# 		   'numberRetweets': tweet.retweet_count}
	# 		  for tweet in tw.Cursor(api.search, q=full_search, tweet_mode='extended', lang='en', count=2).items()
	# 		  if (tweet.retweeted == False) & (tweet.full_text[:2] != 'RT')]
	return tweets


def clean_text(text):
	text = text.lower()
	text = text.replace(r'https\S+', '')
	text = text.replace(r'', '')
	text = text.replace(r'rt', '')
	text = text.strip()
	return text
