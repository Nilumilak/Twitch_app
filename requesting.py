import requests
from pprint import pprint
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
client_id = config['Twitch']['client_id']
client_secret = config['Twitch']['client_secret']
access_token = config['Twitch']['access_token']
token_oauth = config['Twitch']['token_oauth']

# header = {
#     'Authorization': f'Bearer {access_token}',
#     'Client-Id': client_id,
# }
# param = {
#     'login': 'fighting_sheep',
# }
# respond = requests.get('https://tmi.twitch.tv/group/user/pianoparrot/chatters', headers=header)
# print(respond.status_code)
# pprint(respond.json()['chatters']['viewers'] + respond.json()['chatters']['broadcaster'] + respond.json()['chatters']['moderators'])
# pprint(respond.json())

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

# header = {
#     'Authorization': f'Bearer {access_token}',
#     'Client-Id': client_id,
# }
#
# params = {
#     'login': 'pianoparrot',
# }
#
# response = requests.get('https://api.twitch.tv/helix/users', params=params, headers=header)
# print(response.status_code)
# pprint(response.json())
#
#
# header = {
#     'Authorization': f'Bearer {access_token}',
#     'Client-Id': client_id,
# }
#
# params = {
#     'broadcaster_id': '83984822',
# }
# respond = requests.get('https://api.twitch.tv/helix/channels/vips', headers=header, params=params)
# print(respond.status_code)
# pprint(respond.json())

# header = {
#     'Authorization': f'Bearer {access_token}',
#     'Client-Id': client_id,
# }
#
# params = {
#     'user_id': '50935127',
#     'broadcaster_id': '83984822',
# }
# respond = requests.post('https://api.twitch.tv/helix/channels/vips', headers=header, params=params)
# print(respond.status_code)
# pprint(respond.json())


########## ACCESS TOKEN #######################
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
# }
#
# params = {
#
# }
#
# respond = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')
# pprint(respond.status_code)
# pprint(respond.json())


# moz1z640vd60100jqc8l2zftjprrs7
# c3ab8aa609ea11e793ae92361f002671

# params = {
#     'client_id': client_id,
#     'client_secret': client_secret,
#     'code': 'zhr024c6o8hp9le3dc9rn8hfkzprpf',
#     'grant_type': 'authorization_code',
#     'redirect_uri': 'http://localhost:3000',
# }
#
# respond = requests.post('https://id.twitch.tv/oauth2/token', params=params)
# print(respond.status_code)
# pprint(respond.json())

params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials',
}

respond = requests.post('https://id.twitch.tv/oauth2/token', params=params)
print(respond.status_code)
pprint(respond.json())
