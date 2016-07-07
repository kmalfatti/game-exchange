from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/search')
def search():
  return render_template('search.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)