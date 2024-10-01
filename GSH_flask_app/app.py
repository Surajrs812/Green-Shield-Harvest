from flask import Flask, render_template, jsonify
from get_values import get_device_status

app = Flask(__name__)

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for Raspberry Pi view
@app.route('/pi-view')
def pi_view():
    return render_template('pi_view.html')

# API to fetch sensor and weather data
@app.route('/api/get-status', methods=['GET'])
def get_status():
    # Fetch the device status from the external file
    data = get_device_status()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
