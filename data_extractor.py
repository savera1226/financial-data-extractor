from typing import List, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load API key from .env file
load_dotenv()


# ═══════════════════════════════════════════════════════════════
# DATA SCHEMA (Strict Pydantic Validation)
# ═══════════════════════════════════════════════════════════════

class SegmentSplit(BaseModel):
    segment: str = Field(
        description="Name of the business segment or region (e.g. 'Enterprise Cloud', 'North America')"
    )
    revenue: str = Field(
        description="Revenue formatted as '$X.XB' for billions or '$X.XM' for millions. Never spell out 'billion'."
    )
    percentage: str = Field(
        description="ONLY use a percentage explicitly stated in the source text. If not stated, return 'N/A'. Do NOT calculate or infer percentages."
    )


class FinancialData(BaseModel):
    revenue_actual: str = Field(
        description="Actual reported revenue. Format: '$X.XB' (e.g. '$45.2B'). Return 'N/A' if absent."
    )
    revenue_expected: str = Field(
        description="Analyst-estimated revenue. Format: '$X.XB' (e.g. '$42.8B'). Return 'N/A' if absent."
    )
    eps_actual: str = Field(
        description="Actual reported EPS. Format: '$X.XX' (e.g. '$3.15'). Return 'N/A' if absent."
    )
    eps_expected: str = Field(
        description="Analyst-estimated EPS. Format: '$X.XX' (e.g. '$2.95'). Return 'N/A' if absent."
    )

    # 🎯 UPDATED: Extremely strict rule to force a pure float for mathematical operations
    revenue_yoy_growth: Optional[float] = Field(
        default=None,
        description="CRITICAL: Return ONLY a pure float number (e.g., 34.5). Do NOT include the '%' or '+' symbols. Return null if absent."
    )

    bifurcation: List[SegmentSplit] = Field(
        default=[],
        description="List of revenue segment breakdowns explicitly mentioned. Return an empty list [] if no breakdown is mentioned."
    )
    source_quote: str = Field(
        description="The complete verbatim sentence(s) from the text that contain the revenue and EPS figures. Do NOT truncate. Return 'N/A' if absent."
    )


# ═══════════════════════════════════════════════════════════════
# LLM SETUP
# ═══════════════════════════════════════════════════════════════
# Note: Using model="..." (not model_name) to ensure compatibility
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Bind strict Pydantic schema — LLM MUST conform to this structure
structured_llm = llm.with_structured_output(FinancialData)


# ═══════════════════════════════════════════════════════════════
# EXTRACTION FUNCTION
# ═══════════════════════════════════════════════════════════════
def extract(article_text: str) -> dict:
    """
    Extract structured financial metrics from raw text.
    Never raises an error — returns safe fallback dictionary on any failure.
    """
    prompt = """
    You are a senior financial analyst at a top-tier investment bank.
    Extract the exact financial metrics from the document below with absolute precision.

    CRITICAL RULES:
    1. NEVER hallucinate or invent numbers. Only extract what is explicitly written.
    2. Format all revenue values as '$X.XB' for billions (e.g. '$45.2B'). Never write 'billion'.
    3. Format all EPS values as '$X.XX' (e.g. '$3.15').
    4. For revenue_yoy_growth: Return ONLY the raw number (e.g., 34.5). No symbols.
    5. For bifurcation: Do NOT calculate or infer percentages — only use percentages directly stated.
    6. For source_quote: copy the full sentence(s) containing the revenue/EPS numbers verbatim.
    7. Return 'N/A' for any scalar field genuinely absent from the text.

    Document:
    =========
    {article}
    """

    pt = PromptTemplate.from_template(prompt)
    chain = pt | structured_llm

    # Graceful fallback — prevents app crashes
    try:
        result = chain.invoke({"article": article_text})
        result_dict = result.dict()

        # Normalize bifurcation: convert list of Pydantic objects -> list of plain dicts for Streamlit
        if result_dict.get("bifurcation"):
            result_dict["bifurcation"] = [
                {"segment": s["segment"], "revenue": s["revenue"], "percentage": s["percentage"]}
                for s in result_dict["bifurcation"]
            ]
        else:
            result_dict["bifurcation"] = []

        return result_dict

    except Exception as e:
        print(f"[Extractor Error] {type(e).__name__}: {e}")
        # Safe fallback dictionary if the LLM completely fails
        return {
            "revenue_actual": "N/A",
            "revenue_expected": "N/A",
            "eps_actual": "N/A",
            "eps_expected": "N/A",
            "revenue_yoy_growth": None,
            "bifurcation": [],
            "source_quote": "N/A",
        }
