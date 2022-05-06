import html

from telegram.utils.helpers import escape_markdown


def format_data(data):
    text = ""
    for game in data:
        text += f"*LEAGUE: {game['tournament']}* \n"
        text += f"*{game['home']} v {game['away']}*\n"
        text += f"SCORES: {game['scores']}\n"
        text += f"Minutes Played: {game['time']}\n"
        text += f"_{game['status']}_\n"
        text += f"GAME PLAYED: {game['game_played']} \n"
        if game['is_winning'] and game['is_winning'] != 'Error':
            text += f"_Game Status_: *Winning* \n"
        elif not game['is_winning'] and game['is_winning'] != 'Error':
            text += f"_Game Status_: *Losing* \n"
        else:
            text += f"_Game Status_: *null* \n"

        text += "\n\n"

    return text


def welcome_text(username):
    text = ''
    text += f'Welcome {username} \n'
    text += 'I will help you keep track of all your sporty games. '
    text += "To set a game to be tracked, select the /check_bet command. You'd be asked to input the sporty code. \n"
    text += 'On selecting a valid sporty bet code, The current state of the ticket would be displayed. Then ' \
            'subsequent update messages would be broadcast to you. \n\n'
    text += 'Thank you for using this bot, Good luck to your games! ;)'
    return text


def format_markdown_text(text):
    pass
