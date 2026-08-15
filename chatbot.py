from langchain_core.runnables import RunnableLambda, RunnableParallel

from chains import build_branch, build_parallel_pipeline, build_structured_pipeline
from schemas import ResearchResponse


class ResearchX:
    """
    Main orchestration layer.

    Flow:
        user query
            -> RunnableBranch
            -> RunnableParallel
            -> Pydantic structured output
    """

    def __init__(self):
        self.branch = build_branch()
        self.parallel = build_parallel_pipeline()
        self.structured = build_structured_pipeline()

        # RunnableLambda lets us connect the selected branch to the
        # parallel stage without hiding the required Runnable primitives.
        self.workflow = (
            self.branch
            | RunnableLambda(lambda draft: draft)
            | self.parallel
            | self.structured
        )

    def ask(self, question: str) -> ResearchResponse:
        question = question.strip()
        if not question:
            raise ValueError("Question cannot be empty.")

        return self.workflow.invoke(question)
