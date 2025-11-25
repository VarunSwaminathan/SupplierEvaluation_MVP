import sys
from pyngrok import ngrok
import time

def start_tunnel():
    # Check if auth token is needed
    print("Initializing ngrok...")
    
    # Try to connect
    try:
        # Open a HTTP tunnel on the default port 8000
        public_url = ngrok.connect(8000).public_url
        print("\n" + "="*60)
        print(f"NGROK TUNNEL ONLINE: {public_url}")
        print("="*60)
        print("\nCopy the URL above and paste it into Lovable.")
        print("Example: POST " + public_url + "/upload/full_evaluation")
        print("\nPress Ctrl+C to stop the tunnel.")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"\n[ERROR] Could not start tunnel: {e}")
        print("\nYou may need to sign up for a free ngrok account and set your authtoken.")
        print("Run: ngrok config add-authtoken <token>")
        print("Or in python: ngrok.set_auth_token('<token>')")

if __name__ == "__main__":
    start_tunnel()
