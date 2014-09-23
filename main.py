from __future__ import division
import NewsSentiment
import threader

def printSentiment(news, term):
   print news.__class__.__name__ + ": " + str(average(news.getSentiments(term)))

def average(nums):
   return sum(nums)/len(nums)

term = raw_input("Enter a term: ")

cnn = NewsSentiment.Cnn()
fox = NewsSentiment.Fox()

threads = [threader.makeThread(printSentiment, (cnn, term)),
          threader.makeThread(printSentiment, (fox, term))]

threader.joinThreads(threads)
