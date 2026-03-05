from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = FastAPI()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TextInput(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    text_length: int
    input_tokens: int
    output_tokens: int

class ExtractionResponse(BaseModel):
    action_items: list[str]
    key_decisions: list[str]
    input_tokens: int
    output_tokens: int

class CombinedResponse(BaseModel):
    summary: str
    action_items: list[str]
    key_decisions: list[str]
    summary_input_tokens: int
    summary_output_tokens: int
    extract_input_tokens: int
    extract_output_tokens: int

@app.post("/analyze-text")
async def analyze_text(input_data: TextInput):
    text = input_data.text
    print(f"Received text length: {len(text)} characters")
    
    return {
        "message": "Text received successfully",
        "text_length": len(text),
        "word_count": len(text.split())
    }

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(input_data: TextInput):
    text = input_data.text
    print(f"Summarizing text of length: {len(text)} characters")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise summaries of long texts. Focus on the main points and key information."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            temperature=0.5,
            frequency_penalty = 0.2,
            presence_penalty = 0,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        print(f"Summary generated: {len(summary)} characters, Input: {input_tokens}, Output: {output_tokens}")
        
        return {
            "summary": summary,
            "text_length": len(text),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract", response_model=ExtractionResponse)
async def extract_items(input_data: TextInput):
    summary = input_data.text
    print(f"Extracting from summary of length: {len(summary)} characters")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts action items and key decisions from text. Return the results in a structured format with clear bullet points."},
                {"role": "user", "content": f"""From the following summary, extract:
1. Action items (tasks that need to be done)
2. Key decisions (important decisions that were made or need to be made)

Summary:
{summary}

Format your response as:
ACTION ITEMS:
- item 1
- item 2

KEY DECISIONS:
- decision 1
- decision 2"""}
            ],
            temperature=0.3,
            frequency_penalty = 0,
            presence_penalty = 0,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        print(f"Extraction completed, Input: {input_tokens}, Output: {output_tokens}")
        
        # Parse the response
        action_items = []
        key_decisions = []
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'ACTION ITEMS' in line.upper():
                current_section = 'actions'
            elif 'KEY DECISIONS' in line.upper():
                current_section = 'decisions'
            elif line.startswith('-') or line.startswith('•'):
                item = line.lstrip('-•').strip()
                if item:
                    if current_section == 'actions':
                        action_items.append(item)
                    elif current_section == 'decisions':
                        key_decisions.append(item)
        
        return {
            "action_items": action_items,
            "key_decisions": key_decisions,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-combined", response_model=CombinedResponse)
async def analyze_combined(input_data: TextInput):
    text = input_data.text
    print(f"Combined analysis for text of length: {len(text)} characters")
    
    try:
        summary_task = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise summaries of long texts. Focus on the main points and key information."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            temperature=0.5,
            frequency_penalty = 0.2,
            presence_penalty = 0,
            max_tokens=500
        )
        
        summary_response = await summary_task
        summary = summary_response.choices[0].message.content
        summary_input_tokens = summary_response.usage.prompt_tokens
        summary_output_tokens = summary_response.usage.completion_tokens
        
        extract_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts action items and key decisions from text. Return the results in a structured format with clear bullet points."},
                {"role": "user", "content": f"""From the following summary, extract:
1. Action items (tasks that need to be done)
2. Key decisions (important decisions that were made or need to be made)

Summary:
{summary}

Format your response as:
ACTION ITEMS:
- item 1
- item 2

KEY DECISIONS:
- decision 1
- decision 2"""}
            ],
            temperature=0.3,
            frequency_penalty = 0,
            presence_penalty = 0,
            max_tokens=500
        )
        
        content = extract_response.choices[0].message.content
        extract_input_tokens = extract_response.usage.prompt_tokens
        extract_output_tokens = extract_response.usage.completion_tokens
        
        action_items = []
        key_decisions = []
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'ACTION ITEMS' in line.upper():
                current_section = 'actions'
            elif 'KEY DECISIONS' in line.upper():
                current_section = 'decisions'
            elif line.startswith('-') or line.startswith('•'):
                item = line.lstrip('-•').strip()
                if item:
                    if current_section == 'actions':
                        action_items.append(item)
                    elif current_section == 'decisions':
                        key_decisions.append(item)
        
        return {
            "summary": summary,
            "action_items": action_items,
            "key_decisions": key_decisions,
            "summary_input_tokens": summary_input_tokens,
            "summary_output_tokens": summary_output_tokens,
            "extract_input_tokens": extract_input_tokens,
            "extract_output_tokens": extract_output_tokens
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
