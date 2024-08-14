import gradio as gr
import requests
import uuid

os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-f1b48c81-f298-490b-b42c-50ec7943bfba"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-2f5b7e04-745b-4d06-ae9a-3b5cc11f9fb7"
os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com"

def query_api(query, limit=5, temperature=0.1):
    url = 'http://localhost:8000/rag'
    trace_id = str(uuid.uuid4())  # Generate a unique trace ID
    response = requests.post(url, json={
        'query': query,
        'limit': limit,
        'temperature': temperature
    }, headers={'X-Langfuse-Trace-Id': trace_id})
    
    if response.status_code == 200:
        return response.json()['response'], trace_id
    else:
        return f"Error: {response.status_code}, Message: {response.text}", None

def submit_feedback(trace_id, score, comment):
    url = 'http://localhost:8000/feedback'
    response = requests.post(url, json={
        'traceId': trace_id,
        'score': score,
        'comment': comment
    })
    if response.status_code == 200:
        return "Feedback submitted successfully"
    else:
        return f"Error submitting feedback: {response.status_code}"

with gr.Blocks() as app:
    with gr.Row():
        query_box = gr.Textbox(label="Enter your query")
        limit_slider = gr.Slider(minimum=1, maximum=15, value=5, label="Limit")
        temp_slider = gr.Slider(minimum=0.0, maximum=1.0, step=0.1, value=0.1, label="Temperature")

    submit_btn = gr.Button("Submit")
    output_area = gr.Textbox(label="API Response", lines=20)
    trace_id = gr.State()

    with gr.Row():
        feedback_score = gr.Slider(minimum=1, maximum=5, step=1, label="Rate the response (1-5)")
        feedback_comment = gr.Textbox(label="Additional comments (optional)")
    feedback_btn = gr.Button("Submit Feedback")
    feedback_output = gr.Textbox(label="Feedback Status")

    submit_btn.click(
        fn=query_api,
        inputs=[query_box, limit_slider, temp_slider],
        outputs=[output_area, trace_id]
    )

    feedback_btn.click(
        fn=submit_feedback,
        inputs=[trace_id, feedback_score, feedback_comment],
        outputs=feedback_output
    )

app.launch()