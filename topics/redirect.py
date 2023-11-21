from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/redirect')
def redirect_example():
    # Redirecting to the home page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port=2001)
