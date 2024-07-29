import streamlit as st
from PIL import Image
import google.generativeai as genai
import sqlite3
from datetime import datetime

# Configure API key for Gemini
genai.configure(api_key="AIzaSyBC8QHmbUHNWDhu4dC7v5bppEySFemctTM")

# Set up the database connection and cursor
conn = sqlite3.connect('gemini_items.db')
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_prompt TEXT,
        response_text TEXT,
        timestamp TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        response_id INTEGER,
        item_text TEXT,
        FOREIGN KEY (response_id) REFERENCES responses (id)
    )
''')
conn.commit()

# Function to load OpenAI model and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-001')
    response = model.generate_content([input, image, prompt] if image else [input, prompt])
    return response.text

# Function to store response in the database
def store_response(input_prompt, response_text):
    timestamp = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO responses (input_prompt, response_text, timestamp)
        VALUES (?, ?, ?)
    ''', (input_prompt, response_text, timestamp))
    response_id = cursor.lastrowid  # Get the ID of the inserted response
    conn.commit()
    return response_id

# Function to parse items from response text
def parse_items(response_text):
    items = []
    lines = response_text.split('\n')
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() and line[1] == '.' or line.startswith("- ") or line.startswith("* ")):
            item_text = line.split(' ', 1)[1] if ' ' in line else line
            items.append(item_text)
    return items

# Function to store items in the database
def store_items(response_id, items):
    for item in items:
        cursor.execute('''
            INSERT INTO items (response_id, item_text)
            VALUES (?, ?)
        ''', (response_id, item))
    conn.commit()

# Function to clear all records from the tables
def clear_database():
    cursor.execute('DELETE FROM responses')
    cursor.execute('DELETE FROM items')
    conn.commit()

# Define the input prompt template
input_prompt_template = """
You want to create the item shown in the image or mentioned in the text. List down all the required items you will need to create that item.
List all those items in the below format
    1. Item 1
    2. Item 2
    3. Item 3
    and so on
At last also list down all the required tools to make it
Note that dont give any extra details just give names of all the possible items and dont group items
"""

# Initialize Streamlit app
st.set_page_config(page_title="MakeIt")
st.image("https://zeevector.com/wp-content/uploads/Walmart-Logo-PNG@.png")

st.markdown("<h1 style='text-align: center; color: white;'>MakeIt</h1>", unsafe_allow_html=True)


input_prompt = st.text_input("Tell us what you want to make", key="input")
uploaded_file = st.file_uploader("Image of what you want to make", type=["jpg", "jpeg", "png"])
image = Image.open(uploaded_file) if uploaded_file else None

if image:
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("How to  make")

# If the submit button is clicked
if submit and input_prompt:
    # Clear the database before storing new data
    clear_database()
    
    # Get the response from the Gemini model
    response_text = get_gemini_response(input_prompt, image, input_prompt_template)
    st.subheader("You will need: ")
    st.write(response_text)
    
    # Store the response and get the response ID
    response_id = store_response(input_prompt, response_text)
    
    # Parse items from the response text and store them
    items = parse_items(response_text)
    store_items(response_id, items)

# Close the database connection when the script ends
conn.close()






    
