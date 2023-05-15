import streamlit as st
import qrcode
from PIL import Image, ImageOps, ImageDraw
import io
import numpy as np
import imageio


def add_icon2(qr_img, icon_img):
    icon_size = int(qr_img.size[0] * 0.2)
    icon_img = icon_img.resize((icon_size, icon_size))
    x = int((qr_img.size[0] - icon_size) / 2)
    y = int((qr_img.size[1] - icon_size) / 2)
    qr_img.paste(icon_img, (x, y))
    return qr_img

def add_icon3(qr_img, icon_img):
    icon_size = int(qr_img.size[0] * 0.2)
    icon_img = icon_img.resize((icon_size, icon_size), Image.ANTIALIAS)  # Apply antialiasing
    x = int((qr_img.size[0] - icon_size) / 2)
    y = int((qr_img.size[1] - icon_size) / 2)
    qr_img.paste(icon_img, (x, y))
    return qr_img

def add_icon(qr_img, icon_img):
    icon_size = int(qr_img.size[0] * 0.2)
    icon_img = icon_img.resize((icon_size, icon_size), Image.ANTIALIAS)  # Apply antialiasing
    mask = Image.new("L", icon_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, icon_size, icon_size), fill=255)
    icon_img.putalpha(mask)
    x = int((qr_img.size[0] - icon_size) / 2)
    y = int((qr_img.size[1] - icon_size) / 2)
    qr_img.paste(icon_img, (x, y), icon_img)
    return qr_img


def generate_qr_code(url, fill_color, back_color, icon_path):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if icon_path:
        icon_img = Image.open(icon_path).convert("RGBA")
        qr_img = add_icon(qr_img, icon_img)
    return qr_img


st.title("URL to QR Code")
url = st.text_input("Enter a URL:")
fill_color = st.color_picker("Select a fill color", "#000000")
back_color = st.color_picker("Select a background color", "#FFFFFF")
icon_path = st.file_uploader("Select an icon image (optional)", type=["png", "jpg", "jpeg"])
if st.button("Generate QR Code"):
    if url:
        img = generate_qr_code(url, fill_color, back_color, icon_path)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        st.image(img_bytes, caption="QR Code", use_column_width=True)
    else:
        st.warning("Please enter a URL to generate the QR code.")
