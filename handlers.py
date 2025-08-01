import os
import datetime
from client import create_openai_client, get_completion
from components import ChatMessage, ComponentMessage, ChatInput, parse_and_execute_component

def load_context(path: str):
    """Load the LLM context from llms-ctx.txt"""
    context_path = os.path.join(os.path.dirname(__file__), path)
    try:
        with open(context_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "FastHTML context file not found. Using basic FastHTML knowledge."

def handle_chat_send(msg: str, messages: list[str] = None):
    """Handle the form submission for chat messages with conversation context"""
    if not messages:
        messages = []
    messages.append(msg.rstrip())

    # Load context from file
    components_context = load_context("llms-ctx-components.txt")

    system_prompt = f"""You are an expert visual UI designer that transforms complex information into beautifully digestible FastHTML/MonsterUI components.

This UI component should directly address or visualize the user's request (e.g., if they ask for "weather", create a weather card UI).
The generated UI should be visually appealing, creative where it makes sense for visualizations, modern, and functional, and add animations where it makes sense, i.e. for a weather app you may animate rainfall.
For any UI you generate that might need an API key, i.e. weather, just simulate the effect, we do not need these to be wired up.
If generating UI is not appropriate for the user's query, or if you are unable to fulfill the UI request, you may respond with a polite text message explaining why.

# COMPONENT REFERENCE:
{components_context}

🎯 MISSION: Transform the user's request into a visually rich, interactive component that makes complex concepts easy to understand and engage with.

📋 DESIGN PRINCIPLES:
• Visual Hierarchy: Use clear headings, spacing, and typography to guide the eye
• Information Architecture: Break complex data into scannable chunks using cards, grids, and sections
• Progressive Disclosure: Use accordions, tabs, and collapsible sections for deep content
• Visual Cues: Employ icons, colors, badges, and visual indicators to communicate meaning instantly
• Cognitive Load Reduction: Present information in bite-sized, organized pieces
• Interactive Elements: Make content explorable with hover states, expandable sections, and clear navigation
• Use MonsterUI components for the best user experience
• Use TailwindCSS for styling

🎨 COMPONENT SELECTION GUIDE:

For EXPLANATIONS/CONCEPTS → Use Accordion with expandable sections, each with icons and clear headings
For PROCESSES/TUTORIALS → Use Steps with visual progression indicators and detailed descriptions
For COMPARISONS → Use side-by-side cards or tables with clear visual differentiators
For DATA/STATISTICS → Use ApexChart(opts={...}) with proper options object, Progress components for percentages
For TIMELINES/HISTORY → Use Steps (vertical) or timeline cards with dates prominently displayed
For FORMS/INPUT → Use well-structured forms with clear labels and validation hints
For LISTS/CATALOGS → Use Grid with cards containing images, titles, and key info
For COMPLEX INFO → Use tabbed interfaces or accordion patterns

🚀 TECHNICAL REQUIREMENTS:
1. Output ONLY a single FastHTML/MonsterUI component expression
2. NO imports, app setup, routes, or serve() calls
3. Use rich styling with DaisyUI and TailwindCSS classes (cards, shadows, gradients, spacing)
4. Include visual elements: UkIcon, DiceBearAvatar, PicSumImg where appropriate
5. Make it responsive with proper Grid columns and spacing
6. Use semantic colors and typography for better readability

⚠️ CRITICAL COMPONENT USAGE - AVOID THESE ERRORS:

❌ WRONG: ApexChart() - Missing required 'opts' parameter
✅ CORRECT: ApexChart(opts={{"chart": {{"type": "bar"}}, "series": [{{"name": "Data", "data": [10, 20, 30]}}]}})

❌ WRONG: Badge("text") - Badge doesn't exist in FastHTML/MonsterUI
✅ CORRECT: Use Alert, Span with classes, or UkIcon for badges/indicators

❌ WRONG: Card(H3("Title"), P("Content")) - Wrong Card syntax
✅ CORRECT: Card(cls="p-4")(H3("Title"), P("Content"))


COMPONENT SYNTAX RULES:
• ApexChart: ALWAYS include opts parameter with chart config
• Cards: Use Card(cls="...")(content) format
• Badges/Labels: Use Alert, Span + classes, or colored Div
• Charts: Only ApexChart exists, requires opts={{"chart": {{...}}, "series": [...]}}
• Icons: UkIcon("icon-name", width, height) format
• Progress: Progress(value=X, max=100) format
• No Badge component exists - use alternatives

🌟 ELEVATED EXAMPLES:

User: "Explain photosynthesis"
Output:
Div(cls="max-w-4xl mx-auto p-6")(
    Div(cls="text-center mb-8")(
        UkIcon("sun", 48, 48, cls="text-yellow-500 mb-4"),
        H1("Photosynthesis", cls="text-4xl font-bold text-green-700 mb-2"),
        P("How plants convert sunlight into energy", cls="text-xl text-gray-600")
    ),
    Accordion(
        AccordionItem(
            Div(UkIcon("lightbulb", 20, 20), "What is Photosynthesis?", cls="flex items-center gap-3"),
            Div(cls="p-4 bg-green-50 rounded-lg")(
                P("The process by which plants use sunlight, water, and carbon dioxide to create glucose and oxygen."),
                Div(cls="mt-4 p-3 bg-white rounded border-l-4 border-green-500")(
                    Strong("Formula: "), CodeSpan("6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂")
                )
            )
        ),
        AccordionItem(
            Div(UkIcon("settings", 20, 20), "The Process", cls="flex items-center gap-3"),
            Steps(
                LiStep("Light Absorption", cls=StepT.success, data_content="1"),
                LiStep("Water Splitting", cls=StepT.info, data_content="2"),
                LiStep("CO₂ Fixation", cls=StepT.warning, data_content="3"),
                LiStep("Glucose Production", cls=StepT.primary, data_content="4"),
                cls=StepsT.vertical
            )
        ),
        AccordionItem(
            Div(UkIcon("activity", 20, 20), "Importance", cls="flex items-center gap-3"),
            Grid(
                Card(H4("🌍 Global Impact"), P("Produces 70% of Earth's oxygen"), cls="bg-blue-50 p-4"),
                Card(H4("🍃 Plant Growth"), P("Creates energy for all plant functions"), cls="bg-green-50 p-4"),
                Card(H4("🔋 Energy Storage"), P("Forms the base of food chains"), cls="bg-yellow-50 p-4"),
                cols=3
            )
        )
    )
)

User: "Compare Python vs JavaScript"
Output:
Div(cls="max-w-6xl mx-auto p-6")(
    H1("Python vs JavaScript", cls="text-3xl font-bold text-center mb-8"),
    Grid(
        Card(cls="bg-blue-50 border-2 border-blue-200 p-6")(
            Div(cls="flex items-center gap-3 mb-4")(
                UkIcon("code", 32, 32, cls="text-blue-600"),
                H2("Python", cls="text-2xl font-bold text-blue-800")
            ),
            Div(cls="space-y-4")(
                Div(cls="flex items-center gap-2 text-green-600")(
                    UkIcon("check", 16, 16), Strong("Easy to learn")
                ),
                Div(cls="flex items-center gap-2 text-green-600")(
                    UkIcon("check", 16, 16), Strong("Great for data science")
                )
            ),
            Alert("Best for: AI, Data Science, Backend", cls=AlertT.info)
        ),
        Card(cls="bg-yellow-50 border-2 border-yellow-200 p-6")(
            Div(cls="flex items-center gap-3 mb-4")(
                UkIcon("globe", 32, 32, cls="text-yellow-600"),
                H2("JavaScript", cls="text-2xl font-bold text-yellow-800")
            ),
            Div(cls="space-y-4")(
                Div(cls="flex items-center gap-2 text-green-600")(
                    UkIcon("check", 16, 16), Strong("Runs everywhere")
                ),
                Div(cls="flex items-center gap-2 text-green-600")(
                    UkIcon("check", 16, 16), Strong("Interactive UIs")
                )
            ),
            Alert("Best for: Web Development, Mobile Apps", cls=AlertT.warning)
        ),
        cols=2
    )
)

User: "Show sales data chart"
Output:
Div(cls="max-w-4xl mx-auto p-6")(
    H2("Sales Performance", cls="text-2xl font-bold mb-6"),
    ApexChart(opts={{
        "chart": {{"type": "line", "height": 350}},
        "series": [{{"name": "Sales", "data": [30, 40, 35, 50, 49, 60, 70, 91, 125]}}],
        "xaxis": {{"categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]}},
        "stroke": {{"curve": "smooth"}},
        "title": {{"text": "Monthly Sales Trends"}}
    }})
)

DO NOT create endpoints, routes, or serve() calls. ONLY return the FastHTML/MonsterUI component code.
Now create a visually stunning, information-rich component for the user's request."""


    try:
        import time


        client = create_openai_client()

        # Build conversation context for API
        messages_for_api = [{"role": "system", "content": system_prompt}]

        # Add conversation history (alternating user/assistant)
        for i, message in enumerate(messages):
            role = "user" if i % 2 == 0 else "assistant"
            messages_for_api.append({"role": role, "content": message})

        import time
        start_time = time.time()
        response_data = get_completion(client, messages_for_api)
        result = _try_execute_with_retry(msg, response_data["content"], messages, max_retries=3)
        total_time = time.time() - start_time


        generation_info = {
            "total_time": total_time,
            "tokens": response_data["tokens"]["completion"]
        }

        return _add_timing_to_result(result, generation_info)

    except Exception as e:
        print(f"Error: {e}")
        return (ChatMessage(msg, True),
                ChatMessage(f"Sorry, I encountered an error: {str(e)}", False),
                ChatInput())

def _add_timing_to_result(result, generation_info):
    """Add generation information to the component result"""
    if isinstance(result, tuple) and len(result) >= 2:
        # Find the ComponentMessage in the result tuple and update it
        result_list = list(result)
        for i, item in enumerate(result_list):
            # Look for ComponentMessage by checking its structure
            if (hasattr(item, 'children') and len(item.children) >= 3 and
                hasattr(item.children[1], 'children') and
                any('interactive-component' in str(child) for child in item.children[1].children if hasattr(child, 'attrs'))):

                # Extract the original component from the ComponentMessage
                component = item.children[1].children[0].children[0]

                # Create new ComponentMessage with generation info
                from components import ComponentMessage
                result_list[i] = ComponentMessage(
                    component,
                    generation_info=generation_info,
                    context_msg="Generated interactive component"
                )
                break
        return tuple(result_list)

    return result

def _try_execute_with_retry(original_msg: str, generated_code: str, messages: list[str], max_retries: int = 3, retry_count: int = 0):
    """Try to execute code with retry mechanism for fixing errors"""

    try:
        component = parse_and_execute_component(generated_code)
        success_result = [ChatMessage(original_msg, True)]

        # Add retry indicator if this was a retry
        if retry_count > 0:
            success_result.append(ChatMessage(f"✅ Fixed after {retry_count} attempt(s)", False))

        success_result.append(ComponentMessage(component))
        success_result.append(ChatInput())
        return tuple(success_result)

    except Exception as code_error:
        print(f"Error executing generated code (attempt {retry_count + 1}): {code_error}")

        # If we've reached max retries, return the error
        if retry_count >= max_retries:
            result = [ChatMessage(original_msg, True)]
            result.append(ChatMessage(f"❌ Failed after {max_retries + 1} attempts. Final error: {str(code_error)}", False))
            result.append(ChatMessage("Raw code:", False))
            result.append(ChatMessage(f"```\n{generated_code}\n```", False))
            result.append(ChatInput())
            return tuple(result)

        # Try to get the LLM to fix the error
        return _retry_with_error_feedback(original_msg, generated_code, str(code_error), messages, retry_count)

def _retry_with_error_feedback(original_msg: str, failed_code: str, error_message: str, messages: list[str], retry_count: int):
    """Ask LLM to fix the error and retry"""

    # Load context
    components_context = load_context("llms-ctx-components.txt")

    # Create error-fixing prompt
    fix_prompt = f"""You are an expert FastHTML/MonsterUI developer. Fix the error in the generated code.

# COMPONENT REFERENCE:
{components_context}

ORIGINAL REQUEST: {original_msg}

GENERATED CODE THAT FAILED:
```
{failed_code}
```

ERROR MESSAGE: {error_message}

Please fix the error and return ONLY the corrected FastHTML/MonsterUI component code. Common fixes:

CRITICAL FIXES:
- ApexChart MUST have opts parameter: ApexChart(opts={{"chart": {{"type": "bar"}}, "series": [...]}})
- Badge component does NOT exist - use Alert, Span with classes, or colored Div instead
- Card syntax: Card(cls="...")(content) not Card(content, cls="...")
- Button cls error: Never pass cls as both positional and keyword - use Button("Text", cls=ButtonT.primary)
- Duplicate cls error: Never pass cls parameter twice - merge into single cls="class1 class2"
- Assignment in expression: Don't use = in expressions - use separate variables or data attributes
- Progress needs value/max: Progress(value=75, max=100)
- UkIcon needs width/height: UkIcon("name", 16, 16)

SYNTAX FIXES:
- Check parentheses, brackets, and quotes are properly matched
- Ensure proper component parameters and structure
- Use correct DaisyUI/TailwindCSS class names

Return ONLY the fixed component code:"""

    try:
        client = create_openai_client()
        messages_for_api = [
            {"role": "system", "content": fix_prompt}
        ]

        print(f"🔄 Retry attempt {retry_count + 1}: Asking LLM to fix error...")
        response_data = get_completion(client, messages_for_api)
        response = response_data["content"]
        print(f"🔧 Fix attempt response: {response}")

        # Try executing the fixed code
        return _try_execute_with_retry(original_msg, response, messages, max_retries=3, retry_count=retry_count + 1)

    except Exception as e:
        print(f"Error in retry mechanism: {e}")
        # Fall back to original error display
        result = [ChatMessage(original_msg, True)]
        result.append(ChatMessage(f"❌ Retry failed: {str(e)}", False))
        result.append(ChatInput())
        return tuple(result)