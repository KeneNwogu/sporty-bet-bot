from database import games, events
import requests
from scrapers.scraper import url


def check_if_game_has_changed():
    tickets = list(games.find({'finished': False}))
    for ticket in list(map(lambda x: x.get('ticket'), tickets)):
        games_url = url + ticket
        games_object = requests.get(games_url).json()
        outcomes = games_object['data']['outcomes']

        for outcome in outcomes:
            current_home_score = outcome.get('setScore').split(':')[0]
            current_away_score = outcome.get('setScore').split(':')[1]
            current_status = outcome.get("matchStatus")

            event = events.find_one({'match_id': outcome.get('eventId')})
            if event.get('home_score') != current_home_score or \
                    event.get('away_score') != current_away_score or event.get('status') != current_status:
                # update db and update users
                events.update_one({'match_id': outcome.get('eventId')}, {
                    "$set": {
                        "home_score": current_home_score,
                        "away_score": current_away_score,
                        "status": current_status
                    }
                })

                # update users
                text = ''
                text += f'UPDATE: \n\n'
                text += f'MATCH: *{event.get("home")}* vs *{event.get("away")}* \n'
                text += f'SCORES: {current_home_score} : {current_away_score} \n'
                text += f'STATUS: {current_status} \n'
                text += f'TIME: *{outcome.get("playedSeconds")}* \n\n'

                users = list(map(lambda x: x.get('chat_id'), event.get('users')))
                from bot import updater
                for user in users:
                    # send ticket event occurs in to user
                    user_tickets = list(filter(lambda x: x.get('chat_id') == user, event.get('users')))
                    user_event_tickets = ' '
                    if len(user_tickets) > 0:
                        user_event_tickets = user_event_tickets.join(user_tickets[0].get('tickets'))
                    text += f'TICKETS: {user_event_tickets} \n'
                    updater.bot.send_message(user, text=text, parse_mode='MarkdownV2')
        # check if all outcomes are Ended for game and mark game as finished
        if all([x.get('matchStatus') == 'Ended' for x in outcomes]):
            games.update_one({'ticket': ticket}, {
                '$set': {
                    'finished': True
                }
            })
