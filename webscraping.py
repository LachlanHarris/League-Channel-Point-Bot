import streams

def champion_wr_value(player_stats):
    if (player_stats == "-"):
        return 0
    wr = player_stats.split("%")[0]
    games = player_stats.split("(")[1][:-8]     
    
    value = 0
    games = int(games)
    wr = float(wr)/100
        
    if 0 < games < 15:
        value = wr * 0.5
    if 15 <= games < 30:
        value = wr * 0.65
    if 30 <= games < 50:
        value = wr * 0.75
    if 50 <= games < 75:
        value = wr * 0.80
    if 75 <= games < 150:
        value = wr * 0.90
    if 150 < games:
        value = wr * 1
    return value

def player_wr_value(player_stats):
    wr = player_stats.split("%")[0]
    games = player_stats.split("(")[1][:-8]  
        
    value = 0
    games = int(games)
    wr = float(wr)/100
        
    if 0 < games < 50:
        value = wr * 0.5
    if 50 <= games < 75:
        value = wr * 0.6
    if 75 <= games < 150:
        value = wr * 0.75
    if 150 <= games < 300:
        value = wr * 0.8
    if 300 <= games < 500:
        value = wr * 0.9
    if 500 < games < 1000:
        value = wr * 0.95
    if 1000 < games:
        value = wr * 1
    return value

def compute_team_value(team):
    team_overall = 0
    for i in range(0,5):
        champ_wr = champion_wr_value(team["Preseason Champion Information"][i])
        player_wr = player_wr_value(team["Ranked Winratio"][i])
        
        team_overall += champ_wr
        team_overall  += player_wr
        
    return team_overall

def return_winning_team(blue_team, red_team):
    blue_value = compute_team_value(blue_team)
    red_value = compute_team_value(red_team)
    
    if red_value >= blue_value:
        return "RED"
    else:
        return "BLUE"

def find_team_of_streamer(blue_team, red_team, streamer):
    for x in blue_team[blue_team.columns[3]]:
        if x == streamer:
            return "BLUE"
    for x in red_team[red_team.columns[3]]:
        if x == streamer:
            return "RED"

def win_loss_prediction_answer(blue_team, red_team, streamer):
    #find in game name from streamer name
    IGN = streams.Streams[streamer].split("/")
    IGN = IGN [-2]
    #use this to replace html spaces with string spaces
    IGN = IGN.replace("%20" , " ")
    #compute winner using our methods
    winner = return_winning_team(blue_team, red_team)
    teamOfStreamer = find_team_of_streamer(blue_team, red_team, IGN)

    #if they match we return true to bet yes
    #if they dont we return false to bet no 
    if winner == teamOfStreamer:
        return True
    else:
        return False

