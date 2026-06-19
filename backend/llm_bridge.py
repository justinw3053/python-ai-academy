import json
import os

# We would import ollama here, but since the target env has it and our test env might not,
# we structure the generator to wrap the calls.

def stream_chat(message, context):
    """
    Streams the response from the local Ollama daemon using SSE format.
    """
    try:
        import ollama
    except ImportError:
        # Fallback for local testing without ollama installed
        yield "data: Ollama not installed locally, but SSE works.\n\n"
        yield "event: done\ndata: \n\n"
        return

    # In production, we read the prompt from SYSTEM.md
    system_prompt = "You are Pi Agent..." 
    
    messages = [
        {'role': 'system', 'content': f"{system_prompt}\nContext: {context}"},
        {'role': 'user', 'content': message}
    ]
    
    try:
        stream = ollama.chat(
            model='gemma4:e4b',
            messages=messages,
            stream=True,
        )
        
        for chunk in stream:
            content = chunk['message']['content']
            # SSE format requires formatting and replacing newlines
            formatted_content = content.replace('\n', '\\n')
            yield f"data: {formatted_content}\n\n"
            
        yield "event: done\ndata: \n\n"
        
    except Exception as e:
        yield f"data: [COMM LINK ERROR] {str(e)}\n\n"
        yield "event: done\ndata: \n\n"
