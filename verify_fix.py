
import requests
import re

def verify_chatbot():
    session = requests.Session()
    url = "http://127.0.0.1:5000/"
    
    try:
        # Initial access
        print("Accessing homepage...")
        resp = session.get(url)
        resp.raise_for_status()
        
        # Send query
        print("Sending query: 'what causes cancer?'...")
        data = {"prompt": "what causes cancer?"}
        resp = session.post(url, data=data, allow_redirects=True)
        resp.raise_for_status()
        
        html_content = resp.text
        
        # Check for error
        if "410 Client Error" in html_content:
            print("FAILED: 410 Client Error still present.")
            return
        
        if "Error :" in html_content:
            print("FAILED: Generic error found in response.")
            match = re.search(r"Error : (.*?)<", html_content)
            if match:
                print(f"Error details: {match.group(1)}")
            else:
                print(html_content[:500]) # Print start of HTML
            return

        # Check for success indicators (medical content)
        # We expect terms like "DNA", "genetic", "smoking", "environmental", etc.
        # Or just checking if there is a response from "assistant"
        
        print("Response received. Checking content...")
        # Simple check: assuming the response is NOT the error
        if "cancer" in html_content.lower(): 
            print("SUCCESS: 'cancer' found in response.")
        else:
             print("WARNING: 'cancer' not found in response, but no error detected either.")
             
        # Extract response text roughly
        # Looking for the last message
        print("Preview of page text:")
        print(html_content[-2000:]) # Print end of page where chat usually is

    except Exception as e:
        print(f"ERROR: Verification script failed: {e}")

if __name__ == "__main__":
    verify_chatbot()
