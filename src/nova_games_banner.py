import sys
from teams_banner_generator import NovaGamesTeamsBannerGen

if __name__ == "__main__":
    nova_games = NovaGamesTeamsBannerGen(cli_args=sys.argv)

    count = 0

    for banner in nova_games.create():
        count += 1
        nova_games.save(banner, f"{nova_games.date} - Nova Games Team Banner ({count})", "png")