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

# Default prompts for different tasks
default_prompts = {
    "key_takeaways": """
    I want you to only answer in {language}. 
    Please extract key takeaways of the Content. 
    Each key takeaway should be a list item, of the following format:
    "- [relevant emoji] [takeaway]"
    Keep emoji unique to each takeaway item. 
    Please try to use different emojis for each takeaway. Do not render brackets.
    Content: {content}""",

    "instagram_post": """
    Act as if you're a social media expert.
    I want you to create 5 different Instagram posts in {language} based on the Content. 
    The thread should be optimised for virality and contain 
    relevant hashtags and a catchy caption. Stop when you created exactly 5 Posts.
    Content: {content}""",

    "tweet_post": """
    Act as if you're a social media expert. 
    Give me a 10 tweet thread based on the follwing Content: {content}. 
    The thread should be optimised for virality and contain 
    hashtags and emoticons. Each tweet should not exceed 280 characters in length.""",

    "student_summary_notes": """
    I want you to create summary notes in {language} based on the Content. 
    Summarize the key points as if you were taking notes to learn from the content.
    Content: {content}"""
}

# Set up the Streamlit app
st.title("Content Analysis and Generation App")  # Title of the web app
st.write("""
This app analyzes content and generates different outputs using an LLM model. 
Enter the URL of the content or upload a file, select a task, language, and click the button to generate the output.
""")  # Description of the app

# API key input
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Check if API key is provided
if api_key:
    # Save the API key in the session state
    st.session_state["api_key"] = api_key
    
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

    # Language selection
    language_option = st.selectbox("Select language", ["German", "English", "French", "Spanish", "Italian", "Custom"])

    if language_option == "Custom":
        custom_language = st.text_input("Enter custom language", "")
        language = custom_language if custom_language else "Custom"
    else:
        language = language_option

    # Prompt selection
    prompt_option = st.selectbox("Select task", ["Key Takeaways", "Instagram Post", "Tweet Post", "Student Notes", "Custom Prompt"])

    if prompt_option == "Custom Prompt":
        custom_prompt = st.text_area("Enter your custom prompt", "")
        prompt = custom_prompt if custom_prompt else default_prompts["key_takeaways"]
    else:
        prompt = default_prompts[prompt_option.lower().replace(" ", "_")]

    # Replace language placeholder in prompt
    prompt = prompt.replace("{language}", language)

    # Button to generate output
    if st.button("Generate Output"):
        if url or uploaded_file:  # Check if URL or file is provided
            with st.spinner("Loading content and generating output..."):
                if url:
                    # Load content from the provided URL
                    content = load_content(url).content
                elif uploaded_file:
                    # Load content from the uploaded file
                    content = load_file_content(uploaded_file)

                # Split content into manageable chunks
                chunk_size = calculate_chunk_size(max_tokens)
                chunks = split_content(content, chunk_size)

                # Initialize the LLM instance with OpenAI provider and specific model
                llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name=model_option)
                
                # Set the API key for the LLM instance if needed
                llm_instance.api_key = api_key

                # Initialize an empty list to store results from each chunk
                all_outputs = []

                # Process each chunk individually
                for chunk in chunks:
                    # Replace placeholder with actual content in the user-defined prompt
                    formatted_prompt = prompt.format(content=chunk)
                    
                    # Generate the output using the LLM instance
                    generated_text = llm_instance.generate_response(prompt=formatted_prompt)
                    
                    # Append the result to the list of all outputs
                    all_outputs.append(generated_text)
                
                # Combine all outputs into a single string
                combined_output = "\n".join(all_outputs)
                
                # Display the generated output
                st.subheader("Generated Output:")
                st.write(combined_output)
                
                # Add a copy button for the output
                st.button("Copy to Clipboard", on_click=lambda: st.write(st.code(combined_output, language='markdown')))
                # Option to download the output as a file
                st.download_button("Download as TXT", combined_output, file_name="generated_output.txt")
        else:
            st.error("Please enter a valid URL or upload a file.")  # Display an error if neither URL nor file is provided
else:
    st.warning("Please enter your OpenAI API key to proceed.")
