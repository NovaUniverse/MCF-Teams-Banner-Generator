import sys
from teams_banner_generator import MCFTeamsBannerGen

if __name__ == "__main__":
    mcf = MCFTeamsBannerGen(cli_args=sys.argv)
    mcf.save(mcf.create(), f"{mcf.date} - MCF Teams", "png")