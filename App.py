from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load all environment variables from .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini 1.5 flash model and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Loading the genai model
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Mapping image to the bytes
def input_image_setup(upload_file):
    if upload_file is not None:
        # Read file into bytes
        bytes_data = upload_file.getvalue()
        image_parts = [{"mime_type": upload_file.type, "data": bytes_data}]
        return image_parts
    else:
        st.write("No file is uploaded")
        return "0"
        

# Initialize Streamlit app
st.set_page_config(page_title="Image Extractor")
st.header("Gemini Application")

input_prompt = """
You are an expert in understanding invoices. 
You will receive input images as invoices and 
you will have to answer questions based on the input image.
"""

upload_file = st.file_uploader('Choose an Image ...', type=["jpg", "jpeg", "png"])
image = ""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image")
input_text = st.text_input("Input prompt:", key="input")

submit = st.button("Tell Me about the image")

if submit:
    image_data = input_image_setup(upload_file)
    response = get_gemini_response(input_text, image_data, input_prompt)
    st.subheader("The Response is:")
    st.write(response)
    
# To run the above code use the command
# In command prompt >streamlit run App.py