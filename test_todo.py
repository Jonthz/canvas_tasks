import msal
import requests
import webbrowser

def open_id(file):
    with open(file, 'r') as file:
        ids = []
        for line in file.readlines():
            ids.append(line.strip().split('=')[1])
    return ids

def create_confidential_client(client_id, client_secret, authority):
    return msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )

def get_access_token(app, scopes):
    auth_url = app.get_authorization_request_url(scopes)
    webbrowser.open(auth_url, new=True)
    
    authorization_code = input("Enter the authorization code: ")
    token_response = app.acquire_token_by_authorization_code(
        code=authorization_code,
        scopes=scopes
    )
    
    return token_response.get("access_token")

def get_todo_list(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers)
    return response.json().get("value", [])

def main():
    client_id, client_secret, tenant_id = open_id('azure_sec.txt')
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    redirect_uri = 'http://localhost'
    scopes = ["Tasks.ReadWrite"]

    app = create_confidential_client(client_id, client_secret, authority)
    access_token = get_access_token(app, scopes)

    if not access_token:
        print("No access token found.")
        return

    #todo_list = get_todo_list(access_token)
    #for todo_item in todo_list:
        #print(todo_item['displayName'])

if __name__ == "__main__":
    main()
