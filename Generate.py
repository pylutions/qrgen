import streamlit as st
import qrcode
from PIL import Image, ImageOps, ImageDraw
import io
import numpy as np
import imageio
from streamlit.components.v1 import html
import requests
from io import BytesIO
import pyperclip


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


def more():
    button_html = '''
        <div style="position: fixed; bottom: 20%; right: -1%;">
            <a href="https://pylutions.com/#products" target="_blank" style="display: inline-block; background-color: #62c07f; color: black; padding: 12px 48px; font-size: 16px; border-radius: 5px; text-decoration: none;">
                more...
            </a>
        </div>
    '''
    st.markdown(button_html, unsafe_allow_html=True)

def ga():
    st.markdown(
        """
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-JEXQZEME08"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
            
              gtag('config', 'G-JEXQZEME08');
            </script>
        """, unsafe_allow_html=True)



# Function to copy QR code to clipboard
def copy_qr_code(img_io):
    img_data = img_io.getvalue()
    pyperclip.copy(img_data)
    #st.success('QR Code copied to clipboard!')


def add_icon(qr_img, icon_img):
    icon_size = int(qr_img.size[0] * 0.2)
    icon_img = icon_img.resize((icon_size, icon_size), Image.ANTIALIAS)  # Apply antialiasing
    x = int((qr_img.size[0] - icon_size) / 2)
    y = int((qr_img.size[1] - icon_size) / 2)
    qr_img.paste(icon_img, (x, y), mask=icon_img)
    return qr_img


def generate_qr_code(url, fill_color, back_color, icon_path):
    qr = qrcode.QRCode(version=1, box_size=100, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color, scale=10)
    if icon_path:
        icon_img = Image.open(icon_path).convert("RGBA")
        qr_img = add_icon(qr_img, icon_img)
    return qr_img


def get_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


if __name__ == "__main__":
    st.set_page_config(page_title="QR Code Generator", page_icon="icon.ico", layout="wide")
    hide_header()
    ga()
    show_sidebar()
    st.title("URL to QR Code")
    url = st.text_input("Enter a URL:")
    col1, col2 = st.columns(2)
    fill_color = col1.color_picker("Select a fill color", "#000000")
    back_color = col2.color_picker("Select a background color", "#FFFFFF")
    col1, col2 = st.columns(2)

    # File uploader
    with col1:
        icon_path = st.file_uploader("Select an icon image (optional)", type=["png", "jpg", "jpeg"])

    # URL input
    with col2:
        img_url = st.text_input("Enter image URL (optional)")
        if img_url:
            if not img_url.endswith(('png', 'jpg', 'jpeg')):
                st.warning("Invalid file type. Please provide a URL to a PNG, JPG, or JPEG image.")
            else:
                try:
                    icon_path = get_image_from_url(img_url)
                except:
                    st.warning("Failed to fetch the image from the provided URL.")

    if st.button("Generate QR Code"):
        if url:
            img = generate_qr_code(url, fill_color, back_color, icon_path)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            #st.image(img_bytes, caption="QR Code", use_column_width=True)
            st.image(img_bytes, caption="QR Code")
            st.download_button('Download QR Code', img_bytes, file_name='qr_code.png', mime='image/png')

        else:
            st.warning("Please enter a URL to generate the QR code.")
    bmac()
    more()
