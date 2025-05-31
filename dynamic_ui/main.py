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
    # Typography components
    'TextPresets': TextPresets,
    'TextT': TextT,
    'CodeSpan': CodeSpan,
    'Blockquote': Blockquote,
    'CodeBlock': CodeBlock,
    'I': I,
    'Small': Small,
    'Mark': Mark,
    'Sub': Sub,
    'Sup': Sup,
    'Del': Del,
    'Ins': Ins,
    'Dfn': Dfn,
    'Abbr': Abbr,
    'Q': Q,
    'Kbd': Kbd,
    'Samp': Samp,
    'Var': Var,
    'Figure': Figure,
    'Caption': Caption,
    'Details': Details,
    'Summary': Summary,
    'Meter': Meter,
    'Data': Data,
    'Output': Output,
    'Address': Address,
    'Time': Time,
    'Cite': Cite,
    'Section': Section,
    'U': U,
    'S': S,
    'Pre': Pre,
    'Code': Code,
    'Titled': Titled,
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
    # Form components
    'FormLabel': FormLabel,
    'LabelInput': LabelInput,
    'LabelCheckboxX': LabelCheckboxX,
    'LabelSwitch': LabelSwitch,
    'LabelRange': LabelRange,
    'LabelTextArea': LabelTextArea,
    'LabelRadio': LabelRadio,
    'LabelSelect': LabelSelect,
    'Progress': Progress,
    'Radio': Radio,
    'CheckboxX': CheckboxX,
    'Range': Range,
    'Switch': Switch,
    'TextArea': TextArea,
    'Legend': Legend,
    'Fieldset': Fieldset,
    'Upload': Upload,
    'UploadZone': UploadZone,
    'Hidden': Hidden,
    # Button styles
    'ButtonT': ButtonT,
    'TextPresets': TextPresets,
    'DivCentered': DivCentered,
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
        # Ensure code_text is a string
        if not isinstance(code_text, str):
            code_text = str(code_text)

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
        return Div(
            Div(cls="flex items-center gap-2 mb-2")(
                UkIcon("alert-triangle", 16, 16, cls="text-warning"),
                Strong("Visualization Error")
            ),
            P(f"Failed to generate component: {str(e)}", cls=TextPresets.muted_sm),
            cls="alert alert-warning p-4 rounded-lg bg-warning/10 border border-warning/20"
        )

# Define the visual information display function
def VisualDisplay(content_type: str, data: list[str], context: str):
    """Generate the best visual representation for the given information.

    content_type: The type of information (people, places, products, timeline, comparison, list, charts, etc.)
    data: The actual data points to display
    context: Additional context about what the user is asking for
    """
    print(f"Creating visual display for: {content_type}, data: {data}, context: {context}")

    try:
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

For FORMS/SURVEYS/INPUT COLLECTION:
- Use Form() as the container with proper spacing: Form(cls="space-y-4")
- Use LabelInput("Label", id="unique_id") for text inputs
- Use LabelTextArea("Label", id="unique_id") for multi-line text
- Use LabelCheckboxX("Option") for checkboxes
- Use LabelRadio("Option", id="unique_id") for radio buttons (same name for groups)
- Use LabelSelect("Label", Option("Choice 1"), Option("Choice 2"), id="unique_id") for dropdowns
- Use LabelSwitch("Label", id="unique_id") for toggle switches
- Use LabelRange("Label", min=0, max=100, value=50, id="unique_id") for sliders
- Use Progress(value="75", max="100") for progress indicators
- Use Upload("Upload Files", id="upload1") for file uploads
- Use UploadZone(DivCentered(Span("Drop files here"), UkIcon("upload")), id="upload2") for drag-drop upload
- Use Fieldset and Legend for form sections: Fieldset(Legend("Section Title"), form_content...)
- Use Grid() to organize form fields in columns
- Use Button("Submit", cls=ButtonT.primary) for form submission
- Use DivCentered() to center form elements

FORM EXAMPLES:
Contact Form:
Form(cls="space-y-4")(
    DivCentered(H3("Contact Us"), P("Fill out the form below", cls=TextPresets.muted_sm)),
    Grid(LabelInput("First Name", id="fn"), LabelInput("Last Name", id="ln")),
    LabelInput("Email", id="email"),
    LabelTextArea("Message", id="msg"),
    DivCentered(Button("Send Message", cls=ButtonT.primary))
)

Survey Form:
Form(cls="space-y-4")(
    Fieldset(
        Legend("Personal Information"),
        Grid(LabelInput("Name", id="name"), LabelInput("Age", id="age")),
        LabelSelect("Country", Option("USA"), Option("Canada"), Option("UK"), id="country")
    ),
    Fieldset(
        Legend("Preferences"),
        H4("Select your interests:"),
        Grid(*[LabelCheckboxX(opt) for opt in ["Sports", "Music", "Travel", "Food"]], cols=2),
        LabelRange("Satisfaction", min=1, max=10, value=7, id="satisfaction")
    ),
    DivCentered(Button("Submit Survey", cls=ButtonT.primary))
)

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

Available components: Grid, Button, Div, Select, Option, Input, Label, Span, P, H1, H2, H3, H4, H5, H6, Form, A, Img, Ul, Li, Ol, Strong, Em, I, Small, Mark, Sub, Sup, Del, Ins, Dfn, Abbr, Q, Kbd, Samp, Var, Figure, Caption, Details, Summary, Meter, Data, Output, Address, Time, Cite, Section, U, S, Pre, Code, Titled, CodeSpan, Blockquote, CodeBlock, Br, Hr, Table, Tr, Td, Th, Thead, Tbody, ApexChart, Loading, LoadingT, Accordion, AccordionItem, Steps, LiStep, StepsT, StepT, DiceBearAvatar, PicSumImg, UkIcon, UkIconLink, FormLabel, LabelInput, LabelCheckboxX, LabelSwitch, LabelRange, LabelTextArea, LabelRadio, LabelSelect, Progress, Radio, CheckboxX, Range, Switch, TextArea, Legend, Fieldset, Upload, UploadZone, Hidden, ButtonT, TextPresets, TextT, DivCentered

TYPOGRAPHY COMPONENTS:
- All standard typography: H1-H6, P, Strong, Em, I, Small, Mark, Sub, Sup, Del, Ins, U, S
- Semantic elements: Dfn (definitions), Abbr (abbreviations), Q (quotes), Kbd (keyboard), Samp (sample output), Var (variables)
- Code elements: CodeSpan (inline code), CodeBlock (code blocks), Pre, Code
- Content structure: Figure, Caption, Details, Summary, Section, Address, Time, Cite
- Data elements: Meter (progress/gauge), Data (semantic data), Output (form results)
- Text styling: TextPresets (common styles), TextT (style options)

TYPOGRAPHY USAGE EXAMPLES:
- For text emphasis: Strong("bold text"), Em("emphasized"), I("italic"), Small("smaller text")
- For highlighting: Mark("highlighted text"), U("underlined"), S("strikethrough")
- For technical content: CodeSpan("inline code"), Kbd("Ctrl+C"), Samp("output text"), Var("variable")
- For definitions: Dfn("HTML"), Abbr("WWW", title="World Wide Web"), Q("quoted text")
- For scientific notation: H2("Water is H", Sub("2"), "O") or P("E=mc", Sup("2"))
- For edits: Del("old text"), Ins("new text")
- For code blocks: CodeBlock("def hello():\n    print('world')")
- For figures: Figure(PicSumImg(300, 200), Caption("Figure 1: Example"))
- For interactive content: Details(Summary("Click to expand"), P("Hidden content"))
- For data: Data("$42.99", value="42.99"), Meter(value=0.7, min=0, max=1)
- For contact info: Address("123 Main St", Br(), "City, State 12345")
- For time: Time("January 1, 2024", datetime="2024-01-01")
- For quotes: Blockquote(P("Great quote"), Cite("Author Name"))
- For text styling: P("Text", cls=TextPresets.muted_sm) or Span("Text", cls=TextT.bold)

Available components: Grid, Button, Div, Select, Option, Input, Label, Span, P, H1, H2, H3, H4, H5, H6, Form, A, Img, Ul, Li, Ol, Strong, Em, I, Small, Mark, Sub, Sup, Del, Ins, Dfn, Abbr, Q, Kbd, Samp, Var, Figure, Caption, Details, Summary, Meter, Data, Output, Address, Time, Cite, Section, U, S, Pre, Code, Titled, CodeSpan, Blockquote, CodeBlock, Br, Hr, Table, Tr, Td, Th, Thead, Tbody, ApexChart, Loading, LoadingT, Accordion, AccordionItem, Steps, LiStep, StepsT, StepT, DiceBearAvatar, PicSumImg, UkIcon, UkIconLink, FormLabel, LabelInput, LabelCheckboxX, LabelSwitch, LabelRange, LabelTextArea, LabelRadio, LabelSelect, Progress, Radio, CheckboxX, Range, Switch, TextArea, Legend, Fieldset, Upload, UploadZone, Hidden, ButtonT, TextPresets, TextT, DivCentered

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
- For forms, use proper form components with unique IDs and proper styling
- Use Form(cls="space-y-4") for consistent form spacing
- Use Grid() to organize form fields in responsive columns
- Use DivCentered() for centered form elements like titles and buttons
- Use Fieldset and Legend to group related form fields
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
- UkIcon("upload", 16, 16) for file uploads
- UkIcon("mail", 16, 16) for contact forms

AVATAR EXAMPLES:
- DiceBearAvatar("John Doe", 60, 60) for person cards
- DiceBearAvatar("Company Name", 40, 40) for smaller avatars

IMAGE EXAMPLES:
- PicSumImg(300, 200) for card headers
- PicSumImg(150, 150) for square thumbnails
- PicSumImg(400, 150, grayscale=True) for background images

BUTTON STYLE EXAMPLES:
- ButtonT.primary for main actions
- ButtonT.secondary for secondary actions
- ButtonT.success for positive actions
- ButtonT.warning for warning actions
- ButtonT.error for destructive actions

NEVER use uk-chart, chart, or any other chart syntax. ONLY ApexChart.
NEVER use icon= parameter in AccordionItem. Put icons in the title content instead.
ALWAYS use unique IDs for form elements to ensure proper functionality.

CRITICAL MONSTERUI COMPONENT SYNTAX:
- DiceBearAvatar("Name", width, height) - NO cls parameter allowed!
- PicSumImg(width, height) - NO cls parameter for basic usage
- UkIcon("icon-name", width, height) - Can use cls parameter
- For positioning DiceBearAvatar, wrap it in a Div with cls: Div(DiceBearAvatar("Name", 80, 80), cls="mx-auto mb-4")

Return ONLY the FastHTML component code, no explanations:
"""

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

    except Exception as e:
        print(f"Error in VisualDisplay: {e}")
        return Div(
            Div(cls="flex items-center gap-2 mb-2")(
                UkIcon("alert-circle", 16, 16, cls="text-error"),
                Strong("Unable to Create Visualization")
            ),
            P(f"Failed to generate visual display: {str(e)}", cls=TextPresets.muted_sm),
            cls="alert alert-error p-4 rounded-lg bg-error/10 border border-error/20"
        )

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
        Div(cls="chat-bubble chat-bubble-secondary p-1")(
            Div(component, cls="bg-base-100 rounded-lg border p-4")
        )
    )

# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(name='msg',
                id='msg-input',
                placeholder="Chat with me! I'll respond with rich visual components and interactive UI elements",
                cls="input input-bordered w-full",
                hx_swap_oob='true',
                autocomplete="off")

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
    if not messages: messages = []
    messages.append(msg.rstrip())

    cli = Client(model)
    sp = """You are a dynamic generative UI assistant that creates rich visual components. Your responses should be SHORT and TO THE POINT while focusing on visual elements.

RESPONSE STYLE:
- Give brief, direct answers (1-2 sentences max for text)
- Always enhance with appropriate visual components using VisualDisplay
- Focus on the most essential information
- Let the visuals tell the story, not lengthy text

WHEN TO USE VisualDisplay:
- Factual questions about people, places, events, etc.
- Requests for tutorials, guides, or step-by-step instructions
- Form creation requests
- Data visualization needs
- Comparison requests
- FAQ or informational content

RESPONSE EXAMPLES:

USER: "Who were the last 3 presidents?"
SHORT TEXT: "Here are the last 3 US Presidents:"
→ Use VisualDisplay(content_type="people", data=["Joe Biden (2021-present)", "Donald Trump (2017-2021)", "Barack Obama (2009-2017)"], context="Last 3 US Presidents with terms, achievements, and key facts")

USER: "Python tutorial steps"
SHORT TEXT: "Here's a Python learning path:"
→ Use VisualDisplay(content_type="tutorial", data=["Install Python", "Learn syntax", "Variables & data types", "Functions", "Classes & objects"], context="Python tutorial steps with expandable details and progress tracking")

USER: "Create a contact form"
SHORT TEXT: "Professional contact form:"
→ Use VisualDisplay(content_type="forms", data=["Name", "Email", "Subject", "Message"], context="Clean contact form with validation and professional styling")

USER: "Compare iPhone vs Android"
SHORT TEXT: "Mobile OS comparison:"
→ Use VisualDisplay(content_type="comparison", data=["iPhone features", "Android features", "Market share", "Price ranges"], context="iPhone vs Android feature comparison with pros/cons")

USER: "What's the weather like?"
SIMPLE TEXT RESPONSE: "I don't have access to real-time weather data. Please check a weather service like weather.com or your local weather app."

IMPORTANT RULES:
- Use VisualDisplay for ANY factual information that can be visualized
- Keep text responses under 20 words when possible
- For simple questions without visual potential, give direct text answers
- Always prioritize clarity and usefulness over verbosity
- Make visuals comprehensive so text can be minimal"""

    try:
        r = cli.structured([sp, msg], tools=[VisualDisplay])
        print("Response: ", r)

        # Process the response
        response_parts = []
        text_response = ""

        for item in r:
            if hasattr(item, '__call__') or hasattr(item, 'render') or str(type(item)).find('fasthtml') != -1:
                # This is a UI component - add it as a component message
                response_parts.append(ComponentMessage(item))
            else:
                # This is text - accumulate it
                text_response += str(item) + " "

        # Add the user message first
        result = [ChatMessage(msg, True)]

        # Add text response if we have any
        if text_response.strip():
            result.append(ChatMessage(text_response.strip(), False))

        # Add component responses
        result.extend(response_parts)

        # Add fresh input field
        result.append(ChatInput())

        return tuple(result)

    except Exception as e:
        print(f"Error: {e}")
        return (ChatMessage(msg, True),
                ChatMessage(f"Sorry, I encountered an error: {str(e)}", False),
                ChatInput())

serve()
