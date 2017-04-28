import tweepy
import sys
from time import sleep
from time import time
from random import randint
from credentials import *
from hashtags import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)
fav = 0
latestActions = [time() - 600]

def apiDelimiter(time):
	global latestActions
	if time - 500 < latestActions[0]:
		latestActions.append(time)

		if len(latestActions) > 10:
			latestActions.pop(0)
			
		errorHandler('10')
	else:
		latestActions.append(time)
		if len(latestActions) > 10:
			latestActions.pop(0)		

def cleanup(keyword, mod):
	keyword = keyword
	mod = mod

	if mod == 'addRemove':
		if keyword in usedHashtags:
			print("Duplicate keyword error")
			hashtags.remove(keyword)
			print("Deleting duplicate keyword")
			timer(15)
		else:
			usedHashtags.append(keyword)
			hashtags.remove(keyword)

	elif mod == 'clean':
		del hashgtags[:]

		for i in usedHashtags:
			hashgtags.append(i)
		
		del usedHashtags[:]
		print("Application Reset in progress")
		timer(120)
			
def hashtag():
	if len(hashtags) == 1:
		return (hashtags[0])

	randNum = (randint(0,len(hashtags)))

	if randNum >= len(hashtags):
		return (hashtags[len(hashtags) - 1])

	else:
		return (hashtags[randNum])

def heartTweet():
	global fav
	startTime = time()
	passedTweets = 0
	word = hashtag()
	tweets = tweepy.Cursor(api.search, q = word).items(3000)
	try:
		for status in tweets:
			try:	
				if status.favorite_count > 1:
					apiDelimiter(time())
					status.favorite()
					fav += 1
					print("FAVORITED KEYWORD: " + word)
					if status.retweet_count >= 3:
						timer(randint(15, 30))
						apiDelimiter(time())
						status.retweet()
						print("RETWEETED TWEET")
						print("Fav Tweet Count: " +str(fav))
					else:
						print("Status not pupolar enough to retweet.")
						print("Fav Tweet Count: " +str(fav))

					timer(randint(80, 200))
				else:
					passedTweets +=1
					print("Attemp on " + word + " num: " +  str(passedTweets))
					sleep(0.2)
					sys.stdout.write("\033[K") #clear line
					sys.stdout.write("\033[F") #back to previous line

			except tweepy.TweepError as err:
				if '429' in str(err):
					errorHandler('429')

				elif '139' in str(err):
					errorHandler('139')

				elif 'Failed to send request' in str(err):
					errorHandler('404')

				else:
					errorHandler('wait')
				
	except tweepy.TweepError as err:
		if '403' in str(err):
			errorHandler('403')

		elif '429' in str(err):
			errorHandler('429')

		elif 'Failed to send request' in str(err):
			errorHandler('404') 
	
		else:
			print('Error thrown: ' + str(err))
			errorHandler('10')

	cleanup(word, 'addRemove')
	
	if startTime > time() - 260:
		errorHandler('10')

def errorHandler(code):
	global latestActions

	if code == '403':
		print("Login info incorrect")
		quit()
	
	elif code == '429':
		print("Rate Limit Exceeded: Hold for 1 hour")
		print(latestActions)
		timer(4000)

	elif code == '139':
		print("Tweet already Favorited")
		timer(randint(80, 200))

	elif code == '5':
		print("Delimination Timer Sequence Commenced: Hold for 5  minutes")
		timer(60 * 5)

	elif code == '10':
		print("Delimination Timer Sequence Commenced: Hold for 10 minutes")
		print(latestActions)		
		timer(60 * 10)

	elif code == '404':
		timer(60)

	else:
		print("Rate Limit Exceeded: Hold for 15 minutes")
		timer(1000)
	
	del latestActions [:]
	latestActions = [time() - 500]	

def timer(time):
	for i in range(time, 0, -1):
				print(str(i))
				sys.stdout.write("\033[F") #back to previous line
				sleep(1)
				sys.stdout.write("\033[K") #clear line

def main():
	while fav < 1001:
		if fav == 1000:
			cleanup('cleaning', 'clean')

		print(" - - ")	
		heartTweet()
		print(" - - ")
	else:
		print("Ended Run")
		print("Tweet count: " + str(fav))


if __name__ == "__main__":
	main()
