import os
import http.client
import json
from urllib import request, parse
from dotenv import load_dotenv

def main():
    global ai_endpoint
    global ai_key
    
    try:
        # Load configuration settings from .env file
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Get user input until they enter "quit"
        userText = ''
        while userText.lower() != 'quit':
            userText = input('Enter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                GetLanguage(userText)

    except Exception as ex:
        print(ex)

def GetLanguage(text):
    try:
        # Construct the JSON request body
        jsonBody = {
            "documents": [
                {
                    "id": 1,
                    "text": text
                }
            ]
        }

        # Print the JSON body to be sent
        print(json.dumps(jsonBody, indent=2))

        # Prepare the HTTP request
        uri = ai_endpoint.rstrip('/').replace('https://', '')
        conn = http.client.HTTPSConnection(uri)

        # Add the authentication key to the request header
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ai_key
        }

        # Use the Text Analytics language API
        conn.request("POST", "/text/analytics/v3.1/languages", json.dumps(jsonBody).encode('utf-8'), headers)

        # Send the request and get the response
        response = conn.getresponse()
        data = response.read().decode("UTF-8")

        # If the call was successful, process the response
        if response.status == 200:
            results = json.loads(data)
            print(json.dumps(results, indent=2))

            # Extract and display the detected language name for each document
            for document in results["documents"]:
                print("\nLanguage:", document["detectedLanguage"]["name"])
        else:
            # Something went wrong, print the whole response
            print(data)

        conn.close()

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
