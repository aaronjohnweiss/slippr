import requests
from user import User
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("-headless")

base_url = 'https://slippi.gg/user/'
api_url = 'https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql'

post_object = {
  'operationName': 'AccountManagementPageQuery',
  'variables': {
    'cc': 'SYS#0',
    'uid': 'SYS#0'
  },
  'query': 'fragment userProfilePage on User {\n  fbUid\n  displayName\n  connectCode {\n    code\n    __typename\n  }\n  status\n  activeSubscription {\n    level\n    hasGiftSub\n    __typename\n  }\n  rankedNetplayProfile {\n    id\n    ratingOrdinal\n    ratingUpdateCount\n    wins\n    losses\n    dailyGlobalPlacement\n    dailyRegionalPlacement\n    continent\n    characters {\n      id\n      character\n      gameCount\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery AccountManagementPageQuery($cc: String!, $uid: String!) {\n  getUser(fbUid: $uid) {\n    ...userProfilePage\n    __typename\n  }\n  getConnectCode(code: $cc) {\n    user {\n      ...userProfilePage\n      __typename\n    }\n    __typename\n  }\n}\n'
}

rank_map = {
    0: 'Bronze 1',
    766: 'Bronze 2',
    914: 'Bronze 3',
    1055: 'Silver 1',
    1189: 'Silver 2',
    1316: 'Silver 3',
    1436: 'Gold 1',
    1549: 'Gold 2',
    1654: 'Gold 3',
    1752: 'Platinum 1',
    1843: 'Platinum 2',
    1928: 'Platinum 3',
    2004: 'Diamond 1',
    2074: 'Diamond 2',
    2137: 'Diamond 3',
    2192: 'Master 1',
    2275: 'Master 2',
    2350: 'Master 3',
    10000: 'Grandmaster'
}


def get_rank(elo):

    previous_value = rank_map[0]
    for idx, key in enumerate(rank_map):

        if float(elo) < float(key):
            return previous_value
        previous_value = rank_map[key]

    return rank_map[10000]



def get_user_from_tag(tag):
    user = User(tag)

    request_json = post_object.copy()
    request_json['variables']['cc'] = user.tag.upper()
    request_json['variables']['uid'] = user.tag.upper()

    x = requests.post(api_url, json=request_json)

    user_data = x.json()['data']['getConnectCode']['user']
    user.name = user_data['displayName']
    user.elo = user_data['rankedNetplayProfile']['ratingOrdinal']
    user.rank = get_rank(user.elo)
    user.wins = user_data['rankedNetplayProfile']['wins']
    user.losses = user_data['rankedNetplayProfile']['losses']
    user.sets = user_data['rankedNetplayProfile']['ratingUpdateCount']

    return user
