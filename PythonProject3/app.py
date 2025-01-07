from flask import Flask, render_template, jsonify
import speedtest
import threading
from datetime import datetime

app = Flask(__name__)

def get_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000      # Convert to Mbps
    ping = st.results.ping
    return download_speed, upload_speed, ping

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-speed')
def test_speed():
    try:
        download, upload, ping = get_speed()
        return jsonify({
            'download': round(download, 2),
            'upload': round(upload, 2),
            'ping': round(ping, 2),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)