import urllib.request
import ssl
import json



def get_live_data():
    url = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
    scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
    scontext.verify_mode = ssl.VerifyMode.CERT_NONE
    with urllib.request.urlopen(url = url, context=scontext) as f:
        return json.loads(f.read().decode('utf-8'))


def get_level_diff(x):
    """input json output avg lvl diff """
    blue_avg = 0
    red_avg = 0
    for i in range(0,5):
        blue_avg += x[-1]["allPlayers"][i]["level"]
        red_avg += x[-1]["allPlayers"][i+5]["level"]
    blue_avg = blue_avg/5
    red_avg = red_avg/5
    return blue_avg - red_avg

red_towers_ID=[ "Turret_T2_L_03_A",
                "Turret_T2_C_05_A",
                "Turret_T2_R_03_A",
                "Turret_T2_L_02_A",
                "Turret_T2_C_04_A",
                "Turret_T2_R_02_A",
                "Turret_T2_L_01_A",
                "Turret_T2_C_03_A",
                "Turret_T2_R_01_A",
                "Turret_T2_C_02_A",
                "Turret_T2_C_01_A"]

blue_towers_ID=["Turret_T1_L_03_A",
                "Turret_T1_C_05_A",
                "Turret_T1_R_03_A",
                "Turret_T1_L_02_A",
                "Turret_T1_C_04_A",
                "Turret_T1_R_02_A",
                "Turret_T1_L_01_A",
                "Turret_T1_C_03_A",
                "Turret_T1_R_01_A",
                "Turret_T1_C_02_A",
                "Turret_T1_C_01_A"]

def get_teams(x):
    blue_team = []
    red_team = []
    for i in range(0,5):
        blue_team.append(x["allPlayers"][i]["summonerName"])
        red_team.append(x["allPlayers"][i+5]["summonerName"])
    return blue_team,red_team

#what team is active player in?
def team_of_active_player(x):
    name_of_active_player = x['activePlayer']["summonerName"]
    blue_team, _ = get_teams(x)
    if name_of_active_player in blue_team:
        return "blue"
    else:
        return "red"

def towers(x):
    #input game data, #of destroyed towers of active player
    blue_towers_amount = 0
    red_towers_amount = 0
    for i in range(0,len(x["events"]['Events'])):
        
        if x["events"]['Events'][i]["EventName"]  == "TurretKilled": #filtering "tower killed" events
            
            if x["events"]['Events'][i]['TurretKilled'] in red_towers_ID:
                blue_towers_amount += 1
            else:
                red_towers_amount += 1
    if team_of_active_player(x) == "blue":
        return blue_towers_amount
    else:
        return red_towers_amount

#levelDiff
def get_level_diff(x):
    """input json output avg lvl diff """
    blue_avg = 0
    red_avg = 0
    for i in range(0,5):
        blue_avg += x["allPlayers"][i]["level"]
        red_avg += x["allPlayers"][i+5]["level"]
    blue_avg = blue_avg/5
    red_avg = red_avg/5
    return blue_avg - red_avg

def get_assists_diff(x):
    blue_assists_total = 0
    red_assists_total = 0
    for i in range(0,5):
        blue_assists_total += x["allPlayers"][i]["scores"]["assists"]
        red_assists_total += x["allPlayers"][i+5]["scores"]["assists"]
    assists_diff = blue_assists_total-red_assists_total
    if team_of_active_player(x) == "blue":
        return assists_diff
    else:
        return assists_diff*(-1)
    
def get_deaths_diff(x):
    blue_assists_total = 0
    red_assists_total = 0
    for i in range(0,5):
        blue_assists_total += x["allPlayers"][i]["scores"]["deaths"]
        red_assists_total += x["allPlayers"][i+5]["scores"]["deaths"]
    assists_diff = blue_assists_total-red_assists_total
    if team_of_active_player(x) == "blue":
        return assists_diff
    else:
        return assists_diff*(-1)
    
def get_kills_diff(x):
    blue_assists_total = 0
    red_assists_total = 0
    for i in range(0,5):
        blue_assists_total += x["allPlayers"][i]["scores"]["kills"]
        red_assists_total += x["allPlayers"][i+5]["scores"]["kills"]
    assists_diff = blue_assists_total - red_assists_total
    if team_of_active_player(x) == "blue":
        return assists_diff
    else:
        return assists_diff*(-1)
    
def get_dragons_amount(x):
    red_dragons_amount = 0
    blue_dragons_amount = 0
    blue_players,red_players = get_teams(x)
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"] == "DragonKill":
            if x["events"]['Events'][i]['KillerName'] in blue_players:
                blue_dragons_amount += 1
            else:
                 red_dragons_amount += 1
    if team_of_active_player(x) == "blue":
        return blue_dragons_amount
    else:
        return red_dragons_amount

def first_drake(x):
    team_pov = team_of_active_player(x) #"blue" or "red"
    blue_players, _ = get_teams(x) #2lists of players
    first_drake_receivers = ""
    
    for i in range(0,len(x["events"]['Events'])):
        if (x["events"]['Events'][i]["EventName"] == "DragonKill"):
            if (x["events"]['Events'][i]['KillerName'] in blue_players):
                first_drake_receivers = "blue"
                break
            else:
                first_drake_receivers = "red"
                break

    if first_drake_receivers == "blue" and team_pov =="blue":
        return 1
    elif first_drake_receivers == "red" and team_pov =="red":
        return 1
    else:
        return 0
    
def get_inhibs_amount(x):
    red_inhibs = ["Barracks_T2_L1", "Barracks_T2_C1", "Barracks_T2_R1"]
    blue_team_destroyed_amount = 0
    red_team_destroyed_amount = 0
    for i in range(len(x["events"]['Events'])):
        if x["events"]['Events'][i]['EventName'] == 'InhibKilled':
            if x["events"]['Events'][i]['InhibKilled'] in red_inhibs:
                blue_team_destroyed_amount +=1
            else:
                red_team_destroyed_amount +=1
    if team_of_active_player(x) == "blue":
        return blue_team_destroyed_amount
    else:
        return red_team_destroyed_amount
    
def bot_towers_amount(x):    
    red_bot_towers = ["Turret_T2_R_03_A", "Turret_T2_R_02_A","Turret_T2_R_01_A", "Turret_T2_C_01_A"]
    blue_bot_towers = ["Turret_T1_R_03_A", "Turret_T1_R_02_A","Turret_T1_R_01_A", "Turret_T1_C_01_A"]
    blue_amount = 0
    red_amount = 0
    for i in range(len(x["events"]['Events'])):
        if x["events"]['Events'][i]['EventName'] == 'TurretKilled':
            if x["events"]['Events'][i]["TurretKilled"] in blue_bot_towers:
                red_amount += 1
            elif x["events"]['Events'][i]["TurretKilled"] in red_bot_towers:
                blue_amount += 1
    if team_of_active_player(x) == "blue":
        return blue_amount
    else:
        return red_amount
    
def top_towers_amount(x):    
    red_bot_towers = ["Turret_T2_L_03_A","Turret_T2_L_02_A", "Turret_T2_L_01_A","Turret_T2_C_02_A"]
    blue_bot_towers = ["Turret_T1_L_03_A","Turret_T1_L_02_A","Turret_T1_L_01_A","Turret_T1_C_02_A"]
    blue_amount = 0
    red_amount = 0
    for i in range(len(x["events"]['Events'])):
        if x["events"]['Events'][i]['EventName'] == 'TurretKilled':
            if x["events"]['Events'][i]["TurretKilled"] in blue_bot_towers:
                red_amount += 1
            elif x["events"]['Events'][i]["TurretKilled"] in red_bot_towers:
                blue_amount += 1
    if team_of_active_player(x) == "blue":
        return blue_amount
    else:
        return red_amount

def mid_towers_amount(x):    
    red_bot_towers = ["Turret_T2_C_05_A","Turret_T2_C_04_A","Turret_T2_C_03_A"]
    blue_bot_towers = ["Turret_T1_C_05_A", "Turret_T1_C_04_A","Turret_T1_C_03_A"]
    blue_amount = 0
    red_amount = 0
    for i in range(len(x["events"]['Events'])):
        if x["events"]['Events'][i]['EventName'] == 'TurretKilled':
            if x["events"]['Events'][i]["TurretKilled"] in blue_bot_towers:
                red_amount += 1
            elif x["events"]['Events'][i]["TurretKilled"] in red_bot_towers:
                blue_amount += 1
    if team_of_active_player(x) == "blue":
        return blue_amount
    else:
        return red_amount

def first_tower(x):
    team_pov = team_of_active_player(x) #"blue" or "red"
    blue_players, _ = get_teams(x) #2lists of players
    first_drake_receivers = ""
    
    for i in range(0,len(x["events"]['Events'])):
        if (x["events"]['Events'][i]["EventName"] == "TurretKilled"):
            if (x["events"]['Events'][i]["TurretKilled"] in red_towers_ID):
                first_drake_receivers = "blue"
                break
            else:
                first_drake_receivers = "red"
                break

    if first_drake_receivers == "blue" and team_pov =="blue":
        return 1
    elif first_drake_receivers == "red" and team_pov =="red":
        return 1
    else:
        return 0

def first_blood(x):
    blue_players, _ = get_teams(x)
    fb_recipient =""
    
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"] == "FirstBlood":
            if x["events"]['Events'][i]["Recipient"] in blue_players:
                fb_recipient = "blue"
            else:
                fb_recipient = "red"
    
    if team_of_active_player(x) == "blue" and fb_recipient == "blue":
        return 1
    elif team_of_active_player(x) == "red" and fb_recipient == "red":
        return 1
    else:
        return 0
    
def herald_amount(x):
    blue_heralds=0
    red_heralds=0
    blue_players, _ = get_teams(x)
    
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"] == "HeraldKill":
            if x["events"]['Events'][i]["KillerName"] in blue_players:
                blue_heralds+=1
            else:
                red_heralds+=1
    if team_of_active_player(x) == "blue":
        return blue_heralds
    else:
        return red_heralds

def first_inhib(x):
    red_inhibs = ["Barracks_T2_L1", "Barracks_T2_C1", "Barracks_T2_R1"]
    first_inhib_receiver = ""
    for i in range(0,len(x["events"]['Events'])):
        if x["events"]['Events'][i]["EventName"]=="InhibKilled":
            if x["events"]['Events'][i]["InhibKilled"] in red_inhibs:
                first_inhib_receiver = "blue"
            else:
                first_inhib_receiver = "red"
    if team_of_active_player(x) == "blue" and first_inhib_receiver == "blue":
        return 1
    elif team_of_active_player(x) == "red" and first_inhib_receiver == "red":
        return 1
    else:
        return 0
    
def cs_diff(x):
    blue_cs=0
    red_cs=0
    for i in range(5):
        blue_cs += x["allPlayers"][i]['scores']["creepScore"]
        red_cs += x["allPlayers"][i+5]['scores']["creepScore"]
    cs_diff = blue_cs - red_cs
    if team_of_active_player(x) == "blue":
        return cs_diff
    else:
        return cs_diff*(-1)

def jungle_cs_diff(x):
    blue_cs=0
    red_cs=0
    for i in range(5):
        if x["allPlayers"][i]['position'] == "JUNGLE":
            if x["allPlayers"][0]["team"] == "ORDER":              #ORDER is blue team
                blue_cs = x["allPlayers"][i]['scores']["creepScore"]
            else:
                red_cs += x["allPlayers"][i]['scores']["creepScore"]
    cs_diff = blue_cs - red_cs
    if team_of_active_player(x) == "blue":
        return cs_diff
    else:
        return cs_diff*(-1)    

def timestamp(x):
    return x['gameData']["gameTime"]

def current_stats(x):
    current_game_stats = {}
    current_game_stats["time"] = timestamp(x)
    current_game_stats["first_blood"] = first_blood(x)
    current_game_stats["first_tower"] = first_tower(x)
    current_game_stats["first_inhib"] = first_inhib(x)
    current_game_stats["mid_towers_amount"] = mid_towers_amount(x)
    current_game_stats["top_towers_amount"] = top_towers_amount(x)
    current_game_stats["bot_towers_amount"] = bot_towers_amount(x)
    current_game_stats["inhibs_amount"] = get_inhibs_amount(x)
    current_game_stats["first_dragon"] = first_drake(x)
    current_game_stats["Dragons_Amount"] = get_dragons_amount(x)
    current_game_stats["Heralds_amount"] = herald_amount(x)
    current_game_stats["Kills_Diff"] = get_kills_diff(x)
    current_game_stats["Death_Diff"] = get_deaths_diff(x)
    current_game_stats["Assist_Diff"] = get_assists_diff(x)
    current_game_stats["Lvl_Diff"] = get_level_diff(x)
    current_game_stats["cs_Diff"] = cs_diff(x)
    current_game_stats["jungle_cs_Diff"] = jungle_cs_diff(x)
    current_game_stats["win_probability"] = 0.5
    return current_game_stats

