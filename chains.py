from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel

from config import llm
from prompts import (
    CONCEPT_PROMPT,
    DEFAULT_PROMPT,
    METHODOLOGY_PROMPT,
    PLANNING_PROMPT,
    RESEARCH_GAP_PROMPT,
    STRUCTURED_OUTPUT_PROMPT,
)
from schemas import ResearchResponse


def _text(message) -> str:
    """Normalize an AIMessage/string into plain text."""
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


# RunnableBranch
def build_branch():
    """
    Select one specialized research pipeline.

    Branch priority:
      1. Research gap
      2. Methodology/evaluation
      3. Planning
      4. Concept/explanation
      5. General research assistant
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


# RunnableParallel
def build_parallel_pipeline():
    """
    Run multiple independent research analyses on the selected branch draft.

    Each branch receives the same selected draft and produces one component.
    """

    answer_prompt = PromptTemplate(
        input_variables=["draft"],
        template=(
            "You are a careful AI/ML research assistant.\n\n"
            "Use the following specialist draft to write the main answer.\n"
            "Be accurate, clear, and undergraduate-researcher friendly.\n"
            "Do not invent papers, datasets, citations, or experimental results.\n\n"
            "SPECIALIST DRAFT:\n{draft}\n"
        ),
    )

    summary_prompt = PromptTemplate(
        input_variables=["draft"],
        template=(
            "Summarize the following specialist research analysis in 2-4 sentences.\n"
            "Keep the key technical meaning and avoid unsupported claims.\n\n"
            "SPECIALIST DRAFT:\n{draft}\n"
        ),
    )

    concepts_prompt = PromptTemplate(
        input_variables=["draft"],
        template=(
            "Extract the most important AI/ML/research concepts from the specialist "
            "draft. Return a concise comma-separated list of concepts only.\n\n"
            "SPECIALIST DRAFT:\n{draft}\n"
        ),
    )

    directions_prompt = PromptTemplate(
        input_variables=["draft"],
        template=(
            "Based on the specialist draft, propose 3-5 realistic research directions "
            "or next steps for a student. Do not claim that a direction is novel unless "
            "the draft provides evidence. Return a numbered list.\n\n"
            "SPECIALIST DRAFT:\n{draft}\n"
        ),
    )

    questions_prompt = PromptTemplate(
        input_variables=["draft"],
        template=(
            "Generate 3 useful follow-up questions a student researcher could ask "
            "after reading the specialist draft. Return a numbered list.\n\n"
            "SPECIALIST DRAFT:\n{draft}\n"
        ),
    )

    return RunnableParallel(
        answer=answer_prompt | llm | RunnableLambda(_text),
        summary=summary_prompt | llm | RunnableLambda(_text),
        key_concepts=concepts_prompt | llm | RunnableLambda(_text),
        research_directions=directions_prompt | llm | RunnableLambda(_text),
        follow_up_questions=questions_prompt | llm | RunnableLambda(_text),
    )


# Pydantic structured output
def build_structured_pipeline():
    """
    Convert the parallel dictionary into a validated ResearchResponse.

    We use the model's structured-output capability so Pydantic validation is
    performed by LangChain instead of relying on a plain StrOutputParser.
    """
    structured_llm = llm.with_structured_output(ResearchResponse)

    prompt = PromptTemplate(
        input_variables=[
            "answer",
            "summary",
            "key_concepts",
            "research_directions",
            "follow_up_questions",
        ],
        template=STRUCTURED_OUTPUT_PROMPT,
    )

    return prompt | structured_llm