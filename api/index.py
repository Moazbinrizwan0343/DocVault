from flask import Flask, render_template, jsonify, request
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

OFFICE_TYPES = {
    "CNIC": "NADRA office",
    "Passport": "Passport office",
    "B-Form": "NADRA office",
    "Driving License": "Driving License office",
    "Vehicle Card": "Excise office",
}


@app.route("/")
def home():
    return render_template("home.html")
    @app.route("/robots.txt")
def robots():
    return (
        "User-agent: *\n"
        "Allow: /\n\n"
        "Sitemap: https://doc-vault-gray.vercel.app/sitemap.xml\n",
        200,
        {"Content-Type": "text/plain"}
    )


@app.route("/sitemap.xml")
def sitemap():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        '<url>'
        '<loc>https://doc-vault-gray.vercel.app/</loc>'
        '</url>'
        '</urlset>',
        200,
        {"Content-Type": "application/xml"}
    )


@app.route("/vault")
def vault():
    return render_template("vault.html")


@app.route("/api/office-search")
def office_search():
    document_type = request.args.get("type", "")
    office = OFFICE_TYPES.get(document_type, "government office")

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:
        maps_url = (
            f"https://www.google.com/maps/search/"
            f"{office.replace(' ', '+')}/@{lat},{lon},13z"
        )
    else:
        maps_url = (
            f"https://www.google.com/maps/search/"
            f"{office.replace(' ', '+')}"
        )

    return jsonify({
        "office": office,
        "maps_url": maps_url
    })


@app.route("/api/documents", methods=["POST"])
def save_document():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "No document data received"
        }), 400

    return jsonify({
        "success": True,
        "document": data
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
