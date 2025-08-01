from fasthtml.common import *
from monsterui.all import *

def auto_repair_syntax(code_text):
    """Attempt to automatically repair common syntax errors in LLM-generated code."""

    # Remove any stray HTML or XML-like content that sometimes appears
    import re
    code_text = re.sub(r'<[^>]+>', '', code_text)

    # Fix unmatched parentheses - count and balance them
    open_parens = code_text.count('(')
    close_parens = code_text.count(')')

    if open_parens > close_parens:
        # Add missing closing parentheses
        missing_close = open_parens - close_parens
        code_text += ')' * missing_close
    elif close_parens > open_parens:
        # Remove extra closing parentheses from the end
        extra_close = close_parens - open_parens
        # Remove from the end first
        while extra_close > 0 and code_text.endswith(')'):
            code_text = code_text[:-1]
            extra_close -= 1

    # Fix unmatched square brackets
    open_brackets = code_text.count('[')
    close_brackets = code_text.count(']')

    if open_brackets > close_brackets:
        missing_close = open_brackets - close_brackets
        code_text += ']' * missing_close
    elif close_brackets > open_brackets:
        extra_close = close_brackets - open_brackets
        while extra_close > 0 and code_text.endswith(']'):
            code_text = code_text[:-1]
            extra_close -= 1

    # Fix unmatched curly braces
    open_braces = code_text.count('{')
    close_braces = code_text.count('}')

    if open_braces > close_braces:
        missing_close = open_braces - close_braces
        code_text += '}' * missing_close
    elif close_braces > open_braces:
        extra_close = close_braces - open_braces
        while extra_close > 0 and code_text.endswith('}'):
            code_text = code_text[:-1]
            extra_close -= 1

    # Fix missing spaces after commas in common patterns
    code_text = re.sub(r',([^\s])', r', \1', code_text)

    # Fix common typos in component names
    typo_fixes = {
        'UKIcon': 'UkIcon',
        'ukIcon': 'UkIcon',
        'Ukicon': 'UkIcon',
        'daisyUI': 'DaisyUI',
        'DaisyUi': 'DaisyUI',
    }

    for typo, fix in typo_fixes.items():
        code_text = code_text.replace(typo, fix)

    return code_text.strip()

def parse_and_execute_component(code_text):
    """Parse and execute the generated component code, trusting LLM output."""
    try:
        # Ensure code_text is a string
        if not isinstance(code_text, str):
            code_text = str(code_text)

        # Clean up the code text
        code_text = code_text.strip()

        # Remove markdown code blocks if present
        if code_text.startswith('```'):
            lines = code_text.split('\n')
            # Remove first and last lines (markdown markers)
            if len(lines) > 2:
                code_text = '\n'.join(lines[1:-1])
            # Handle single-line code blocks
            elif len(lines) == 2:
                code_text = lines[1]
            else:
                code_text = code_text.replace('```', '')

        # Remove any leading/trailing whitespace
        code_text = code_text.strip()

        # Handle common LLM patterns - function definition with separate return
        lines = code_text.split('\n')
        if len(lines) > 1 and lines[-1].strip().startswith('return ') and lines[-1].strip().endswith('()'):
            # Extract function name from return statement
            return_line = lines[-1].strip()
            func_name = return_line.replace('return ', '').replace('()', '')
            # Remove the return line and add function call inside the function or after
            code_text = '\n'.join(lines[:-1])
            # Add the function call as a separate statement
            code_text += f'\n\nresult = {func_name}()'

        # Auto-repair common syntax issues
        code_text = auto_repair_syntax(code_text)

        # Basic syntax validation
        import ast
        try:
            ast.parse(code_text)
        except SyntaxError as syntax_error:
            print(f"Syntax error in generated code: {syntax_error}")
            raise syntax_error

        print(f"Executing code")

        # Determine if this is a simple expression or complex statement
        try:
            # Try to compile as an expression first
            compile(code_text, '<string>', 'eval')
            # If successful, it's a simple expression - use eval
            result = eval(code_text, globals())
            return result
        except SyntaxError:
            # If it fails, it's a complex statement - use exec
            pass

        # Try to parse and handle the final expression separately
        import ast

        try:
            parsed = ast.parse(code_text)
            statements = parsed.body

            if statements and isinstance(statements[-1], ast.Expr):
                # Last statement is an expression - this is likely our component
                # Execute all but the last statement, then eval the last one
                if len(statements) > 1:
                    # Execute function definitions and other statements
                    setup_code = ast.unparse(ast.Module(body=statements[:-1], type_ignores=[]))
                    exec(setup_code, globals())

                # Evaluate the final expression
                final_expr = ast.unparse(statements[-1].value)
                result = eval(final_expr, globals())
                return result
        except Exception as ast_error:
            print(f"AST parsing failed: {ast_error}, falling back to standard exec")

        # Fallback: Create a local namespace for execution
        local_namespace = {}

        # Execute the code directly with full access to imports
        exec(code_text, globals(), local_namespace)

        # Look for a return value in the local namespace
        # Check for functions that might have been defined
        functions = {k: v for k, v in local_namespace.items() if callable(v)}
        non_functions = {k: v for k, v in local_namespace.items() if not callable(v)}

        if 'result' in local_namespace:
            # Look for explicit result variable
            result = local_namespace['result']
        elif non_functions:
            # If there are non-function variables, use the last one
            result = list(non_functions.values())[-1]
        elif len(local_namespace) == 1:
            # If there's exactly one item, it's likely the result
            result = list(local_namespace.values())[0]
        else:
            # Look for FastHTML components (objects with __ft__ attribute)
            component_vars = [v for v in local_namespace.values() if hasattr(v, '__ft__') or hasattr(v, 'render')]
            if component_vars:
                result = component_vars[0]
            else:
                result = None

        if result is None:
            return Div(
                P("Code executed successfully but no component was returned", cls=TextPresets.muted_sm),
                P(f"Found {len(functions)} functions and {len(non_functions)} other variables in namespace", cls="text-xs text-gray-500"),
                cls="alert alert-info p-4 rounded-lg bg-info/10 border border-info/20"
            )

        return result

    except Exception as e:
        print(f"Error executing code: {e}")
        raise e


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
def ChatMessage(msg, user, **kwargs):
    bubble_class = "chat-bubble-primary" if user else 'chat-bubble-secondary'
    chat_class = "chat-end" if user else 'chat-start'
    return Div(cls=f"chat {chat_class}", **kwargs)(
               Div('user' if user else 'assistant', cls="chat-header"),
               Div(msg, cls=f"chat-bubble {bubble_class}"),
               Hidden(msg, name="messages")
           )

# Component message (renders generated UI components)
def ComponentMessage(component, context_msg="Generated interactive component", generation_info=None, **kwargs):
    content = [
        Div(component, cls="bg-base-100 rounded-lg border p-4 interactive-component")
    ]

    # Add generation information if provided
    if generation_info:
        info_display = Div(cls="mt-2 text-xs text-gray-500 flex gap-4")(
            Span(f"Generated in {generation_info['total_time']:.2f}s"),
            Span(f"{generation_info['tokens']} tokens")
        )
        content.append(info_display)

    return Div(cls="chat chat-start", **kwargs)(
        Div('assistant', cls="chat-header"),
        Div(cls="chat-bubble chat-bubble-secondary p-1")(*content),
        Hidden(context_msg, name="messages")
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
            P("Powered by FastHTML, MonsterUI & OpenRouter", cls="text-sm text-gray-600")
        )
    )