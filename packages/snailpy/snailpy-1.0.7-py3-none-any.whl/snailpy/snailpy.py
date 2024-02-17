import requests

api_url = 'https://projects.snail-ide.com'

def customAPI(url):
    global api_url
    api_url = url
    print(f'You are now using: {api_url}')

def get_follower_count(username):
    url = f'{api_url}/api/users/getFollowerCount?username={username}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            follower_count = int(response.text)
            return follower_count
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def id_to_name(args):
    url = f'{api_url}/api/pmWrapper/getProject?id={args["WHO"]}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            return json_data.get('name', '')
        else:
            return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def id_to_owner(args):
    url = f'{api_url}/api/pmWrapper/getProject?id={args["WHO"]}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            return json_data.get('author', {}).get('username', '')
        else:
            return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
