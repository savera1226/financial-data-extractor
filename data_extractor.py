from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load your Groq API key from the .env file
load_dotenv()

# Connect to the 70B Cloud Model
llm = ChatGroq(model_name="llama-3.3-70b-versatile")


def extract(article_text):
    prompt = '''
        From the below news article, extract financial metrics in JSON format.
        Keys required: 
        'revenue_actual', 'revenue_expected', 
        'eps_actual', 'eps_expected', 
        'bifurcation' 

        IMPORTANT: For 'bifurcation', provide a clean, bulleted list of the revenue split 
        (e.g., "• Google Search: $63.1B | • YouTube: $11.4B"). 
        Do NOT include any HTML colors or markdown styling in the JSON value.

        Article
        ========
        {article}
        '''
    pt = PromptTemplate.from_template(prompt)

    # Move the parser UP so Python knows what it is before building the chain
    parser = JsonOutputParser()

    # Build the LangChain pipeline (LCEL)
    chain = pt | llm | parser

    # Execute the chain
    res = chain.invoke({"article": article_text})

    return res
