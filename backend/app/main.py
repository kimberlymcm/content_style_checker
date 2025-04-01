from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import re
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class ContentRequest(BaseModel):
    text: str
    use_llm: bool = False
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "The form cannot be utilized until it has been completed by the applicant.",
                    "use_llm": True
                }
            ]
        }
    }

class ContentIssue(BaseModel):
    type: str
    description: str
    start: int
    end: int
    suggestion: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "complex_word",
                    "description": "Use simpler language",
                    "start": 0,
                    "end": 10,
                    "suggestion": "use"
                }
            ]
        }
    }

class ContentResponse(BaseModel):
    issues: List[ContentIssue]
    improved_text: str
    llm_details: Optional[Dict[str, str]] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "issues": [],
                    "improved_text": "The form can't be used until the applicant completed it.",
                    "llm_details": None
                }
            ]
        }
    }

def check_passive_voice(text: str) -> List[ContentIssue]:
    # Enhanced passive voice detection with better suggestions
    passive_patterns = [
        (r'\b(?:am|is|are|was|were)\s+being\s+(\w+ed)\b', "being"),  # Continuous passive
        (r'\b(?:has|have|had)\s+been\s+(\w+ed)\b', "have been"),  # Perfect passive
        (r'\b(?:am|is|are|was|were)\s+(\w+ed)\b', "is")  # Simple past passive
    ]
    issues = []
    
    for pattern, aux in passive_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            verb = match.group(1)
            if "by" in text[match.end():].split(".")[0]:
                # If there's a "by" phrase, we can make a better suggestion
                by_phrase = text[match.end():].split(".")[0]
                actor = by_phrase[by_phrase.find("by")+3:].strip().split()[0]
                suggestion = f"{actor} {verb}"
            else:
                suggestion = f"someone {verb}"
            
            issues.append(ContentIssue(
                type="passive_voice",
                description="Use active voice instead of passive voice",
                start=match.start(),
                end=match.end(),
                suggestion=suggestion
            ))
    return issues

def check_abbreviations(text: str) -> List[ContentIssue]:
    # Common acceptable abbreviations that don't need expansion
    common_abbr = {
        "US": "US",  # Acceptable as is
        "VA": "VA",  # Acceptable as is
        "FAQ": "FAQ"  # Acceptable as is
    }
    
    # Terms that should be replaced with plain language
    plain_language_terms = {
        "VADSEB": "VA education benefits for dependents and spouses",
        "VTP": "Veterans transportation program",
        "VTS": "Veterans transportation service",
        "BT": "travel reimbursement",
        "HRTG": "rural transportation grants",
        "SMT": "special transportation",
        "OJT": "on-the-job training",
        "DMDC": "Defense Manpower Data Center",
        "CIA": "Central Intelligence Agency",
        "FBI": "Federal Bureau of Investigation"
    }
    
    issues = []
    
    # First check for parenthetical acronyms that should be removed entirely
    pattern = r'\b[A-Za-z- ]+\s*\([A-Z]+\)'
    for match in re.finditer(pattern, text):
        full_phrase = match.group(0)
        # Extract the acronym
        acronym = re.search(r'\(([A-Z]+)\)', full_phrase).group(1)
        # Get the descriptive part before the acronym
        main_phrase = re.sub(r'\s*\([A-Z]+\)', '', full_phrase)
        
        # If we have a plain language replacement, use it
        if acronym in plain_language_terms:
            suggestion = plain_language_terms[acronym]
        else:
            # If no specific replacement, just use the main phrase in lowercase
            suggestion = main_phrase.lower()
            
        issues.append(ContentIssue(
            type="abbreviation",
            description="Use plain language without acronyms",
            start=match.start(),
            end=match.end(),
            suggestion=suggestion
        ))
    
    # Then check for standalone acronyms
    for match in re.finditer(r'\b[A-Z]{2,}\b', text):
        abbr = match.group()
        if abbr in plain_language_terms and abbr not in common_abbr:
            issues.append(ContentIssue(
                type="abbreviation",
                description="Use plain language instead of acronyms",
                start=match.start(),
                end=match.end(),
                suggestion=plain_language_terms[abbr]
            ))
    
    return issues

def check_complex_words(text: str) -> List[ContentIssue]:
    complex_words = {
        "utilize": "use",
        "implement": "start",
        "facilitate": "help",
        "leverage": "use",
        "commence": "begin",
        "terminate": "end",
    }
    issues = []
    
    for word, suggestion in complex_words.items():
        for match in re.finditer(r'\b' + word + r'\b', text, re.IGNORECASE):
            issues.append(ContentIssue(
                type="complex_word",
                description=f"Use simpler language",
                start=match.start(),
                end=match.end(),
                suggestion=suggestion
            ))
    return issues

def check_contractions(text: str) -> List[ContentIssue]:
    # Enhanced contractions with more patterns
    no_contraction_patterns = {
        "do not": "don't",
        "cannot": "can't",
        "will not": "won't",
        "should not": "shouldn't",
        "is not": "isn't",
        "are not": "aren't",
        "have not": "haven't",
        "has not": "hasn't"
    }
    issues = []
    
    for phrase, contraction in no_contraction_patterns.items():
        for match in re.finditer(r'\b' + re.escape(phrase) + r'\b', text, re.IGNORECASE):
            issues.append(ContentIssue(
                type="contraction",
                description="Use contractions to make content more conversational",
                start=match.start(),
                end=match.end(),
                suggestion=contraction
            ))
    return issues

def apply_non_overlapping_fixes(text: str, issues: List[ContentIssue]) -> str:
    # Sort issues by priority and position
    priority_order = {"complex_word": 0, "contraction": 1, "abbreviation": 2, "passive_voice": 3}
    sorted_issues = sorted(issues, key=lambda x: (priority_order[x.type], -x.end))  # Sort by priority and reverse position
    
    # Create a list of non-overlapping changes
    changes = []
    for issue in sorted_issues:
        # Skip passive voice suggestions that don't have a specific actor
        if issue.type == "passive_voice" and issue.suggestion.startswith("someone"):
            continue
        
        # Check if this change overlaps with any accepted changes
        overlaps = False
        for accepted in changes:
            if (issue.start < accepted[1] and issue.end > accepted[0]):
                overlaps = True
                break
        
        if not overlaps:
            changes.append((issue.start, issue.end, issue.suggestion))
    
    # Sort changes by position in reverse order (to apply from end to start)
    changes.sort(key=lambda x: -x[0])
    
    # Apply changes
    result = text
    for start, end, suggestion in changes:
        result = result[:start] + suggestion + result[end:]
    
    return result

def improve_with_llm(text: str) -> tuple[str, List[ContentIssue], Dict[str, str]]:
    """Use LLM to improve text according to VA.gov style guide."""
    if not openai.api_key:
        return text, [], None
        
    prompt = """You are a VA.gov content specialist. Improve the following text according to VA.gov content style guidelines.

Key style rules to follow:

Content Voice and Tone:
- Address Veterans directly using "you"
- Use "we" when referring to VA
- Be direct, confident, and empathetic
- Use conversational language while maintaining professionalism

Plain Language Requirements:
- Use simple, everyday words
- Avoid jargon, technical terms, and bureaucratic language
- Keep sentences short and clear
- Break complex information into digestible chunks
- Use active voice
- Use contractions to be conversational (e.g., "can't" instead of "cannot")

Abbreviations and Acronyms:
- Spell out abbreviations on first use
- Don't create new acronyms
- Use plain language labels instead of program names
- Only use acronyms that are widely known by Veterans

Formatting and Structure:
- Use proper capitalization (don't capitalize generic terms)
- Format dates as Month DD, YYYY
- Format phone numbers as 000-000-0000
- Use serial commas
- Use numerals for numbers

Original text:
{text}

Please provide:
1. The improved text that follows all VA.gov guidelines
2. A list of specific changes made and why they align with VA.gov style
"""
    
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert VA.gov content specialist who ensures all content follows VA style guidelines perfectly."},
                {"role": "user", "content": prompt.format(text=text)}
            ],
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        parts = result.split("\n\n")
        improved_text = parts[0]
        
        issues = []
        for change in parts[1:]:
            if ":" in change:
                description, suggestion = change.split(":", 1)
                issues.append(ContentIssue(
                    type="style_improvement",
                    description=description.strip(),
                    start=0,
                    end=0,
                    suggestion=suggestion.strip()
                ))
        
        llm_details = {
            "prompt": prompt.format(text=text),
            "response": result,
            "model": "gpt-4"
        }
        
        return improved_text, issues, llm_details
        
    except Exception as e:
        print(f"LLM error: {e}")
        return text, [], None

@app.post("/analyze", response_model=ContentResponse)
async def analyze_content(request: ContentRequest):
    text = request.text
    issues = []
    llm_details = None
    
    if request.use_llm and openai.api_key:
        # Try LLM-based improvement first
        improved_text, llm_issues, llm_details = improve_with_llm(text)
        issues.extend(llm_issues)
        
        if improved_text != text:  # If LLM made changes
            return ContentResponse(
                issues=issues, 
                improved_text=improved_text,
                llm_details=llm_details
            )
    
    # Fallback to rule-based checks if LLM not used or failed
    issues.extend(check_complex_words(text))
    issues.extend(check_contractions(text))
    issues.extend(check_abbreviations(text))
    issues.extend(check_passive_voice(text))
    
    improved_text = apply_non_overlapping_fixes(text, issues)
    return ContentResponse(
        issues=issues, 
        improved_text=improved_text,
        llm_details=llm_details
    ) 