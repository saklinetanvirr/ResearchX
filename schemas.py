from typing import Literal

from pydantic import BaseModel, Field


class ResearchResponse(BaseModel):
    """Validated response schema displayed by the Streamlit application."""

    answer: str = Field(
        description="The main answer to the user's research question."
    )
    summary: str = Field(
        description="A concise summary of the answer."
    )
    category: Literal[
        "Concept Explanation",
        "Research Gap",
        "Research Methodology",
        "Research Planning",
        "General Research",
    ] = Field(
        description="The research-question category."
    )
    key_concepts: list[str] = Field(
        description="Important concepts extracted from the response."
    )
    difficulty: Literal[
        "Beginner",
        "Intermediate",
        "Advanced",
    ] = Field(
        description="Estimated difficulty for understanding the topic."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Model confidence from 0.0 to 1.0."
    )
    research_directions: list[str] = Field(
        description="Potential research directions or next steps."
    )
    follow_up_questions: list[str] = Field(
        description="Useful follow-up questions for the researcher."
    )
