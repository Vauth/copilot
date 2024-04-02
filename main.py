"""
SAVED FOR FUTURE USE
"""
import requests
import time

# Insert access token here
ACCESS_TOKEN = 'YOUR TOKEN' # Use GetAccessToken()
MODEL = 'gpt-4' # Read README.md

#Get access token
def GetAccessToken() -> str:
    Loginheaders = {
        'accept': 'application/json',
        'editor-version': 'Neovim/0.6.1',
        'editor-plugin-version': 'copilot.vim/1.16.0',
        'content-type': 'application/json',
        'user-agent': 'GithubCopilot/1.155.0',
        'accept-encoding': 'gzip,deflate,br'
    }
    login = (requests.post('https://github.com/login/device/code', headers=Loginheaders, data='{"client_id":"Iv1.b507a08c87ecfe98","scope":"read:user"}')).json()
    print(f'>>> Visit {login["verification_uri"]} and enter code {login["user_code"]} to authenticate.')

    while True:
        time.sleep(5)
        Oauthheader = {
            'accept': 'application/json',
            'editor-version': 'Neovim/0.6.1',
            'editor-plugin-version': 'copilot.vim/1.16.0',
            'content-type': 'application/json',
            'user-agent': 'GithubCopilot/1.155.0',
            'accept-encoding': 'gzip,deflate,br'
        }
        oauth = (requests.post('https://github.com/login/oauth/access_token', headers=Oauthheader, data=f'{{"client_id":"Iv1.b507a08c87ecfe98","device_code":"{login['device_code']}","grant_type":"urn:ietf:params:oauth:grant-type:device_code"}}')).json()
        if oauth.get('access_token'): break

    return oauth['access_token']

#Get worker token
def GetToken() -> str:
    headers = {
        'authorization': f'token {ACCESS_TOKEN}',
        'editor-version': 'vscode/1.80.1',
        'editor-plugin-version': 'copilot.vim/1.16.0',
        'user-agent': 'GithubCopilot/1.155.0'
    }
    r = requests.get('https://api.github.com/copilot_internal/v2/token', headers=headers)
    return r.json()['token']


#Ask Anything
def Copilot(prompt:str) -> str:
    headers={
        'authorization': f'Bearer {GetToken()}',
        'Editor-Version': 'vscode/1.80.1'
    }
    json={
        "messages":[{"role": "system", "content": prompt}],
        "model": MODEL,
        "temperature":0.4,
        "role":"system"
    }
    try: r = requests.post('https://api.githubcopilot.com/chat/completions', headers=headers, json=json)
    except Exception as e: return e

    return r.json()["choices"][0]["message"]["content"]
