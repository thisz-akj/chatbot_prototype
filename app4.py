from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Initialize model and embeddings
llm = ChatGoogleGenerativeAI(model="gemini-pro")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load and split PDF into multiple pages
loader = PyPDFLoader("item_list.pdf")
pages = loader.load_and_split()

# Initialize VectorDB and Retriever
vectordb = Chroma.from_documents(pages, embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 2})

# Define retrieval chain
template = """
You are a helpful AI assistant.
Your work is to give the link of input.
In the PDF format is 
input1**input1_link**
input2**input2_link**
and so on
input: {input}
Context: {context}
Please provide only the link associated with the input:
answer:
"""
prompt = PromptTemplate.from_template(template)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

def get_link_from_db(item_name):
    try:
        response = retrieval_chain.invoke({"input": item_name})
        link = response.get("answer", "#")
        return link
    except Exception as e:
        return f"An error occurred: {e}"



# Ensure your Streamlit app has access to the necessary functions and setup
# ...

# Initialize Streamlit app
st.set_page_config(page_title="MakeIt")
st.markdown("<h1 style='text-align: center; color: white;'>MakeIt</h1>", unsafe_allow_html=True)

input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

input_prompt = """
You are a masterchef who wants to create a item shown in the image or mentioned in the text. List down all the required items you will need to create that item.
List all those items in the following format and describe the process for making the product using those items:
    1. Item 1
    2. Item 2
    3. Item 3
    and so on.
At last, also list down all the required tools to make it.
Make sure to only give items only no extra text and don't group similar items.
Dont seperate items and tools list them without any extra heading
Never give extra information or comments just show items name only. It is very important to just show only items names.
And  also avoid using random sentences like "your favourite","as per your choice".
Give only top priority requirements.
 
 
"""


# Initialize the Google Generative AI model
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-001')
    try:
        if input_text and image:
            response = model.generate_content([input_text, image, prompt])
        elif input_text:
            response = model.generate_content([input_text, prompt])
        elif image:
            response = model.generate_content([image, prompt])
        else:
            response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"


if submit:
    response = get_gemini_response(input_text, image, input_prompt)
    st.subheader("Requirements:")

    # Assume response is a list of items in text format
    items_list = response.strip().split('\n')
    for item in items_list:
        item_name = item.strip().split('.', 1)[-1].strip()  # Extract the item name
        if item_name:
            # Retrieve the associated link from the database
            link = get_link_from_db(item_name)
            
            # Debug print
            #st.write(f"Link for {item_name}: {link}")

            # Display the item with a "Buy" button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(item_name)
            with col2:
                # Use markdown to create a clickable link styled as a button
                st.markdown(
                    f'<a href="{link}" target="_blank" class="buy-button">Buy</a>',
                    unsafe_allow_html=True
                )

# Add some CSS to style the "Buy" button
st.markdown("""
    <style>
        .buy-button {
            display: inline-block;
            padding: 8px 16px;
            font-size: 16px;
            font-weight: bold;
            color:#fff;
            background-color:#D0D0D0;
            border-radius: 4px;
            text-decoration: none;
        }
        .buy-button:hover {
            background-color:#A9A9A9;
        }
    </style>
""", unsafe_allow_html=True)
