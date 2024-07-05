# Import necessary libraries
import streamlit as st  # Streamlit for creating the web interface
from SimplerLLM.language.llm import LLM, LLMProvider  # LLM and LLMProvider for language model handling
from SimplerLLM.tools.generic_loader import load_content  # Function to load content from a URL

# Set up the Streamlit app
st.title("Blog-Post & YouTube Video Key Takeaways Extractor")  # Title of the web app
st.write("""
This app extracts key takeaways from a Blog-Post or a YouTube video using an LLM model. 
Enter the Blog-Post or Video URL, upload a file, and click the button to get the key takeaways in German.
""")  # Description of the app

# Input for URL or file upload
url = st.text_input("Enter URL", "")  # Text input for the URL
uploaded_file = st.file_uploader("Or upload a file", type=["txt", "md"])  # File uploader for text files

# Default prompt template
default_prompt = """
I want you to only answer in German. 
Please extract key takeaways of the Content. 
Each key takeaway should be a list item, of the following format:
"- [relevant emoji] [takeaway]"
Keep emoji unique to each takeaway item. 
Please try to use different emojis for each takeaway. Do not render brackets.
Content: {content}"""

# Prompt input for user to edit
user_prompt = st.text_area("Edit the Prompt as needed", default_prompt)

# Function to load content from file
def load_file_content(file):
    return file.read().decode("utf-8")

# Button to generate key takeaways
if st.button("Generate Key Takeaways"):
    if url or uploaded_file:  # Check if URL or file is provided
        with st.spinner("Loading content and generating summary..."):
            if url:
                # Load content from the provided URL
                content = load_content(url).content
            elif uploaded_file:
                # Load content from the uploaded file
                content = load_file_content(uploaded_file)

            # Initialize the LLM instance with OpenAI provider and specific model
            llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo-1106")

            # Replace placeholder with actual content in the user-defined prompt
            formatted_prompt = user_prompt.format(content=content)
            
            # Generate the summary using the LLM instance
            generated_text = llm_instance.generate_response(prompt=formatted_prompt)
            
            # Display the generated key takeaways
            st.subheader("Key Takeaways:")
            st.write(generated_text)
            
            # Add a copy button for the output
            st.button("Copy to Clipboard", on_click=lambda: st.write(st.code(generated_text, language='markdown')))
            # Option to download the output as a file
            st.download_button("Download as TXT", generated_text, file_name="key_takeaways.txt")
    else:
        st.error("Please enter a valid URL or upload a file.")  # Display an error if neither URL nor file is provided
