from flask import Flask, render_template, request, session, json
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def flaskapp():
    if request.method == 'POST':
        pass

    return render_template('index.html')

@app.route('/estimate', methods = ['POST'])
def estimate():

    # Figure out how to make the AJAX call to the CL listing on the client side
    # listing = request.attrs['listing']
    link = request.form['link']

    # Parse the listing to get all the attributes
    #   Set actual = 'price'

    # Feed all the attributes into the model to make one estimate
    #   Set estimate = 'estimate'

    # Temporary
    print(link)
    print(type(link))
    estimate = float(link.split(' ')[1])
    actual = '$ %6.2f' % (estimate * 1.2)
    estimate = '$ %6.2f' % estimate

    # Return the estimate and actual price, which get set on the client side
    return json.dumps({'status': 'OK', 'estimate': estimate, 'actual': actual})

if __name__ == '__main__':
    # Load the model
    app.run()
