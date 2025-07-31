import os
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
    fasthtml_context = load_context("llms-ctx-fast-html.txt")
    monsterui_context = load_context("llms-ctx-monster-ui.txt")

    system_prompt = f"""You are an expert visual UI designer that transforms complex information into beautifully digestible FastHTML/MonsterUI components.

CONTEXT:
<fasthtml>
{fasthtml_context}
</fasthtml>

<monsterui>
{monsterui_context}
</monsterui>

🎯 MISSION: Transform the user's request into a visually rich, interactive component that makes complex concepts easy to understand and engage with.

📋 DESIGN PRINCIPLES:
• Visual Hierarchy: Use clear headings, spacing, and typography to guide the eye
• Information Architecture: Break complex data into scannable chunks using cards, grids, and sections
• Progressive Disclosure: Use accordions, tabs, and collapsible sections for deep content
• Visual Cues: Employ icons, colors, badges, and visual indicators to communicate meaning instantly
• Cognitive Load Reduction: Present information in bite-sized, organized pieces
• Interactive Elements: Make content explorable with hover states, expandable sections, and clear navigation

🎨 COMPONENT SELECTION GUIDE:

For EXPLANATIONS/CONCEPTS → Use Accordion with expandable sections, each with icons and clear headings
For PROCESSES/TUTORIALS → Use Steps with visual progression indicators and detailed descriptions
For COMPARISONS → Use side-by-side cards or tables with clear visual differentiators
For DATA/STATISTICS → Use ApexChart for numerical data, progress bars for percentages
For TIMELINES/HISTORY → Use Steps (vertical) or timeline cards with dates prominently displayed
For FORMS/INPUT → Use well-structured forms with clear labels and validation hints
For LISTS/CATALOGS → Use Grid with cards containing images, titles, and key info
For COMPLEX INFO → Use tabbed interfaces or accordion patterns

🚀 TECHNICAL REQUIREMENTS:
1. Output ONLY a single FastHTML/MonsterUI component expression
2. NO imports, app setup, routes, or serve() calls
3. Use rich styling with DaisyUI classes (cards, shadows, gradients, spacing)
4. Include visual elements: UkIcon, DiceBearAvatar, PicSumImg where appropriate
5. Make it responsive with proper Grid columns and spacing
6. Use semantic colors and typography for better readability

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
    H1("Python vs JavaScript", cls="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-blue-600 to-yellow-500 bg-clip-text text-transparent"),
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
                ),
                Div(cls="flex items-center gap-2 text-green-600")(
                    UkIcon("check", 16, 16), Strong("Extensive libraries")
                ),
                Div(cls="flex items-center gap-2 text-red-600")(
                    UkIcon("x", 16, 16), Strong("Slower execution")
                )
            ),
            Div(cls="mt-6 p-3 bg-blue-100 rounded")(
                Strong("Best for: "), "AI, Data Science, Backend, Automation"
            )
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
                ),
                Div(cls="flex items-center gap-2 text-green-600")(
                    UkIcon("check", 16, 16), Strong("Fast execution")
                ),
                Div(cls="flex items-center gap-2 text-red-600")(
                    UkIcon("x", 16, 16), Strong("Complex syntax")
                )
            ),
            Div(cls="mt-6 p-3 bg-yellow-100 rounded")(
                Strong("Best for: "), "Web Development, Mobile Apps, Real-time Apps"
            )
        ),
        cols=2
    )
)

Now create a visually stunning, information-rich component for the user's request:"""


    try:
        client = create_openai_client()

        # Build conversation context for API
        messages_for_api = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (alternating user/assistant)
        for i, message in enumerate(messages):
            role = "user" if i % 2 == 0 else "assistant"
            messages_for_api.append({"role": role, "content": message})

        response = get_completion(client, messages_for_api)

        # Parse and execute the generated FastHTML code
        return _try_execute_with_retry(msg, response, messages, max_retries=3)

    except Exception as e:
        print(f"Error: {e}")
        return (ChatMessage(msg, True),
                ChatMessage(f"Sorry, I encountered an error: {str(e)}", False),
                ChatInput())

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
    context_files = ["llms-ctx-fast-html.txt", "llms-ctx-monster-ui.txt"]
    fasthtml_context = load_context(context_files[0])
    monsterui_context = load_context(context_files[1])

    # Create error-fixing prompt
    fix_prompt = f"""You are an expert FastHTML/MonsterUI developer. Fix the error in the generated code.

CONTEXT:
<fasthtml>
{fasthtml_context}
</fasthtml>

<monsterui>
{monsterui_context}
</monsterui>

ORIGINAL REQUEST: {original_msg}

GENERATED CODE THAT FAILED:
```
{failed_code}
```

ERROR MESSAGE: {error_message}

Please fix the error and return ONLY the corrected FastHTML/MonsterUI component code. Common fixes:
- For ApexChart errors: Make sure to include the required 'opts' parameter
- For missing parameters: Check component documentation for required parameters
- For syntax errors: Check parentheses, brackets, and quotes are properly matched
- For component errors: Ensure proper component usage as documented

Return ONLY the fixed component code:"""

    try:
        client = create_openai_client()
        messages_for_api = [
            {"role": "system", "content": fix_prompt}
        ]

        print(f"🔄 Retry attempt {retry_count + 1}: Asking LLM to fix error...")
        response = get_completion(client, messages_for_api)
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