from flask import *
from flask import Flask

from teams_banner_generator import NovaGamesTeamsBannerGen, MCFTeamsBannerGen

available_tournaments = ["NovaGames", "MCF"]
output_folder = "./dest"

app = Flask("teams_banner_generator")

from . import endpoints