import gradio as gr
from chatbot import ResearchX
from config import APP_TITLE

pilot = None

def get_pilot():
    global pilot
    if pilot is None:
        pilot = ResearchX()
    return pilot


def bullet_list(items):
    return "\n".join(f"- {x}" for x in items) if items else "_Not available._"


def numbered_list(items):
    return "\n".join(f"{i+1}. {x}" for i, x in enumerate(items)) if items else "_Not available._"


def empty_outputs(answer=""):
    return (answer, "", "", "", "", "", "", "", "", "", "", "", "", "")


def ask_researchx(question):
    if not question.strip():
        yield empty_outputs("Please enter a research question.")
        return

    bot = get_pilot()
    answer = ""

    for token in bot.stream_answer(question):
        answer += token
        yield (answer, "", "", "", "", "", "", "", "", "", "", "", question, "")

    result = bot.analyze(question)

    profile = f"""# 🔬 Research Profile

## Topic
{result.topic}

## Research Area
{', '.join(result.research_area)}

## Category
{result.category}

## Difficulty
{result.difficulty}

## Confidence
{result.confidence:.0%}
"""

    yield (
        answer, profile, result.summary, result.why_it_matters,
        bullet_list(result.key_concepts),
        numbered_list(result.technical_breakdown),
        numbered_list(result.challenges),
        numbered_list(result.research_directions),
        numbered_list(result.experimental_setup),
        numbered_list(result.evaluation_plan),
        numbered_list(result.follow_up_questions),
        result.bottom_line, question, ""
    )


css = """
#title{text-align:center;font-size:42px;font-weight:700}
#subtitle{text-align:center;color:#666}
"""

examples = [["What is RAG?"],["What research gaps exist in RAG hallucination detection?"]]

with gr.Blocks(title=APP_TITLE) as demo:
    gr.Markdown(f"<div id='title'>⟡ {APP_TITLE}</div><div id='subtitle'>AI/ML research assistant</div>")

    question = gr.Textbox(label="Ask ResearchX", lines=3)
    with gr.Row():
        submit_btn = gr.Button("✨ Analyze", variant="primary")
        clear_btn = gr.Button("🗑️ Clear")

    gr.Examples(examples=examples, inputs=question)

    answer = gr.Markdown()
    profile = gr.Markdown()
    summary = gr.Markdown()
    why = gr.Markdown()
    concepts = gr.Markdown()
    technical = gr.Markdown()
    challenges = gr.Markdown()
    directions = gr.Markdown()
    experiment = gr.Markdown()
    evaluation = gr.Markdown()
    follow = gr.Markdown()
    bottom = gr.Markdown()
    hidden = gr.Textbox(visible=False)
    status = gr.Textbox(visible=False)

    outputs=[answer,profile,summary,why,concepts,technical,challenges,directions,experiment,evaluation,follow,bottom,hidden,status]

    submit_btn.click(ask_researchx, inputs=question, outputs=outputs)
    question.submit(ask_researchx, inputs=question, outputs=outputs)
    clear_btn.click(lambda: empty_outputs(), outputs=outputs)

demo.queue(max_size=20)

if __name__ == '__main__':
    demo.launch(css=css)
