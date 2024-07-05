# Import necessary libraries
import streamlit as st  # Streamlit for creating the web interface
from SimplerLLM.language.llm import LLM, LLMProvider  # LLM and LLMProvider for language model handling
from SimplerLLM.tools.generic_loader import load_content  # Function to load content from a URL

# Set up the Streamlit app
st.title("Blog-Post & YouTube Video Key Takeaways Extractor")  # Title of the web app
st.write("""
This app extracts key takeaways from a Blog-Post or a YouTube video using an LLM model. 
Enter the Blog-Post or Video URL and click the button to get the key takeaways in German.
""")  # Description of the app

# Input for YouTube video URL
url = st.text_input("Enter URL", "")  # Text input for the URL

# Button to generate key takeaways
if st.button("Generate Key Takeaways"):
    if url:  # Check if the URL is provided
        # Display a loading message while processing
        with st.spinner("Loading content and generating summary..."):
            # Load content from the provided URL
            content = load_content(url).content
            
            # Initialize the LLM instance with OpenAI provider and specific model
            llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo-1106")
            
            # Create the prompt for generating the summary
            youtube_to_points_summary = f"""
            I want you to only answer in German. 
            Please extract key takeaways of the Content. 
            Each key takeaway should be a list item, of the following format:
            "- [relevant emoji] [takeaway]"
            Keep emoji unique to each takeaway item. 
            Please try to use different emojis for each takeaway. Do not render brackets.
            Content: {content}"""
            
            # Generate the summary using the LLM instance
            generated_text = llm_instance.generate_response(prompt=youtube_to_points_summary)
            
            # Display the generated key takeaways
            st.subheader("Key Takeaways:")
            st.write(generated_text)
    else:
        st.error("Please enter a valid URL.")  # Display an error if no URL is provided
