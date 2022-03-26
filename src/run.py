from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import requests
import datetime
import os

current_working_dir = os.getcwd()

#  Grabing json file and opening it with json encorder and shit.

teams_json_file_path = input("Drag teams.json in here and hit enter --> ")

teams_json = json.load(open(teams_json_file_path, mode="r"))

# Generate teams dict.
max_teams = 13
teams = {}
for team_num in range(1, max_teams):
    teams[f"{team_num}"] = []

# Sorting the teams data.
for player in teams_json:
    uuid = player["uuid"]
    name = player["username"]
    team = player["team_number"]
    
    teams[f"{team}"].append({"ign":name, "uuid":uuid})

# Storing todays date.
date = datetime.datetime.now().strftime("%d.%m.%Y")

#  Now we're generating that UwU image of yours.
#-------------------------------------------------
bg_image_uwu = Image.open("./assets/background_1.png", mode="r")
bg_image_uwu = bg_image_uwu.filter(ImageFilter.GaussianBlur(radius=5))

image_uwu = Image.new(mode="RGB", size=(1920, 1080))

image_uwu.paste(bg_image_uwu)

# Place Title Text

title_text = f"MCF Teams - {date}"
title_font = ImageFont.truetype('./assets/MilkyNice_Clean.ttf', 120)

title_blur_layer = Image.new('RGBA', image_uwu.size)
title_blur = ImageDraw.Draw(title_blur_layer)
w, h = title_blur.textsize(title_text, font=title_font)
title_blur.text(((image_uwu.width-w)/2, 10), title_text, font=title_font, fill="black")
title_blur_layer = title_blur_layer.filter(ImageFilter.BoxBlur(9))
image_uwu.paste(title_blur_layer, title_blur_layer)

title = ImageDraw.Draw(image_uwu)
w, h = title.textsize(title_text, font=title_font)
title.text(((image_uwu.width-w)/2, 10), title_text, font=title_font, fill=(192, 59, 108))

# Generate Teams Sting
teams_string = ""
for team in teams:
    print(teams[team])

    if not teams[team] == []: # If team not empty.
        if len(teams[team]) == 1:
            player_1 = teams[team][0]["ign"]
            if len(player_1) >= 30:
                player_1 = player_1[0:24] + "..."

            players_string = f"{player_1}". center(31)
        else:
            player_1 = teams[team][0]["ign"]
            player_2 = teams[team][1]["ign"]

            if len(player_1) >= 20:
                player_1 = player_1[0:15] + "..."

            if len(player_2) >= 20:
                player_2 = player_2[0:15] + "..."

            players_string = f"{player_1} & {player_2}".center(28)

        teams_string += f"• TEAM {team}: {players_string}\n"

    else:
        no_players = "[Free Team]"
        teams_string += f"• TEAM {team}: {no_players}\n"

print(teams_string)

# Place Teams Text

teams_text = teams_string
teams_font = ImageFont.truetype('./assets/MilkyNice_Clean.ttf', size=65, encoding="utf-8")

teams_blur_layer = Image.new('RGBA', image_uwu.size)
teams_blur = ImageDraw.Draw(teams_blur_layer)
w, h = teams_blur.textsize(teams_text, font=teams_font)
teams_blur.text(((image_uwu.width-w)/2, 180), teams_text, font=teams_font, fill="black")
teams_blur_layer = teams_blur_layer.filter(ImageFilter.BoxBlur(8))
image_uwu.paste(teams_blur_layer, teams_blur_layer)

teams_draw = ImageDraw.Draw(image_uwu)
w, h = teams_draw.textsize(teams_text, font=teams_font)
teams_draw.text(((image_uwu.width-w)/2, 180), teams_text, font=teams_font, fill=(250, 220, 168))

# Place novauniverse branding.
nova_logo = Image.open("./assets/novauniverse_logo.png", mode="r")
nova_logo = nova_logo.resize((300, 300))
offset = (1620, 800)
image_uwu.paste(nova_logo, offset, mask=nova_logo)
 
# Save the UwU image file.
image_uwu.save(f"./dest/{date} - MCF Teams.png")

#  Open the UwU png file.
os.startfile(f"{current_working_dir}/dest/{date} - MCF Teams.png")