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
    # Fixed typo: 'fformat' to 'format'
    prompt = '''
    From the below news article, extract revenue and eps in JSON format containing the
    following keys: 'revenue_actual','revenue_expected','eps_actual','eps_expected'.
    Only return the valid JSON. No preamble.

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