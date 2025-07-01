import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Function to load font
def load_font(font_path, font_size):
    return ImageFont.truetype(font_path, size=font_size)

# Function to load certificate template
def load_template(template_path):
    return Image.open(template_path)

# Function to position text dynamically
def get_text_position(draw, text, font, anchor_pos):
    bbox = draw.textbbox(anchor_pos, text, font=font)
    text_width = bbox[2] - bbox[0]
    adjusted_x = anchor_pos[0] - text_width // 2
    return adjusted_x, anchor_pos[1]

# Function to create certificate
def create_certificate(name, college_name, output_path, template_path, font_details):
    template = load_template(template_path)
    draw = ImageDraw.Draw(template)

    # Load fonts
    name_font = load_font(font_details['name_font_style'], font_details['name_font_size'])
    college_font = load_font(font_details['college_font_style'], font_details['college_font_size'])

    # Position text dynamically
    name_pos = get_text_position(draw, name, name_font, font_details['name_position'])
    college_pos = get_text_position(draw, college_name, college_font, font_details['college_position'])

    # Draw text on the certificate
    draw.text(name_pos, name, font=name_font, fill="black")
    draw.text(college_pos, college_name, font=college_font, fill="black")

    # Save certificate
    os.makedirs("certificates", exist_ok=True)
    template.save(output_path)

# Function to send email with certificate attachment
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
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}. Error: {e}")
        return False

# Function to process CSV and generate/send certificates
def process_csv_and_generate_certificates(csv_file, template_path, font_details, sender_email, sender_password):
    subject = "Your Certificate of Achievement"
    success_count = 0
    data = pd.read_csv(csv_file)

    for index, row in data.iterrows():
        name, college_name, email = row['Name'], row['College Name'], row['Email']

        # Updated email content
        body = f"""Dear {name},

Congratulations! You have successfully attended the Gen-AI with Cloud and AI Agent Implementation workshop
held on 15-Mar-2025 at Kongu Engineering College, Erode.

Please find attached your certificate of achievement.
If any changes are needed, contact us!!!

Best Regards,
AI Association
aiassociationaia@gmail.com
"""



        certificate_path = os.path.join("certificates", f"{name}.png")
        create_certificate(name, college_name, certificate_path, template_path, font_details)

        if send_email(sender_email, sender_password, email, subject, body, certificate_path):
            success_count += 1

    return success_count

# Streamlit UI
st.title("Certificate Generator")
st.sidebar.header("Email Settings")
sender_email = st.sidebar.text_input("Sender Email")
sender_password = st.sidebar.text_input("App Password", type="password")

st.sidebar.header("Font Details")
name_font_style = st.sidebar.text_input("Name Font Style", "times.ttf")  # Times New Roman
name_font_size = st.sidebar.number_input("Name Font Size", value=28, step=1)
name_position_x = st.sidebar.number_input("Name Position X", value=760, step=10)
name_position_y = st.sidebar.number_input("Name Position Y", value=410, step=10)

college_font_style = st.sidebar.text_input("College Font Style", "times.ttf")  # Times New Roman
college_font_size = st.sidebar.number_input("College Font Size", value=28, step=1)
college_position_x = st.sidebar.number_input("College Position X", value=560, step=10)
college_position_y = st.sidebar.number_input("College Position Y", value=460, step=10)

csv_file = st.file_uploader("Upload CSV", type=["csv"])
template_file = st.file_uploader("Upload Certificate Template", type=["png", "jpg", "jpeg"])

# Generate Certificates Button
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
        st.error("Please fill all fields and upload necessary files.")
