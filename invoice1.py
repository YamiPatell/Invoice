from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import pandas as pd
import google.generativeai as genai



os.getenv("API_KEY")
genai.configure(api_key=os.getenv("API_KEY"))


## Function to load OpenAI model and get respones
def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):

    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Gemini Image Demo")
st.header("Invoice Data Extractor")
input = st.text_area("Input Prompts (Enter multiple questions):", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image=""  
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

 
submit=st.button("Tell me about the image")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

## If ask button is clicked

if st.button("Submit"):
    # Assuming you have the necessary functions defined
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    # Display the response
    st.subheader("The Response is")
    st.write(response)

    # Save the response to an Excel file
    df = pd.DataFrame({"Input Prompt": [input], "Response": [response]})
    print("data")
    df.to_excel("responses.xlsx", index=False)
    st.success("Response saved to responses.xlsx")



