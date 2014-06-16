#grabwitches.py
#cause it was originally made to find witchy new age tweets
import twitter
witchwordslist = open("witchwordslist.dat", "r")
witchscorelist = open("witchscorelist.dat", "r")
lamewordslist = open("lamewordslist.dat", "r")
alreadylist = open("alreadylist.dat", "r+")
configfile = open("witchy.config", "r")

witchwords = witchwordslist.read().split("\n")
witchscore = witchscorelist.read().split("\n")
lamewords = lamewordslist.read().split("\n")
already = alreadylist.read().split("\n")
configarray = configfile.read().split("\n")
config = {'key':'value'}
for c in range(len(configarray) -1):
  getcon = configarray[c].split("=")
  config[getcon[0]] = getcon[1]
#print(config['recORpop'])

filtered=[]
finest=twitter.Status()
api = twitter.Api(consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'], access_token_key=config['access_token_key'], access_token_secret=config['access_token_secret'])
print("collecting...")
for f in range(len(witchwords) - 1):
  #print("searching " + witchwords[f])
  #this search should be MORE configurable!
  somewitchshit = api.GetSearch(witchwords[f], result_type=config['recORpop'], lang=config['lang'])
  #print(witchwords[f] + " tweets: " + str(len(somewitchshit)))
  for i in range(len(somewitchshit) - 1):
    e = somewitchshit[i]
    oktweet = True
    for h in range(len(lamewords) - 1):
      if lamewords[h] in e.text:
        oktweet = False
    for j in range(len(already) - 1):
      if already[j] in str(e.id):
        oktweet = False
    if oktweet == True:
      filtered.append(e)
best = 0
print("scoring...")
for g in range(len(filtered)):
  better = 0
  for m in range(len(witchscore) - 1):
    if witchscore[m] in filtered[g].text:
      better = better + 1
  #print(filtered[g].text)
  potency = float(better)/len(filtered[g].text.split(" "))
  #print("^tweet scored: " + str(better) + ". potency: " + str(potency))
  if (better*potency) > best:
    best = better*potency
    finest = filtered[g]
if best < float(config['threshold']):
  print("Best tweet wasn't witchy enough.")
else:
  alreadylist.write(str(finest.id) + "\n")
  #print(str(len(filtered)) + " possible tweets.")
  #print("winner with a score of " + str(best) + ":\n" + finest.text)
  #dort = raw_input("Retweet it? [y]:")
  dort = "y"
  if dort == "y":
    api.PostRetweet(finest.id)
  print("Retweeted.")
