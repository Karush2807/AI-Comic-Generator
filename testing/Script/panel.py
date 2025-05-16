import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
groq_api_key = os.getenv("GROQ_API_KEY")

prompt = ChatPromptTemplate(
    [
        ("system",
        "You are a comic script generator. "
        "Generate 6 comic panels based on the story. For each panel, only include:\n"
        "- Panel Number\n"
        "- Scene Description (setting, mood only — NO character appearances)\n"
        "- Scene Explanation (explain like a narrator, what is happening in that scene)\n"
        "- Characters Involved (just names and roles like 'Aria (female colored Pixar like style)', 'Iris (drone colored Pixar like style)'. Remember to add this 'colored Pixar like style'.)\n"
        "- Dialogues (Speaker: Line)"
        ),
        ("user",
        "Story:\n{story}\n\n"
        "Generate exactly 6 panels. Keep descriptions concise and focused on the environment."
        )
    ]
)



llm = ChatGroq(model="Llama-3.3-70b-Versatile", groq_api_key=groq_api_key)

output_parser = StrOutputParser()

chain = prompt|llm|output_parser

story = input("Enter your story: ")

if story.strip():
    result = chain.invoke({"story":story})
    with open("comic_script.txt", "w") as file:
        file.write(result)
else:
    print("Please enter a valid story")