import json

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda

from config import llm

from prompts import (
    CONCEPT_PROMPT,
    DEFAULT_PROMPT,
    METHODOLOGY_PROMPT,
    PLANNING_PROMPT,
    RESEARCH_GAP_PROMPT,
)

from schemas import ResearchResponse



# -----------------------------
# Helpers
# -----------------------------

def _text(message) -> str:
    return getattr(message, "content", message)



def _keyword_match(*keywords):

    lowered_keywords = tuple(
        k.lower()
        for k in keywords
    )


    def predicate(question: str):

        q = question.lower()

        return any(
            keyword in q
            for keyword in lowered_keywords
        )


    return predicate



def _prompt_chain(template):

    prompt = PromptTemplate(
        input_variables=[
            "question"
        ],
        template=template,
    )


    return (
        prompt
        |
        llm
        |
        RunnableLambda(_text)
    )



# -----------------------------
# Research Router
# -----------------------------

def build_branch():

    research_gap = _prompt_chain(
        RESEARCH_GAP_PROMPT
    )

    methodology = _prompt_chain(
        METHODOLOGY_PROMPT
    )

    planning = _prompt_chain(
        PLANNING_PROMPT
    )

    concept = _prompt_chain(
        CONCEPT_PROMPT
    )

    default = _prompt_chain(
        DEFAULT_PROMPT
    )


    return RunnableBranch(

        (
            _keyword_match(
                "research gap",
                "research gaps",
                "novelty",
                "underexplored",
                "open problem",
                "unexplored",
            ),
            research_gap,
        ),


        (
            _keyword_match(
                "methodology",
                "method",
                "evaluate",
                "evaluation",
                "experiment",
                "metric",
                "benchmark",
            ),
            methodology,
        ),


        (
            _keyword_match(
                "research plan",
                "research roadmap",
                "how should i research",
                "how can i research",
                "research design",
                "proposal",
            ),
            planning,
        ),


        (
            _keyword_match(
                "what is",
                "explain",
                "difference between",
                "compare",
                "how does",
                "define",
            ),
            concept,
        ),


        default,

    )



# -----------------------------
# JSON Parser
# -----------------------------

def parse_json_response(text):

    try:

        # remove markdown fences if model adds them

        cleaned = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


        data = json.loads(
            cleaned
        )


        return ResearchResponse(
            **data
        )


    except Exception as e:


        print(
            "JSON parsing failed:",
            e
        )


        return ResearchResponse(

            topic="Unknown",

            research_area=[],

            category="General",

            difficulty="Intermediate",

            confidence=0.5,

            answer=text,

            summary=text[:500],

            why_it_matters="",

            key_concepts=[],

            technical_breakdown=[],

            challenges=[],

            research_directions=[],

            experimental_setup=[],

            evaluation_plan=[],

            follow_up_questions=[],

            bottom_line=""

        )



# -----------------------------
# Structured Research Report
# -----------------------------

def build_structured_pipeline():


    prompt = PromptTemplate(

        input_variables=[
            "draft"
        ],


        template="""

You are ResearchX.

Convert the research draft below into a structured JSON research report.

Return ONLY valid JSON.

Do not use markdown.

JSON format:


{{
"topic": "",
"research_area": [],
"category": "",
"difficulty": "",
"confidence": 0.0,

"answer": "",

"summary": "",

"why_it_matters": "",

"key_concepts": [],

"technical_breakdown": [],

"challenges": [],

"research_directions": [],

"experimental_setup": [],

"evaluation_plan": [],

"follow_up_questions": [],

"bottom_line": ""
}}


Rules:

- Be accurate.
- Do not invent citations.
- Do not create fake papers.
- Do not claim unsupported results.
- Write for AI/ML students and researchers.
- Make every section meaningful.


Research Draft:

{draft}

"""

    )


    return (

        prompt

        |

        llm

        |

        RunnableLambda(_text)

        |

        RunnableLambda(
            parse_json_response
        )

    )