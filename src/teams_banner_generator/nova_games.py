import datetime
import time
from typing import Dict, List
import json, os, sys
import webview
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import dateparser

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from io import BytesIO

from . import BannerGen, Background_Images

class TeamColours():
    BLACK = (0, 0, 0)
    DARK_BLUE = (0, 0, 170)
    DARK_GREEN = (0, 170, 0)
    DARK_AQUA = (0, 170, 170)
    DARK_RED = (170, 0, 0)
    DARK_PURPLE = (170, 0, 170)
    GOLD = (255, 170, 0)
    GRAY = (170, 170, 170)
    DARK_GRAY = (85, 85, 85)
    BLUE = (85, 85, 255)
    GREEN = (85, 255, 85)
    AQUA = (85, 255, 255)
    RED = (255, 85, 85)
    LIGHT_PURPLE = (255, 85, 255)
    YELLOW = (255, 255, 85)
    WHITE = (255, 255, 255)

class NovaGamesTeamsBannerGen(BannerGen):
    def __init__(self, cli_args: List[str] = []):
        self.date = None

        self.team_colours:dict = {
            "1" : TeamColours.DARK_BLUE,
            "2" : TeamColours.DARK_GREEN,
            "3" : TeamColours.DARK_AQUA,
            "4" : TeamColours.DARK_RED,
            "5" : TeamColours.DARK_PURPLE,
            "6" : TeamColours.GOLD,
            "7" : TeamColours.GRAY,
            "8" : TeamColours.DARK_GRAY,
            "9" : TeamColours.BLUE,
            "10" : TeamColours.GREEN,
            "11" : TeamColours.AQUA,
            "12" : TeamColours.RED,
            "13" : TeamColours.LIGHT_PURPLE,
            "14" : TeamColours.YELLOW,
            "15" : TeamColours.WHITE,
        }

        self.team_names:dict = {
            "1" : "Navy  Narwhals",
            "2" : "Green  Guppys",
            "3" : "Teal  Turtles",
            "4" : "Crimson  Chipmunks",
            "5" : "Purple  Peacocks",
            "6" : "Golden  Geckos",
            "7" : "Silver  Snakes",
            "8" : "White  Wolves",
            "9" : "Blue  Bears",
            "10" : "Green  Geese",
            "11" : "Cyan  Cats",
            "12" : "Red  Rats",
            "13" : "Pink  Platypus",
            "14" : "Yellow  Yaks"
        }

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')

        self.driver = webdriver.Chrome(f"./teams_banner_generator/chromedriver_{sys.platform}.exe", chrome_options=options)

        super().__init__(cli_args)

    def create(self):
        """Creates nova games teams banner."""

        teams_json = json.load(open(self.teams_json_file_path, mode="r"))

        if self.max_teams == None: 
            max_teams = 14
        else: 
            max_teams = int(self.max_teams)

        teams = {}
        for team_num in range(1, max_teams + 1):
            teams[f"{team_num}"] = []

        # Sorting the teams data.
        for player in teams_json:
            uuid = player["uuid"]
            name = player["username"]
            team_num = player["team_number"]
            channel_url = player["channel_url"]
            
            try:
                teams[f"{team_num}"].append({"ign":name, "uuid":uuid, "channel_url":channel_url})
            except KeyError:
                pass

        # Storing todays date.date
        if not self.date_string == None:
            self.date = dateparser.parse(self.date_string, date_formats=["%d/%m/%Y", "%Y/%m/%d"]).strftime("%d.%m.%Y")
        else:
            self.date = datetime.datetime.now().strftime("%d.%m.%Y")

        return self.generate(teams, self.date)

    def generate(self, teams:dict, date:str):
        """Generates the actual image. UwU"""

        print(teams)

        # Getting and placing background
        team_template_image_path = "./assets/nova_games_assets/template_banner.png"
        team_template_image = Image.open(team_template_image_path, mode="r").convert("RGBA")

        team_banner_list:List[Image.Image] = []

        for team in teams:
            team_banner_image = Image.new(mode="RGBA", size=team_template_image.size, color=(201, 0, 52))
            
            player_count = 0

            for player in teams[team]:
                
                # Get player channel pfp.
                channel_url = player["channel_url"]

                pfp_url = self.get_pfp(channel_url)
                print(self.BLUE(f"Profile Picture URL >>> {pfp_url}"))
                response = requests.get(pfp_url)

                player_channel_pfp = Image.open(BytesIO(response.content))
                player_channel_pfp = player_channel_pfp.resize((550, 550)).convert("RGBA")

                team_banner_image.paste(player_channel_pfp, (275 + (740*player_count), int(team_template_image.size[1]/3 + 10)))
                
                player_count += 1

            team_banner_image = Image.alpha_composite(team_banner_image, team_template_image)

            # Place Team Name
            #====================
            team_name_text = f"{self.team_names[team]}"
            team_name_font = ImageFont.truetype('./assets/mustardo.ttf', 200)

            team_name_blur_layer = Image.new('RGBA', team_banner_image.size)
            team_name_blur = ImageDraw.Draw(team_name_blur_layer)
            w, h = team_name_blur.textsize(team_name_text, font=team_name_font)
            team_name_blur.text(((team_banner_image.width-w)/2 + 4, (team_banner_image.height-h)/1.048 + 4), team_name_text, font=team_name_font, fill="black")
            team_name_blur_layer = team_name_blur_layer.filter(ImageFilter.BoxBlur(1))
            team_banner_image.paste(team_name_blur_layer, team_name_blur_layer)

            team_name = ImageDraw.Draw(team_banner_image)
            w, h = team_name.textsize(team_name_text, font=team_name_font)
            team_name.text(((team_banner_image.width-w)/2, (team_banner_image.height-h)/1.048), team_name_text, font=team_name_font, fill=self.team_colours[team])

            team_banner_list.append(team_banner_image)

        return team_banner_list

    def get_pfp(self, channel_url:str):
        if "https://www.youtube.com/" in channel_url:
            return self.get_yt_pfp(channel_url + "/about")

        if "https://www.twitch.tv/" in channel_url:
            return self.get_twitch_pfp(channel_url + "/about")

    def get_yt_pfp(self, channel_url:str):
        html = requests.get(channel_url, cookies={"CONSENT": "YES+1"}).text
        soup = BeautifulSoup(html, "html.parser")
        data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)
        json_data = json.loads(data)

        channel_logo_url:str = json_data["header"]["c4TabbedHeaderRenderer"]["avatar"]["thumbnails"][2]["url"]
        channel_logo_url = channel_logo_url.replace("s176", "s1000") # Resize
        return channel_logo_url

    def get_twitch_pfp(self, channel_url:str):
        self.driver.get(channel_url)

        time.sleep(0.25)

        page = self.driver.execute_script('return document.body.innerHTML')

        soup = BeautifulSoup(page, "html.parser")
        channel_logo_div = soup.find_all("div", class_="Layout-sc-nxg1ff-0 hhcjeu")[0]
        channel_logo_url:str = channel_logo_div.find_all("img", class_="InjectLayout-sc-588ddc-0 iDjrEF tw-image tw-image-avatar")[0]["src"]

        channel_logo_url = channel_logo_url.replace("70x70", "600x600") # Resize
        return channel_logo_url