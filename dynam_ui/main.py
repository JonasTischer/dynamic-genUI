from fasthtml.common import *
from monsterui.all import *
from claudette import *
from datetime import datetime
from dotenv import load_dotenv
import re

load_dotenv()

# import os
# os.environ['ANTHROPIC_LOG'] = 'debug'

# Enable ApexCharts support
hdrs = Theme.blue.headers(apex_charts=True)

# Create your app with the theme
app, rt = fast_app(hdrs=hdrs)

model = models[1]

# Safe namespace for executing generated code
SAFE_NAMESPACE = {
    # Basic FastHTML components
    'Grid': Grid,
    'Button': Button,
    'Div': Div,
    'Select': Select,
    'Option': Option,
    'Input': Input,
    'Label': Label,
    'Span': Span,
    'P': P,
    'H1': H1,
    'H2': H2,
    'H3': H3,
    'H4': H4,
    'H5': H5,
    'H6': H6,
    'Form': Form,
    'A': A,
    'Img': Img,
    'Ul': Ul,
    'Li': Li,
    'Ol': Ol,
    'Strong': Strong,
    'Em': Em,
    'Br': Br,
    'Hr': Hr,
    'Table': Table,
    'Tr': Tr,
    'Td': Td,
    'Th': Th,
    'Thead': Thead,
    'Tbody': Tbody,
    # Chart components
    'ApexChart': ApexChart,
    # Loading components
    'Loading': Loading,
    'LoadingT': LoadingT,
    # Accordion components
    'Accordion': Accordion,
    'AccordionItem': AccordionItem,
    # Steps components
    'Steps': Steps,
    'LiStep': LiStep,
    'StepsT': StepsT,
    'StepT': StepT,
    # Icons & Images components
    'DiceBearAvatar': DiceBearAvatar,
    'PicSumImg': PicSumImg,
    'UkIcon': UkIcon,
    'UkIconLink': UkIconLink,
    # Allow cls parameter
    'cls': 'cls',
    # Safe Python built-ins
    'enumerate': enumerate,
    'range': range,
    'len': len,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'set': set,
    'min': min,
    'max': max,
    'sum': sum,
    'sorted': sorted,
    'reversed': reversed,
    'zip': zip,
    'any': any,
    'all': all,
}

def parse_and_execute_component(code_text):
    """Safely parse and execute the generated component code."""
    try:
        # Clean up the code text
        code_text = code_text.strip()

        # Remove markdown code blocks if present
        if code_text.startswith('```'):
            lines = code_text.split('\n')
            code_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else code_text

        # Remove any leading/trailing whitespace
        code_text = code_text.strip()

        print(f"Executing code: {code_text}")

        # Execute the code in our safe namespace
        result = eval(code_text, {"__builtins__": {}}, SAFE_NAMESPACE)
        return result
    except Exception as e:
        print(f"Error executing code: {e}")
        return Div(f"Error parsing component: {str(e)}", cls="alert alert-error")

# Define the visual information display function
def VisualDisplay(content_type: str, data: list[str], context: str):
    """Generate the best visual representation for the given information.

    content_type: The type of information (people, places, products, timeline, comparison, list, charts, etc.)
    data: The actual data points to display
    context: Additional context about what the user is asking for
    """
    print(f"Creating visual display for: {content_type}, data: {data}, context: {context}")

    cli = Client(model)
    prompt = f"""You are creating a visual information display for: {context}

Content Type: {content_type}
Data: {data}

Create a comprehensive, visually appealing FastHTML component that best presents this information. Choose the most appropriate layout:

For PEOPLE (presidents, celebrities, historical figures):
- Use Grid with cards showing name, title, key facts, and links
- Use DiceBearAvatar for profile pictures: DiceBearAvatar("Name", 80, 80)
- Include relevant details like dates, achievements, etc.

For PLACES (countries, cities, landmarks):
- Use cards with location info, key facts, population, etc.
- Use PicSumImg for placeholder images: PicSumImg(200, 150)
- Include links to maps or more information

For PRODUCTS/ITEMS (books, movies, products):
- Use cards with images, descriptions, ratings, links
- Use PicSumImg for placeholder product images

For TIMELINES/EVENTS:
- Use ordered lists or timeline layout with dates and descriptions
- Use UkIcon for timeline markers: UkIcon("calendar", 16, 16)

For TUTORIALS/PROCESSES/STEP-BY-STEP GUIDES:
- Use Steps with LiStep for sequential processes
- STEPS SYNTAX: Steps(LiStep("Step Name", cls=StepT.primary), LiStep("Next Step", cls=StepT.neutral), ...)
- Use StepT for colors: StepT.primary, StepT.success, StepT.neutral, StepT.info, StepT.warning, StepT.error
- Use StepsT.vertical for vertical layout: Steps(..., cls=StepsT.vertical)
- Add emojis/icons in data_content: LiStep("Step", cls=StepT.success, data_content="✅")

For COMPARISONS:
- Use tables or side-by-side cards
- Use UkIcon for pros/cons: UkIcon("check", 16, 16), UkIcon("x", 16, 16)

For FAQ/STRUCTURED INFO:
- Use Accordion with AccordionItem for collapsible sections
- ACCORDION SYNTAX: AccordionItem(title_with_icon, content...)
- To include icons in accordion titles, put them IN the title: AccordionItem(Div(UkIcon("help-circle", 16, 16), "Question text", cls="flex items-center gap-2"), content...)

For DATA/STATISTICS/CHARTS (numbers, trends, analytics):
- ALWAYS use ApexChart (not uk-chart, not chart, only ApexChart) for visualizing numerical data
- Available chart types: line, pie, bar, area, donut, scatter, etc.
- MANDATORY syntax: ApexChart(opts={{"chart": {{"type":"bar"}}, "series": [...], "xaxis": {...}}})

CRITICAL: When creating charts, you MUST use this exact syntax:
ApexChart(opts={{"chart": {{"type":"TYPE_HERE"}}, "series": [...], "xaxis": {...}}})

Available components: Grid, Button, Div, Select, Option, Input, Label, Span, P, H1, H2, H3, H4, H5, H6, Form, A, Img, Ul, Li, Ol, Strong, Em, Br, Hr, Table, Tr, Td, Th, Thead, Tbody, ApexChart, Loading, LoadingT, Accordion, AccordionItem, Steps, LiStep, StepsT, StepT, DiceBearAvatar, PicSumImg, UkIcon, UkIconLink

ACCORDION RULES:
- AccordionItem(title, content...) - NO icon parameter!
- To add icons to titles: AccordionItem(Div(UkIcon("icon-name", 16, 16), "Title Text", cls="flex items-center gap-2"), content...)
- Available parameters: title, content, cls, title_cls, content_cls, open, li_kwargs, a_kwargs, div_kwargs

Guidelines:
- Use Grid() for multiple items
- Use Div(cls="card bg-base-100 shadow-xl") for card layouts
- Use H3/H4 for titles, P for descriptions
- Use DiceBearAvatar for person profile pictures
- Use PicSumImg for placeholder images (vary the size based on context)
- Use UkIcon to enhance visual appeal with relevant icons
- Use Button with A() for external links
- Use Accordion for FAQ, step-by-step guides, or organizing lots of information
- For accordion titles with icons: AccordionItem(Div(UkIcon(...), "Text", cls="flex items-center gap-2"), content)
- Use Steps for tutorials, processes, workflows, and sequential guides
- For horizontal steps: Steps(LiStep(...), LiStep(...))
- For vertical steps: Steps(LiStep(...), LiStep(...), cls=StepsT.vertical)
- Mark completed steps with StepT.success, current step with StepT.primary, future steps with StepT.neutral
- For charts, ONLY use ApexChart with opts parameter
- Use proper DaisyUI classes: "card", "card-body", "card-title", "btn", "grid", etc.
- Make it visually appealing and informative

ICON EXAMPLES (common Lucide icons):
- UkIcon("user", 16, 16) for people
- UkIcon("map-pin", 16, 16) for locations
- UkIcon("calendar", 16, 16) for dates/events
- UkIcon("star", 16, 16) for ratings
- UkIcon("check", 16, 16) for checkmarks
- UkIcon("x", 16, 16) for errors/negatives
- UkIcon("info", 16, 16) for information
- UkIcon("external-link", 16, 16) for external links

AVATAR EXAMPLES:
- DiceBearAvatar("John Doe", 60, 60) for person cards
- DiceBearAvatar("Company Name", 40, 40) for smaller avatars

IMAGE EXAMPLES:
- PicSumImg(300, 200) for card headers
- PicSumImg(150, 150) for square thumbnails
- PicSumImg(400, 150, grayscale=True) for background images

NEVER use uk-chart, chart, or any other chart syntax. ONLY ApexChart.
NEVER use icon= parameter in AccordionItem. Put icons in the title content instead.

Return ONLY the FastHTML component code, no explanations:"""

    response = cli([prompt])
    print(f"LLM Response: {response}")

    # Extract text content from the response
    if hasattr(response, 'content') and len(response.content) > 0:
        response_text = response.content[0].text
    else:
        response_text = str(response)

    print(f"Extracted text: {response_text}")

    # Parse and execute the generated code
    component = parse_and_execute_component(response_text)
    return component

# Loading message component (shows while generating)
def LoadingMessage():
    return Div(cls="chat chat-start")(
        Div('assistant', cls="chat-header"),
        Div(cls="chat-bubble chat-bubble-secondary")(
            Div(cls="flex items-center space-x-3")(
                Loading((LoadingT.dots, LoadingT.md)),
                Span("Generating visual display...", cls="text-sm")
            )
        )
    )

# Chat message component (renders a chat bubble)
def ChatMessage(msg, user):
    bubble_class = "chat-bubble-primary" if user else 'chat-bubble-secondary'
    chat_class = "chat-end" if user else 'chat-start'
    return Div(cls=f"chat {chat_class}")(
               Div('user' if user else 'assistant', cls="chat-header"),
               Div(msg, cls=f"chat-bubble {bubble_class}"),
               Hidden(msg, name="messages")
           )

# Component message (renders generated UI components)
def ComponentMessage(component):
    return Div(cls="chat chat-start")(
        Div('assistant', cls="chat-header"),
        Div(cls="chat-bubble chat-bubble-secondary")(
            Div("Here's your visual display:", cls="mb-3 text-sm font-medium"),
            Div(component, cls="p-4 bg-base-100 rounded-lg border")
        )
    )

# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(name='msg', id='msg-input', placeholder="Ask me anything! I'll display information in the best visual format.",
                 cls="input input-bordered w-full", hx_swap_oob='true')

# Header component
def Header():
    return Div(cls="navbar bg-base-100 border-b")(
        Div(cls="navbar-start")(
            H1("🎨 Intelligent Visual Assistant", cls="text-xl font-bold")
        ),
        Div(cls="navbar-end")(
            Div(cls="flex items-center space-x-2")(
                Div(cls="badge badge-primary badge-outline")("AI-Powered"),
                Div(cls="badge badge-secondary badge-outline")("Charts & Visuals")
            )
        )
    )

# Footer component
def Footer():
    return Div(cls="footer footer-center p-4 bg-base-200 text-base-content border-t")(
        Div(
            P("Powered by FastHTML, MonsterUI & Claude AI", cls="text-sm text-gray-600")
        )
    )

# The main screen
@app.get
def index():
    page = Div(cls="min-h-screen flex flex-col")(
        Header(),
        Div(cls="flex-1 container mx-auto p-4")(
            Div(cls="max-w-6xl mx-auto")(
                # Welcome message
                Div(cls="text-center mb-6")(
                    H2("Ask me anything and I'll create beautiful visualizations", cls="text-2xl font-semibold text-gray-700 mb-2"),
                    P("Try: 'Who were the last 3 presidents?', 'Python tutorial steps', 'FAQ about electric cars'", cls="text-gray-500")
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
                                    cls="btn btn-primary"
                                )
                            )
                        )
                    )
                )
            )
        ),
        Footer()
    )
    return Titled('Intelligent Visual Assistant', page)

# Handle the form submission
@app.post
def send(msg: str, messages: list[str] = None):
    if not messages: messages = []
    messages.append(msg.rstrip())

    cli = Client(model)
    sp = """You are an intelligent visual information assistant. When users ask for information, you should present it in the most comprehensive and visually appealing way possible using the VisualDisplay tool.

Your job is to:
1. Analyze what type of information the user is asking for
2. Determine the best visual presentation format
3. Use the VisualDisplay tool to create an appropriate display

Examples of how to respond:

USER: "Who were the last 3 presidents?"
→ Use VisualDisplay(content_type="people", data=["Joe Biden", "Donald Trump", "Barack Obama"], context="Last 3 US Presidents with terms, key achievements, avatars, and links")

USER: "What are the largest cities in California?"
→ Use VisualDisplay(content_type="places", data=["Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno"], context="Largest cities in California with population, images, and key facts")

USER: "Python tutorial steps"
→ Use VisualDisplay(content_type="tutorial", data=["Install Python", "Setup IDE", "Variables", "Functions", "Classes"], context="Python learning tutorial with expandable steps, icons, and accordion")

USER: "FAQ about electric cars"
→ Use VisualDisplay(content_type="faq", data=["How far can they go?", "How long to charge?", "Are they expensive?", "Environmental impact?"], context="Electric car FAQ with collapsible answers and icons")

USER: "Show me Apple stock performance this year"
→ Use VisualDisplay(content_type="charts", data=["150", "160", "140", "155", "170"], context="Apple stock price chart showing monthly performance with line chart")

USER: "Compare iPhone vs Android market share"
→ Use VisualDisplay(content_type="charts", data=["iPhone: 25%", "Android: 71%", "Others: 4%"], context="Mobile OS market share comparison using pie chart")

USER: "Timeline of World War II"
→ Use VisualDisplay(content_type="timeline", data=["1939 - War begins", "1941 - Pearl Harbor", "1944 - D-Day", "1945 - War ends"], context="Major events of World War II timeline with icons and dates")

IMPORTANT:
- For people: use content_type="people" to create cards with avatars and biographical info
- For places: use content_type="places" to create cards with images and location details
- For step-by-step guides, tutorials, FAQ: use content_type="tutorial" or "faq" with icons and accordion
- For numerical data, trends, statistics: use content_type="charts" to create ApexChart visualizations
- Always include visual elements like icons, avatars, and images when appropriate
- Choose the best visual format for the information type

Always use VisualDisplay when the user asks for factual information that can be presented visually. For simple conversations or clarifying questions, respond normally with text."""

    try:
        r = cli.structured([sp, msg], tools=[VisualDisplay])
        print("Response: ", r)

        # Check if the response contains a generated component
        response_parts = []
        for item in r:
            if hasattr(item, '__call__') or hasattr(item, 'render') or str(type(item)).find('fasthtml') != -1:
                # This is likely a UI component
                response_parts.append(ComponentMessage(item))
            else:
                # This is text response
                response_parts.append(ChatMessage(str(item), False))

        return (ChatMessage(msg, True), *response_parts, ChatInput())

    except Exception as e:
        print(f"Error: {e}")
        return (ChatMessage(msg, True),
                ChatMessage(f"Sorry, I encountered an error: {str(e)}", False),
                ChatInput())

serve()
