
import gradio as gr
from gradio_url_buttons import source_buttons

def add_source():
    return [{"link": "https://www.github.com", "hostname": "Github.com"}, {"link": "https://www.hkk.de", "hostname": "HKK.de"}]

with gr.Blocks() as demo:
    gr.Markdown("# Change the value (keep it JSON) and the front-end will update automatically.")
    source_buttons(value=[])
    buttons = source_buttons()
    click = gr.Button("Click me")
    source_buttons(value=[{"link": "https://www.google.com", "hostname": "Google.com"}, {"link": "https://www.hkk.de", "hostname": "HKK.de"}])

    click.click(add_source, inputs=[], outputs=[buttons])


if __name__ == "__main__":
    demo.launch()
