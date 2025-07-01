A smart, automated system to generate and distribute personalized certificates via email — ideal for workshops, webinars, and academic events.

✨ Features
Upload CSV file with participant details: Name, College Name, and Email

Upload custom certificate template (PNG or JPG)

Customize font style, size, and position for name and college

Automatically place participant info on the certificate

Send personalized certificates via email (SMTP)

Certificates saved locally in a certificates/ folder

Easy-to-use web interface built with Streamlit

🛠️ Built With
Python – Core scripting

Streamlit – UI framework

Pandas – CSV data handling

Pillow (PIL) – Certificate image editing

smtplib & email.mime – Email automation



📂 Required Inputs
CSV file with columns:

Name

College Name

Email

Certificate template image (.png or .jpg)

Font file (.ttf like times.ttf)

Sender email and App Password (Gmail)

🧪 Sample CSV Format
csv
Copy
Edit
Name,College Name,Email
John Doe,ABC College,john@example.com
Jane Smith,XYZ University,jane@example.com
🚀 How to Run the App
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/e-certificate-generator.git
cd e-certificate-generator
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Launch the app

bash
Copy
Edit
streamlit run app.py
📤 Email Sending Info
Uses Gmail SMTP server (smtp.gmail.com, port 465)

Requires an App Password if 2-Step Verification is enabled

Make sure SMTP access is allowed in your Gmail account

🧰 Project Structure
bash
Copy
Edit
📦 e-certificate-generator
 ┣ 📄 app.py                 # Streamlit main app
 ┣ 📁 certificates/          # Output folder for generated certificates
 ┣ 📄 requirements.txt       # Required Python packages
 ┗ 📄 README.md              # Project description
📌 Workshop Info
Event: Gen-AI with Cloud and AI Agent Implementation
Date: 15-Mar-2025
Organized by: AI Association, Kongu Engineering College
Contact: aiassociationaia@gmail.com

📈 Future Enhancements
QR code verification on certificates

Email delivery tracking

Dashboard for preview and admin control

Bulk certificate status monitoring




