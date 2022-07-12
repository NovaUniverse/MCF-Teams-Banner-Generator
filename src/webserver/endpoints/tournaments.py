from webserver import app, available_tournaments, request, jsonify

@app.route("/tournaments", methods=["GET"])
def tournaments():
    if request.remote_addr == "127.0.0.1":
        return jsonify(available_tournaments)