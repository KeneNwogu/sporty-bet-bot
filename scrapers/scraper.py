import requests
from database import events

url = "https://www.sportybet.com/api/ng/orders/share/"


def get_games(bet_code: str, user_id: str):
    games_url = url + bet_code
    games_object = requests.get(games_url).json()

    if games_object.get('innerMsg') == "Invalid":
        raise ValueError('Invalid Game Code')

    outcomes = games_object['data']['outcomes']
    games_details = []

    for outcome in outcomes:
        data = {}
        # set events to db
        if not events.find_one({"match_id": outcome.get('eventId')}):
            events.insert_one({
                'match_id': outcome.get('eventId'),
                'tickets': [bet_code],
                'home': outcome["homeTeamName"],
                'away': outcome["awayTeamName"],
                'home_score': outcome.get('setScore', '0:0').split(':')[0],
                'away_score': outcome.get('setScore', '0:0').split(':')[1],
                'status': outcome.get("matchStatus"),
                'users': [{'chat_id': user_id, 'tickets': [bet_code]}]
            })
        else:
            # check if user is in current event handler
            if not events.find_one({"match_id": outcome.get('eventId'), "users.chat_id": user_id}):
                events.update_one({"match_id": outcome.get('eventId')}, {
                    "$addToSet": {
                        "users": {
                            "chat_id": user_id,
                            "tickets": [bet_code]
                        }
                    }
                })
            else:
                events.update_one({"match_id": outcome.get('eventId'), "users.chat_id": user_id}, {
                    "$addToSet": {
                        "users.$.tickets": bet_code
                    }
                })
            events.update_one({"match_id": outcome.get('eventId')}, {"$addToSet": {"tickets": bet_code}})

        data['home'] = outcome["homeTeamName"]
        data['away'] = outcome["awayTeamName"]
        data["scores"] = outcome.get('setScore')
        data["time"] = outcome.get("playedSeconds")
        data["status"] = outcome.get("matchStatus")
        data['sport'] = outcome["sport"]["name"]
        data['country'] = outcome["sport"]["category"]["name"]
        data['tournament'] = outcome["sport"]["category"]["tournament"]["name"]
        # print(len(outcome["markets"][0]["outcomes"]))
        try:
            data["game_played"] = outcome["markets"][0]["outcomes"][0]["desc"]
            data["win_probability"] = outcome["markets"][0]["outcomes"][0].get("probability")
        except IndexError:
            data["game_played"] = None
            data["win_probability"] = None
        else:
            games_details.append(data)

    return games_details
