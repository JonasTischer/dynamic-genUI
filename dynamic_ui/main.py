from fasthtml.common import *
from monsterui.all import *

from components import LoadingMessage, ChatInput, Footer
from handlers import handle_chat_send

# Enable ApexCharts support
hdrs = Theme.blue.headers(apex_charts=True)

# Create your app with the theme
app, rt = fast_app(hdrs=hdrs)


# The main screen
@app.get
def index():
    page = Div(cls="min-h-screen flex flex-col")(
        Div(cls="flex-1 container mx-auto p-4")(
            Div(cls="max-w-6xl mx-auto")(
                # Welcome message
                Div(cls="text-center mb-6")(
                    H2("Dynamic UI Chat Assistant", cls="text-2xl font-semibold text-gray-700 mb-2"),
                    P("Chat naturally with me - I'll respond with interactive UI components to help you better understand and work with information", cls="text-gray-500")
                ),

                # Chat interface
                Form(hx_post=send, hx_target="#chatlist", hx_swap="beforeend", hx_indicator="#loading")(
                    Div(cls="bg-white rounded-lg shadow-lg border")(
                        Div(id="chatlist", cls="chat-box h-[60vh] overflow-y-auto p-4"),

                        # Loading indicator (hidden by default)
                        Div(id="loading", cls="htmx-indicator")(
                            LoadingMessage()
                        ),

                        # Input area
                        Div(cls="border-t p-4")(
                            Div(cls="flex space-x-3")(
                                ChatInput(),
                                Button(
                                    Span("Send", cls="mr-2"),
                                    Loading((LoadingT.spinner, LoadingT.xs), htmx_indicator=True),
                                    cls="btn btn-primary",
                                    type="submit",
                                    id="send-btn",
                                    hx_disabled_elt="#send-btn",  # Disable the button during request
                                    hx_trigger="submit"
                                )
                            )
                        )
                    )
                )
            )
        ),
        Footer()
    )
    return Titled('🎨 Dynamic Generative UI Assistant', page)

# Handle the form submission
@app.post
def send(msg: str, messages: list[str] = None):
    return handle_chat_send(msg, messages)

serve(port=5001)