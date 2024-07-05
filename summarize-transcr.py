from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.generic_loader import load_content


llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo-1106")

url = "https://www.rad1.de/gazelle/"

content = load_content(url).content

Q_A_prompt = f"""In den folgenden Eingaben werde ich dir einen Text geben, den du für mich zusammenfassen sollst.

Erstelle eine kurze Zusammenfassung des Artikels in wenigen Sätzen.
Erstelle eine Q&A oder FAQ-Sektion mit möglichen Fragen und Antworten, basierend auf dem Artikel.
Die Anzahl der FAQs sollte zwischen 5 und 10 liegen, abhängig von der Länge des Artikels.
Die Sprache des Textes, den du erhältst, bestimmt die Sprache, in der du die Zusammenfassung und die Q&A/FAQ schreibst. Wenn der Text auf Deutsch ist, schreibe die Zusammenfassung und die Q&A/FAQ ebenfalls auf Deutsch.

Bei der Erstellung der Zusammenfassung und der Q&A/FAQ bitte ich dich, die folgenden Informationen zu berücksichtigen: Bei der Texterstellung sind zwei Faktoren entscheidend: "Perplexität" und "Burstiness". Perplexität misst die Komplexität eines Textes. Burstiness vergleicht die Variationen der Sätze. Menschen neigen dazu, mit großer Burstiness zu schreiben, also mit einigen längeren oder komplexen Sätzen neben kürzeren Sätzen. KI-Sätze tendieren dazu, gleichmäßiger zu sein. Daher benötige ich für den folgenden Inhalt, den ich dich bitten werde zu erstellen, eine gute Mischung aus Perplexität und Burstiness.

Hier sind die Parameter für die Zusammenfassung:

Text: {content}"""

generated_text = llm_instance.generate_response(prompt=Q_A_prompt)

print(generated_text)