from typing import List
from PIL import Image
import sys, os, random

from devgoldyutils import Console

if sys.platform == "win32": os.system("color")

class BannerGen(Console):
    def __init__(self, cli_args:List[str]=[], dont_ask=False):
        self.is_none = ["", "none", "null", None]

        self.cli_args = cli_args

        self.teams_json_file_path = self.get_arg(arg_num=1, text=self.BLUE("Drag teams.json in here and hit enter --> "), required=True, dont_ask=dont_ask)
        self.date_string = self.get_arg(arg_num=2, text=self.PURPLE("Enter the date this event is taking place. (FORMAT: 01/04/2030) [Default: Todays Date] --> "), dont_ask=dont_ask)
        self.max_teams = self.get_arg(arg_num=3, text=self.CLAY("Max Number of Teams [Default: 12] --> "), dont_ask=dont_ask)
            
        self.dont_open_file = self.get_arg(arg_num=4, dont_ask=True)
        self.save_location = self.get_arg(arg_num=5, dont_ask=True)

        if not "dest" in os.listdir("./"): os.mkdir("./dest")

    def enter(self, text:str, required=False):
        """A method to print and get input from command line."""
        output = input(text)

        if output in self.is_none: 
            if required == True: 
                print(self.RED("[THIS OPTION IS REQUIRED!]"))
                self.enter(text, required=True)
            else: return None

        return output

    def get_arg(self, arg_num:int, text:str=None, required=False, dont_ask=False):
        """Processes cli argument."""
        try:
            option = self.cli_args[arg_num]
            if option in self.is_none: 
                return None
            return option
        except IndexError:
            if dont_ask == True:
                return None
            else:
                return self.enter(text, required)

    def place_nova_branding(self, image:Image.Image, offset:tuple=(1665, 835)):
        """Place novauniverse branding. UwU"""
        nova_logo = Image.open("./assets/novauniverse_logo.png", mode="r")
        nova_logo = nova_logo.resize((260, 260))
        image.paste(nova_logo, offset, mask=nova_logo)

    def save(self, image:Image.Image, file_name:str, file_type:str, location=None):
        """Saves banner."""
        if location == None: location = self.save_location
        if location == None: location = "./dest"

        image.save(f"{location}/{file_name}.{file_type}")

        return f"{location}/{file_name}.{file_type}"

    def open(self, file_path:str):
        if self.dont_open_file == None:
            os.startfile(file_path)

class Background_Images():
    def __init__(self, bg_images_folder_dir:str):
        self.bg_images_folder_dir = bg_images_folder_dir

    def get_one(self, bg_number:int=1):
        """Returns a backgrounud image from that directory."""
        return f"{self.bg_images_folder_dir}/background_{bg_number}.png"

    def get_random(self):
        return f"{self.bg_images_folder_dir}/background_{random.randint(1, len(os.listdir(self.bg_images_folder_dir)))}.png"

from .mcf import MCFTeamsBannerGen
from .nova_games import NovaGamesTeamsBannerGen