# Import necessary libraries
import streamlit as st  # Streamlit for creating the web interface
from SimplerLLM.language.llm import LLM, LLMProvider  # LLM and LLMProvider for language model handling
from SimplerLLM.tools.generic_loader import load_content  # Function to load content from a URL

# Function to split content into chunks
def split_content(content, chunk_size):
    # Split the content into chunks of a specified size
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

# Function to load content from file
def load_file_content(file):
    return file.read().decode("utf-8")

# Function to calculate chunk size based on model
def calculate_chunk_size(max_tokens, prompt_tokens=1000):
    return max_tokens - prompt_tokens

# Set up the Streamlit app
st.title("Blog-Post & YouTube Video Key Takeaways Extractor")  # Title of the web app
st.write("""
This app extracts key takeaways from a Blog-Post or a YouTube video using an LLM model. 
Enter the Blog-Post or Video URL, upload a file, and click the button to get the key takeaways in German.
""")  # Description of the app

# Input for URL or file upload
url = st.text_input("Enter URL", "")  # Text input for the URL
uploaded_file = st.file_uploader("Or upload a file", type=["txt", "md"])  # File uploader for text files

# Model selection
model_option = st.selectbox("Choose a GPT model", ["gpt-3.5-turbo", "gpt-4 (8k context)", "gpt-4 (32k context)"])

# Define maximum tokens based on selected model
model_token_limits = {
    "gpt-3.5-turbo": 4096,
    "gpt-4 (8k context)": 8192,
    "gpt-4 (32k context)": 32768
}

# Get the maximum token limit for the selected model
max_tokens = model_token_limits[model_option]

# Calculate recommended chunk size
chunk_size = calculate_chunk_size(max_tokens)

# API Key input
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Prompt options
prompt_option = st.selectbox(
    "Choose the type of prompt",
    ["Key Takeaways", "Instagram Post", "Student Notes", "Custom"]
)

# Default prompts
prompts = {
    "Key Takeaways": """
    I want you to only answer in German. 
    Please extract key takeaways of the Content. 
    Each key takeaway should be a list item, of the following format:
    "- [relevant emoji] [takeaway]"
    Keep emoji unique to each takeaway item. 
    Please try to use different emojis for each takeaway. Do not render brackets.
    Content: {content}""",
    
    "Instagram Post": """
    I want you to only answer in German.
    Please create an Instagram post from the content.
    Include a catchy headline and relevant hashtags.
    Content: {content}""",
    
    "Student Notes": """
    I want you to only answer in German.
    Please summarize the content as if you were taking notes for a class.
    Keep it concise and informative.
    Content: {content}"""
}

# Custom prompt input if selected
if prompt_option == "Custom":
    user_prompt = st.text_area("Enter your custom prompt")
else:
    user_prompt = prompts[prompt_option]

# Button to generate key takeaways
if st.button("Generate Output"):
    if (url or uploaded_file) and api_key:  # Check if URL or file is provided and API key is entered
        with st.spinner("Loading content and generating summary..."):
            if url:
                # Load content from the provided URL
                content = load_content(url).content
            elif uploaded_file:
                # Load content from the uploaded file
                content = load_file_content(uploaded_file)

            # Split content into manageable chunks
            chunks = split_content(content, chunk_size)

            # Set the API key for the LLM instance
            LLM.api_key = api_key

            # Initialize the LLM instance with OpenAI provider and specific model
            llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name=model_option)

            # Initialize an empty list to store results from each chunk
            all_key_takeaways = []

            # Process each chunk individually
            for chunk in chunks:
                # Replace placeholder with actual content in the user-defined prompt
                formatted_prompt = user_prompt.format(content=chunk)
                
                # Generate the summary using the LLM instance
                generated_text = llm_instance.generate_response(prompt=formatted_prompt)
                
                # Append the result to the list of all key takeaways
                all_key_takeaways.append(generated_text)
            
            # Combine all key takeaways into a single string
            combined_key_takeaways = "\n".join(all_key_takeaways)
            
            # Display the generated key takeaways
            st.subheader("Output:")
            st.write(combined_key_takeaways)
            
            # Add a copy button for the output
            st.button("Copy to Clipboard", on_click=lambda: st.write(st.code(combined_key_takeaways, language='markdown')))
            # Option to download the output as a file
            st.download_button("Download as TXT", combined_key_takeaways, file_name="output.txt")
    else:
        st.error("Please enter a valid URL or upload a file and provide your OpenAI API key.")  # Display an error if neither URL nor file is provided and API key is not entered
