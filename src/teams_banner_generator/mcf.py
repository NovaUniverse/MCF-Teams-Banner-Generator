import datetime
from typing import List
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import dateparser

from . import BannerGen, Background_Images

class MCFTeamsBannerGen(BannerGen):
    def __init__(self, cli_args: List[str] = []):
        super().__init__(cli_args)

    def create(self):
        """Creates mcf teams banner."""

        teams_json = json.load(open(self.teams_json_file_path, mode="r"))

        # Generate teams dict.
        if self.max_teams == None: 
            max_teams = 12
        else: 
            max_teams = int(self.max_teams)

        teams = {}
        for team_num in range(1, max_teams + 1):
            teams[f"{team_num}"] = []

        # Sorting the teams data.
        for player in teams_json:
            uuid = player["uuid"]
            name = player["username"]
            team = player["team_number"]
            
            try:
                teams[f"{team}"].append({"ign":name, "uuid":uuid})
            except KeyError:
                pass

        # Storing todays date.
        if not self.date_string == None:
            date = dateparser.parse(self.date_string, date_formats=["%d/%m/%Y", "%Y/%m/%d"]).strftime("%d.%m.%Y")
        else:
            date = datetime.datetime.now().strftime("%d.%m.%Y")

        return self.generate(teams, date)

    def generate(self, teams:dict, date:str):
        """Generates the actual image. UwU"""

        # Getting and placing background
        bg = Background_Images("./assets/mcf_background_images")

        bg_image_uwu = Image.open(bg.get_random(), mode="r")
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
        teams_string_2 = ""
        for team in teams:
            print(teams[team])

            if not teams[team] == []: # If team not empty.
                if len(teams[team]) == 1:
                    player_1 = teams[team][0]["ign"]
                    if len(player_1) >= 30:
                        player_1 = player_1[0:24] + "..."

                    players_string = f"{player_1}".center(31)
                else:
                    player_1 = teams[team][0]["ign"]
                    player_2 = teams[team][1]["ign"]

                    if len(player_1) >= 13:
                        player_1 = player_1[0:9] + "..."

                    if len(player_2) >= 13:
                        player_2 = player_2[0:9] + "..."

                    players_string = f"{player_1} & {player_2}".center(28)

                if len(teams_string.splitlines()) >= 12:
                    teams_string_2 += f"• TEAM {team}: {players_string}\n"
                else:
                    teams_string += f"• TEAM {team}: {players_string}\n"

            else:
                no_players = "[Free Team]"
                if len(teams_string.splitlines()) >= 12:
                    teams_string_2 += f"• TEAM {team}: {no_players}\n"
                else:
                    teams_string += f"• TEAM {team}: {no_players}\n"

        print(teams_string)
        print(teams_string_2)

        # Place novauniverse branding.
        self.place_nova_branding(image_uwu)

        #  Place Teams Text
        if not teams_string_2 == "": size = 45
        else: size = 65

        def place_teams_text(teams_text, string_num:int=None):
            teams_font = ImageFont.truetype('./assets/MilkyNice_Clean.ttf', size=size, encoding="utf-8")
            if not teams_string_2 == "":
                spacing = 10
            else:
                spacing = 1

            if not string_num == None:
                if string_num == 1:
                    x_placement = 16
                if string_num == 2:
                    x_placement = 1.035

                y_placement = 70
            else:
                x_placement = 2
                y_placement = 0

            teams_blur_layer = Image.new('RGBA', image_uwu.size)
            teams_blur = ImageDraw.Draw(teams_blur_layer)
            w, h = teams_blur.multiline_textsize(teams_text, font=teams_font)
            teams_blur.multiline_text((((image_uwu.width-w)/x_placement) + 2, 192 + y_placement), teams_text, font=teams_font, fill="black", spacing=spacing)
            teams_blur_layer = teams_blur_layer.filter(ImageFilter.BoxBlur(3))
            image_uwu.paste(teams_blur_layer, teams_blur_layer)

            teams_draw = ImageDraw.Draw(image_uwu)
            w, h = teams_draw.multiline_textsize(teams_text, font=teams_font)
            teams_draw.multiline_text(((image_uwu.width-w)/x_placement, 190 + y_placement), teams_text, font=teams_font, fill=(250, 220, 168), spacing=spacing)

        if not teams_string_2 == "":
            place_teams_text(teams_string, 1)
            place_teams_text(teams_string_2, 2)
        else:
            place_teams_text(teams_string)

        return image_uwu