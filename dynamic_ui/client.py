from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME

def create_openai_client():
    """Create OpenAI client configured for OpenRouter"""
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )

def get_completion(client: OpenAI, messages: list, tools=None):
    """Get completion from OpenRouter using OpenAI client"""
    kwargs = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "extra_body": {
            "provider": {
                "sort": "throughput"
            }
        }
    }

    if tools:
        # Convert tools to OpenAI format if needed
        kwargs["tools"] = tools

    response = client.chat.completions.create(**kwargs)
    
    # Return both content and usage information
    usage = response.usage
    return {
        "content": response.choices[0].message.content,
        "tokens": {
            "prompt": usage.prompt_tokens if usage else 0,
            "completion": usage.completion_tokens if usage else 0,
            "total": usage.total_tokens if usage else 0
        }
    }