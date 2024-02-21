
import gradio as gr
from gradio_mindbox import Mindbox


example = Mindbox().example_inputs()

demo = gr.Interface(
    lambda x:x,
    gr.Textbox(
        label="主题输入"
    ),  # interactive version of your component
    Mindbox(label="思维导图"),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)


if __name__ == "__main__":
    demo.launch()
