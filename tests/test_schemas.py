from schemas import ResearchResponse


def test_research_response_schema():
    response = ResearchResponse(
        answer="RAG combines retrieval with generation.",
        summary="It retrieves relevant information before generation.",
        category="Concept Explanation",
        key_concepts=["RAG", "retrieval", "LLM"],
        difficulty="Intermediate",
        confidence=0.9,
        research_directions=["Compare retrieval strategies."],
        follow_up_questions=["How does RAG differ from fine-tuning?"],
    )

    assert response.confidence == 0.9
    assert response.category == "Concept Explanation"
