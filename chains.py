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


def _text(message) -> str:
    """Convert AIMessage to plain text."""
    return getattr(message, "content", message)


def _keyword_match(*keywords):
    lowered_keywords = tuple(k.lower() for k in keywords)

    def predicate(question: str) -> bool:
        q = question.lower()
        return any(keyword in q for keyword in lowered_keywords)

    return predicate


def _prompt_chain(template: str):
    prompt = PromptTemplate(
        input_variables=["question"],
        template=template,
    )
    return prompt | llm | RunnableLambda(_text)


def build_branch():
    """
    Select one specialized research pipeline.
    Only one specialist draft is generated.
    """

    research_gap = _prompt_chain(RESEARCH_GAP_PROMPT)
    methodology = _prompt_chain(METHODOLOGY_PROMPT)
    planning = _prompt_chain(PLANNING_PROMPT)
    concept = _prompt_chain(CONCEPT_PROMPT)
    default = _prompt_chain(DEFAULT_PROMPT)

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


def build_structured_pipeline():
    """
    Convert specialist draft into a richer structured research report.
    """

    structured_llm = llm.with_structured_output(ResearchResponse)

    prompt = PromptTemplate(
        input_variables=["draft"],
        template="""
You are ResearchX, a structured AI/ML research assistant.

You will receive a specialist draft. Convert it into a high-quality structured research report.

Return all fields required by the schema.

Guidelines:

1. topic
- Give a short, specific topic name.

2. research_area
- Return 2 to 5 broader research areas.

3. category
- Choose the best fitting category from:
  - Concept Explanation
  - Research Gap Exploration
  - Research Methodology
  - Research Planning
  - Paper/Topic Analysis

4. difficulty
- Choose one: Beginner, Intermediate, Advanced

5. confidence
- Return a number between 0 and 1.

6. answer
- Give a clear and direct answer.
- Make it readable and well-structured.
- Use short paragraphs or bullets where useful.

7. summary
- Give a compact 2-4 sentence executive summary.

8. why_it_matters
- Explain why this topic is important in research or real-world systems.

9. key_concepts
- Return 5 to 10 concise key concepts.

10. technical_breakdown
- Return a list of important technical points or system components.
- Each item should be self-contained and meaningful.

11. challenges
- Return practical limitations, risks, or open technical issues.

12. research_directions
- Return realistic future research directions.
- Avoid exaggerated novelty claims.

13. experimental_setup
- Suggest useful datasets, baselines, setup ideas, or methodology steps.

14. evaluation_plan
- Suggest useful evaluation metrics or analysis criteria.

15. follow_up_questions
- Return useful next-step research questions.

Important rules:
- Be accurate.
- Do not invent papers, datasets, results, or citations.
- If a dataset or benchmark is mentioned, only include widely known examples when appropriate.
- Write for a student or early-stage researcher.
- Make the response practical, structured, and meaningful.

SPECIALIST DRAFT:
{draft}
"""
    )

    return prompt | structured_llm