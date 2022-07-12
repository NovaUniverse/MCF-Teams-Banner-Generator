import json, os
import shutil
from webserver import app, available_tournaments, request, jsonify, NovaGamesTeamsBannerGen, MCFTeamsBannerGen, output_folder
import io
import hashlib

@app.route("/banner_gen", methods=["POST"])
def banner_gen():
    if request.remote_addr == "127.0.0.1":
        data = request.get_json(force=True)

        if data["tournament"] in available_tournaments:
            if data["tournament"] == "NovaGames":
                if "temp" in os.listdir("."):
                    shutil.rmtree("./temp")
                os.mkdir("./temp")

                path_to_json_file = "./temp/teams.json"

                with open(path_to_json_file, 'a') as file:
                    json.dump(data["teams"], file)

                # Hard coded 14 teams for now, since I'm lazy.
                nova_games = NovaGamesTeamsBannerGen(cli_args=["", path_to_json_file, None, data["team_count"], "", output_folder])

                count = 0
                locations = {}

                for banner in nova_games.create():
                    count += 1

                    # Get Bytes
                    img_byte_arr = io.BytesIO()
                    banner.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    readable_hash = hashlib.sha256(img_byte_arr).hexdigest()

                    nova_games.save(banner, f"{readable_hash}", "png")

                    locations[count] = readable_hash

                shutil.rmtree("./temp")

                return jsonify(
                    {
                        "success" : True,
                        "generated_images": locations
                    }
                )

        else:
            return jsonify({"success" : False})

    return jsonify({"success" : False})