import threading
import time
import requests
import webview
from backend.main import create_app

def wait_for_server(url, timeout=5.0):
    """Wait for the Flask server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.1)
    return False

def start_server(port=5000):
    """Start the Flask server in a daemon thread."""
    app = create_app()
    # disable werkzeug logging for cleaner output
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Run the server without the reloader since we are in a thread
    app.run(host='127.0.0.1', port=port, threaded=True, use_reloader=False)

def main():
    port = 5000
    url = f"http://127.0.0.1:{port}"
    health_url = f"{url}/api/health"
    
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    
    if wait_for_server(health_url):
        window = webview.create_window(
            'Space Station Academy',
            url,
            width=1200,
            height=800,
            min_size=(800, 600)
        )
        # In production, debug should be False to disable DevTools
        webview.start(debug=False)
    else:
        print("Failed to start backend server.")

if __name__ == '__main__':
    main()
