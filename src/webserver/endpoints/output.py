from webserver import app, request, send_from_directory, output_folder, jsonify

@app.route("/output/<hash>", methods=["GET"])
def output(hash):
    if request.remote_addr == "127.0.0.1":
        if not hash == "":
            return send_from_directory(f".{output_folder}", f"{hash}.png")

        return jsonify({"success" : False})