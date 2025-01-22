import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import qrcode

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


def create_certificate(name, roll_no, college_name, output_path, template, font_details):
    template = Image.open(template)
    draw = ImageDraw.Draw(template)

    name_font = ImageFont.truetype(font_details['name_font_style'], size=font_details['name_font_size'])
    college_font = ImageFont.truetype(font_details['college_font_style'], size=font_details['college_font_size'])

    name_position = font_details['name_position']
    college_position = font_details['college_position']

    draw.text(name_position, name, font=name_font, fill="black", anchor="mm")
    draw.text(college_position, college_name, font=college_font, fill="black", anchor="mm")

    qr_data = f"Name: {name}\nRoll No: {roll_no}\nCollege: {college_name}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill="black", back_color="white")
    qr_img = qr_img.resize((150, 150))

    qr_position = (template.width - qr_img.width - 60, template.height - qr_img.height - 70)
    template.paste(qr_img, qr_position)

    os.makedirs("certificates", exist_ok=True)
    template.save(output_path)


def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            msg.attach(part)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True

    except Exception as e:
        print(f"Failed to send email to {recipient_email}. Error: {e}")
        return False


def process_csv_and_generate_certificates(csv_file, template, font_details, sender_email, sender_password):
    data = pd.read_csv(csv_file)
    subject = "Certificate of Participation in GENESIZ's 2K25 from the Department of AI at Kongu Engineering College"
    success_count = 0

    for index, row in data.iterrows():
        roll_no = row['Roll_No']
        name = row['Name']
        college_name = row['College Name']
        email = row['Email']

        body = f"Dear {name},\n\nPlease find attached your certificate of achievement.\nIf any changes are needed, contact us!!! \n\nBest Regards,\nAI Association,\naiassocationaia@gmail.com"
        certificate_path = os.path.join("certificates", f"{roll_no}_{name}.png")

        create_certificate(name, roll_no, college_name, certificate_path, template, font_details)

        if send_email(sender_email, sender_password, email, subject, body, certificate_path):
            success_count += 1

    return success_count


st.title("Certificate Generator with QR Code")
st.write("Upload your CSV file and certificate template. Configure font details and email settings.")

st.sidebar.header("Email Settings")
sender_email = st.sidebar.text_input("Sender Email", value="", help="Enter the sender email address.")
sender_password = st.sidebar.text_input("App Password", value="", type="password", help="Enter the sender app password.")

st.sidebar.header("Font Details")
name_font_style = st.sidebar.text_input("Name Font Style", value="arial.ttf")
name_font_size = st.sidebar.number_input("Name Font Size", value=50, step=1)
name_position_x = st.sidebar.number_input("Name Position X", value=1400, step=10)
name_position_y = st.sidebar.number_input("Name Position Y", value=630, step=10)

college_font_style = st.sidebar.text_input("College Font Style", value="arial.ttf")
college_font_size = st.sidebar.number_input("College Font Size", value=50, step=1)
college_position_x = st.sidebar.number_input("College Position X", value=1000, step=10)
college_position_y = st.sidebar.number_input("College Position Y", value=730, step=10)

csv_file = st.file_uploader("Upload CSV", type=["csv"])
template_file = st.file_uploader("Upload Certificate Template", type=["png", "jpg", "jpeg"])

if st.button("Generate Certificates"):
    if csv_file and template_file and sender_email and sender_password:
        font_details = {
            'name_font_style': name_font_style,
            'name_font_size': name_font_size,
            'name_position': (name_position_x, name_position_y),
            'college_font_style': college_font_style,
            'college_font_size': college_font_size,
            'college_position': (college_position_x, college_position_y)
        }
        success_count = process_csv_and_generate_certificates(csv_file, template_file, font_details, sender_email, sender_password)
        st.success(f"Successfully sent {success_count} certificates!")
    else:
        st.error("Please fill all required fields and upload the necessary files.")
