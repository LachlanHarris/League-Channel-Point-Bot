import streams

def calculate_average_champion_wr(team):
    team_overall = 0
    for i in range(0,5):
        wr = team["Preseason Champion Information"][i].split("%")[0]
            #add 45 for players who are playing a character for the first time
        if wr == "-":
            team_overall += 45
        else:
            team_overall += int(wr)
    return team_overall

def higher_champ_wr_value(blue_team, red_team):
    blue_wr_avg = calculate_average_champion_wr(blue_team)
    red_wr_avg = calculate_average_champion_wr(red_team)
    print(blue_wr_avg, red_wr_avg)
    if blue_wr_avg > red_wr_avg:
        return "BLUE"
    else:
        return "RED"

#here we make a crude calculation of the rank of each player and the team average
def calculate_average_LP(team):
    accepted_ranks = ["master","grandmaster","challenger"]
    team_overall = 0
    
    for i in range(0,5):
        #cleaning the parsed data removing brackets and taking tier/LP
        split = team["Preseason.1"][i].split("(")
        tier = split[0]
        
        #slice off last 3 digits to remove "LP)"
        LP = split[1][:-3]
        
        #if the player is not within the top 3 rank tiers thier values are not counted
        if tier in accepted_ranks:
            team_overall += int(LP)
            
    return team_overall

#find which of the two teams has a higher LP average
def higher_avg_LP_value(blue_team,red_team):
    blue_LP_avg = calculate_average_LP(blue_team)
    red_LP_avg = calculate_average_LP(red_team)
    print(blue_LP_avg, red_LP_avg)
    if blue_LP_avg > red_LP_avg:
        return "BLUE"
    else:
        return "RED"

def find_winner(blue_team, red_team):
    blue = 0
    red = 1
    #red starts with one more point because the matchmaking system makes the red side have the higher MMR players
    #there is probably a better way to implement this
    if (higher_champ_wr_value(blue_team,red_team)) == "RED":
        red += 1
    else:
        blue += 1
        
    if (higher_avg_LP_value(blue_team, red_team)) == "RED":
        red += 1
    else:
        blue += 1
        
    if red > blue:
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
    winner = find_winner(blue_team, red_team)
    #find which team the player is on
    teamOfStreamer = find_team_of_streamer(blue_team, red_team, IGN)

    #if they match we return true to bet yes
    #if they dont we return false to bet no 
    if winner == teamOfStreamer:
        return True
    else:
        return False

