import requests
from pprint import pprint

with open('tokens/Client ID.txt') as token:
    client_id = token.readline().strip()

with open('tokens/ClientSecret.txt') as token:
    client_secret = token.readline().strip()

with open('tokens/AccessToken.txt') as token:
    access_token = token.readline().strip()

with open('tokens/Oauth token.txt') as token:
    token_oauth = token.readline().strip()

header = {
    'Authorization': f'Bearer {access_token}',
    'Client-Id': client_id,
}
param = {
    'login': 'pianoparrot',
}
respond = requests.get('https://tmi.twitch.tv/group/user/pianoparrot/chatters', headers=header)
print(respond.status_code)
pprint(respond.json()['chatters']['viewers'] + respond.json()['chatters']['broadcaster'] + respond.json()['chatters']['moderators'])
pprint(respond.json())

# header = {
#     'Authorization': f'Bearer {access_token}',
#     'Client-Id': client_id,
# }
# param = {
#     'broadcaster_id': '83984822'
# }
# respond = requests.get('https://api.twitch.tv/helix/channels', headers=header, params=param)
# print(respond.status_code)
# pprint(respond.json())
#