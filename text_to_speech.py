from dotenv import load_dotenv
import requests
from pypdf import PdfReader
import boto3
import os
import tkinter as tk
from tkinter import filedialog

# load env variables
load_dotenv()
aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key_id = os.environ['AWS_SECRET_ACCESS_KEY']


# file dialog for pdf file
def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()  # Open the file dialog
    return file_path


# initialize polly
polly_client = boto3.Session(
    aws_access_key_id=aws_key_id,
    aws_secret_access_key=aws_secret_key_id,
    region_name='us-east-2'
).client('polly')


def translate(input_text):
    return polly_client.synthesize_speech(
        Text = input_text,
        OutputFormat = 'mp3',
        VoiceId = 'Joanna'
    )

file_path = open_file_dialog()
reader = PdfReader(file_path)
# print(len(reader.pages))
text=''
for page in reader.pages:
    text += page.extract_text()

# page1 = reader.pages[1]
# text = page1.extract_text()
# print(text)
text = text.split('References')[0]
print(text)



response = translate(text)


with open('example_pdfs/speech.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())

