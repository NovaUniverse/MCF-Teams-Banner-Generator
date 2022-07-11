import sys
from teams_banner_generator import NovaGamesTeamsBannerGen

if __name__ == "__main__":
    nova_games = NovaGamesTeamsBannerGen(cli_args=sys.argv)
    nova_games.save(nova_games.create()[0], f"Lol - Nova Games", "png")