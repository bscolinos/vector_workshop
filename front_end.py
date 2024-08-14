import gradio as gr
import requests

def query_api(query, limit=5, temperature=0.1):
    """ Sends a request to the FastAPI backend and returns the response """
    url = 'http://localhost:8000/rag'
    response = requests.post(url, json={
        'query': query,
        'limit': limit,
        'temperature': temperature
    })
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Error: {response.status_code}, Message: {response.text}"

# Define the interface components
with gr.Blocks() as app:
    with gr.Row():
        query_box = gr.Textbox(label="Enter your query")
        limit_slider = gr.Slider(minimum=1, maximum=15, value=5, label="Limit")
        temp_slider = gr.Slider(minimum=0.0, maximum=1.0, step=0.1, value=0.1, label="Temperature")

    submit_btn = gr.Button("Submit")
    output_area = gr.Textbox(label="API Response", lines=20)


    submit_btn.click(
        fn=query_api,
        inputs=[query_box, limit_slider, temp_slider],
        outputs=output_area
    )

app.launch()