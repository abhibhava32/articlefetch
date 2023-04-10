from flask import Flask, render_template, request
from newspaper import Article
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Extract the URL entered by the user from the request
        url = request.form['url']
        
        # Validate the URL
        if not url.startswith('http'):
            error = 'Enter a valid URL'
            return render_template('index.html', error=error)

        # Fetch the article information using newspaper3k
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        
        # Extract the article information
        image_url = article.top_image
        article_title = article.title
        # published_time = article.publish_date
        summary = article.summary
        source = article.source_url
        keywords = article.keywords

        # Render a new HTML template with the fetched article information
        return render_template('result.html', image_url=image_url, article_title=article_title, summary=summary, source=source, keywords=keywords)
    
    # Render the homepage HTML template
    return render_template('index.html')

if __name__ == '__main__':
    # app.run(debug=True)
    http_server = WSGIServer(('https://abhibhava32-articlefetch-app-i6qquu.streamlit.app/', 8080), app)
    http_server.serve_forever()