from datetime import datetime, timedelta
import requests
import json


# def generate_oauth_token(self, certificate_location, print_access_token, username, password, access_token_url):
def generate_oauth_token(certificate_location, access_token_url, username, password, print_access_token):
    
    print("Generating access token")

    # Requesting the OAuth 2.0 token
    response = requests.post(url = access_token_url,
                                data={'client_id':username, 'client_secret':password, 'grant_type':'client_credentials'},
                                verify=certificate_location).text
    
    # Parse a valid json response and convert it into a dictionary 
    response_dict = json.loads(response)

    # Access the token from dictionary created comprising the returned json response
    access_token = response_dict['access_token']

    if print_access_token == True:
        print("Access token -> ", access_token)
    
    # Return the access token to the calling function.
    return access_token



def trigger_alteryx_workflow(certificate_location, access_token_url, url, username, password, print_access_token):

    print("Alteryx API endpoint URL -> ", url)

    # Obtain OAuth token
    access_token = generate_oauth_token(certificate_location, access_token_url, username, password, print_access_token)

    # HTTP headers
    headers = {'Authorization':'Bearer ' + access_token}

    # Post a request to the endpoint of the required workflow.
    print("Posting a request to the endpoint of the required workflow, after obtaing the access token from the Alteryx API")
    trigger_workflow_response = requests.post(url, headers=headers, verify=certificate_location)

    # Load the json output generated after trigerring the workflow
    trigger_workflow_response_content = json.loads(trigger_workflow_response.content.decode("utf8"))

    # Print the json output generated
    print("Trigger Response :")
    print(trigger_workflow_response_content)
    print('Status code of the trigger -> ', trigger_workflow_response.status_code)

    # Check if the workflow has been trigerred.
    if trigger_workflow_response.status_code == 200:
        print("Workflow triggered successfully!")
        return trigger_workflow_response.status_code
    else:
        print(f"Error triggering workflow: {trigger_workflow_response.status_code} - {trigger_workflow_response.text}")
        return trigger_workflow_response.status_code
