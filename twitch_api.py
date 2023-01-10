import requests
import configparser

from requests.exceptions import ConnectionError

config = configparser.ConfigParser()
config.read('settings.ini')
client_id = config['Twitch']['client_id']
client_secret = config['Twitch']['client_secret']
access_token = config['Twitch']['access_token']
token_oauth = config['Twitch']['token_oauth']


def get_chatters():
    """
    Gets list of viewers from chat.
    """
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }

    params = {
        'broadcaster_id': '83984822',
        'moderator_id': '83984822',
        'first': 1000,
    }

    try:
        respond = requests.get('https://api.twitch.tv/helix/chat/chatters', headers=header, params=params)
        return [user['user_login'] for user in respond.json()['data']]
    except ConnectionError as error:
        print(error)


def get_user_id(username: str):
    """
    Gets username id

    :param username: username nickname
    :return: username_id
    """
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }

    params = {
        'login': username
    }

    try:
        respond = requests.get('https://api.twitch.tv/helix/users', headers=header, params=params)
        if respond.status_code == 200:
            return respond.json()['data'][0]['id']
    except ConnectionError as error:
        print(error)


def get_vip_list():
    """
    Gets list of vips

    :return: list of vips
    """
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }

    params = {
        'broadcaster_id': '83984822'
    }

    try:
        respond = requests.get('https://api.twitch.tv/helix/channels/vips', headers=header, params=params)
        if respond.status_code == 200:
            return [user['user_name'] for user in respond.json()['data']]
    except ConnectionError as error:
        print(error)


def grant_vip_status(username_id: str):
    """
    Grants VIP status to user

    :param username_id: username id
    :return: status
    """
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }

    params = {
        'user_id': username_id,
        'broadcaster_id': '83984822',
    }

    try:
        respond = requests.post('https://api.twitch.tv/helix/channels/vips', headers=header, params=params)
        return respond.status_code
    except ConnectionError as error:
        print(error)


def remove_vip_status(username_id: str):
    """
    Removes VIP status to user

    :param username_id: username id
    :return: status
    """
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }

    params = {
        'user_id': username_id,
        'broadcaster_id': '83984822',
    }

    try:
        respond = requests.delete('https://api.twitch.tv/helix/channels/vips', headers=header, params=params)
        return respond.status_code
    except ConnectionError as error:
        print(error)


def timeout_user(username_id: str, reason: str = "Just because"):
    """
    Sets timeout for user

    :param username_id: username id
    :param reason: reason for the timeout
    :return: status
    """
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }

    params = {
        'broadcaster_id': '83984822',
        'moderator_id': '83984822',
    }

    data = {"data": {"user_id": username_id, "duration": 60, "reason": reason}}

    try:
        respond = requests.post('https://api.twitch.tv/helix/moderation/bans', headers=header, params=params, json=data)
        return respond.status_code
    except ConnectionError as error:
        print(error)


def get_list_of_banned_users(page=None):
    """
    Gets list of banned users

    :return: list of users
    """
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }

    params = {
        'broadcaster_id': '83984822',
        'first': 100,
        'after': page,
    }

    try:
        respond = requests.get('https://api.twitch.tv/helix/moderation/banned', headers=header, params=params)
        users = [user['user_login'] for user in respond.json()['data']]

        if respond.json()['pagination']:
            return users + get_list_of_banned_users(respond.json()['pagination']['cursor'])
        else:
            return users
    except ConnectionError as error:
        print(error)


if __name__ == '__main__':
    # print(get_chatters())
    # print(get_user_id('pianoparrot'))
    # print(grant_vip_status('50935127'))
    # print(remove_vip_status('50935127'))
    # print(get_vip_list())
    print(get_list_of_banned_users())
