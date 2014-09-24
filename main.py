import pygal
import NewsSentiment
import threader
import webbrowser

def makeChart(term):
   chart = pygal.Box(range=(-1, 1))
   chart.title = 'News Sentiments for Term \'' + term + '\''

   cnn = NewsSentiment.Cnn()
   fox = NewsSentiment.Fox()

   threads = [threader.makeThread(generateSentiment, (chart, cnn, term)),
              threader.makeThread(generateSentiment, (chart, fox, term))]
   threader.joinThreads(threads)

   filename = term + '.png'
   chart.render_to_png(filename)
   webbrowser.open(filename)

def generateSentiment(chart, news, term):
   sentiments = [round(sentiment, 2) for sentiment in news.getSentiments(term)]
   chart.add(news.__class__.__name__ , sentiments)

term = raw_input("Enter a term: ")
makeChart(term)
