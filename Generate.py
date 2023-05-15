import streamlit as st
import qrcode
from PIL import Image, ImageOps, ImageDraw
import io
import numpy as np
import imageio
from streamlit.components.v1 import html


def hide_header():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


def show_sidebar():
    with st.sidebar:
        st.header("Welcome to the best QR Code Generator!")
        # Create slider for factor
        st.write("- no costs")
        st.write("- no redirects")
        st.write("- no data recording")
        st.write("- simple and efficient")


def bmac():
    button = "<script type=\"text/javascript\" src=\"https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js\" data-name=\"bmc-button\" data-slug=\"pylutions\" data-color=\"#62c07f\" data-emoji=\"\"  data-font=\"Poppins\" data-text=\"\" data-outline-color=\"#000000\" data-font-color=\"#000000\" data-coffee-color=\"#255D36\" ></script>"
    html(button, width=74, height=80)
    st.markdown(
        """
        <style>
            iframe[width="74"] {
                position: fixed;
                top: 5%;
                right: 0%;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def add_icon(qr_img, icon_img):
    icon_size = int(qr_img.size[0] * 0.2)
    icon_img = icon_img.resize((icon_size, icon_size), Image.ANTIALIAS)  # Apply antialiasing
    x = int((qr_img.size[0] - icon_size) / 2)
    y = int((qr_img.size[1] - icon_size) / 2)
    qr_img.paste(icon_img, (x, y), mask=icon_img)
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


if __name__ == "__main__":
    st.set_page_config(page_title="QR Generator", page_icon="icon.ico", layout="wide")
    hide_header()
    show_sidebar()
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
    bmac()