from typing import List
from pydantic import BaseModel, Field


class ResearchResponse(BaseModel):

    topic: str = Field(
        description="Short topic/title for the user's question."
    )


    research_area: List[str] = Field(
        default_factory=list,
        description="2-5 broader research areas related to the topic."
    )


    category: str = Field(
        description="Research category."
    )


    difficulty: str = Field(
        description="Difficulty level."
    )


    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score."
    )


    answer: str = Field(
        description="Direct answer."
    )


    summary: str = Field(
        description="Executive summary."
    )


    why_it_matters: str = Field(
        description="Why this topic matters."
    )


    key_concepts: List[str] = Field(
        default_factory=list
    )


    technical_breakdown: List[str] = Field(
        default_factory=list
    )


    challenges: List[str] = Field(
        default_factory=list
    )


    research_directions: List[str] = Field(
        default_factory=list
    )


    experimental_setup: List[str] = Field(
        default_factory=list
    )


    evaluation_plan: List[str] = Field(
        default_factory=list
    )


    follow_up_questions: List[str] = Field(
        default_factory=list
    )


    bottom_line: str = Field(
        default="",
        description="Final conclusion of the research topic."
    )