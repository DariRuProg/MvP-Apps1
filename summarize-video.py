from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.generic_loader import load_content


llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo-1106")

url = "https://youtu.be/MOyl58VF2ak?si=T4eN18oqZLk0BeYW"

content = load_content(url).content

youtube_to_points_summary = f"""I want you to only answer in German. 
Please extract key takeaways of the Content. 
Each key takeaway should be a list item, of the following format:
"- [relevant emoji] [takeaway]"
Keep emoji unique to each takeaway item. 
Please try to use different emojis for each takeaway. Do not render brackets.
Content: {content}"""

generated_text = llm_instance.generate_response(prompt=youtube_to_points_summary)

print(generated_text)