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
