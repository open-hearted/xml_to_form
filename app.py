from flask import Flask, request, render_template, send_file
from bs4 import BeautifulSoup
from pdf2image import convert_from_path
from PIL import ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_path = "static/output.png"
    name = ""
    if request.method == "POST":
        xml_file = request.files["xmlfile"]
        if xml_file:
            soup = BeautifulSoup(xml_file.read(), "xml")
            name = soup.find("xml001_B00160").text if soup.find("xml001_B00160") else ""
            image = convert_from_path("extractable.pdf", dpi=200, first_page=1, last_page=1)[0]
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("meiryo.ttc", 32)
            draw.text((1580, 120), name, fill="black", font=font)
            image.save(output_path)
    return render_template("index.html", name=name, image_path=output_path if name else None)
