from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def flaskapp():
    return render_template('index.html')

@app.route('/test')
def testthis():
    return 'This!'

if __name__ == '__main__':
    app.run()
