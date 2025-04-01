from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    text: str

class ContentIssue(BaseModel):
    type: str
    description: str
    start: int
    end: int
    suggestion: str

class ContentResponse(BaseModel):
    issues: List[ContentIssue]
    improved_text: str

def check_passive_voice(text: str) -> List[ContentIssue]:
    # Simple passive voice detection (can be expanded)
    passive_patterns = [
        r'\b(?:am|is|are|was|were|be|been|being)\s+\w+ed\b',
        r'\b(?:has|have|had)\s+been\s+\w+ed\b'
    ]
    issues = []
    
    for pattern in passive_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            issues.append(ContentIssue(
                type="passive_voice",
                description="Use active voice instead of passive voice",
                start=match.start(),
                end=match.end(),
                suggestion="Consider restructuring to use active voice"
            ))
    return issues

def check_abbreviations(text: str) -> List[ContentIssue]:
    # Check for undefined abbreviations
    abbreviation_pattern = r'\b[A-Z]{2,}\b'
    issues = []
    
    for match in re.finditer(abbreviation_pattern, text):
        abbr = match.group()
        if abbr not in ["US", "VA", "FAQ"]:  # Common acceptable abbreviations
            issues.append(ContentIssue(
                type="abbreviation",
                description=f"Define {abbr} on first use",
                start=match.start(),
                end=match.end(),
                suggestion=f"Spell out {abbr} on first use"
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
                suggestion=f"Replace with '{suggestion}'"
            ))
    return issues

def check_contractions(text: str) -> List[ContentIssue]:
    # VA.gov encourages contractions
    no_contraction_patterns = {
        r'\b(?:do not|cannot|will not|should not)\b': {
            "do not": "don't",
            "cannot": "can't",
            "will not": "won't",
            "should not": "shouldn't"
        }
    }
    issues = []
    
    for pattern, replacements in no_contraction_patterns.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            found = match.group().lower()
            issues.append(ContentIssue(
                type="contraction",
                description="Use contractions to make content more conversational",
                start=match.start(),
                end=match.end(),
                suggestion=f"Use '{replacements[found]}'"
            ))
    return issues

@app.post("/analyze", response_model=ContentResponse)
async def analyze_content(request: ContentRequest):
    text = request.text
    issues = []
    
    # Run all checks
    issues.extend(check_passive_voice(text))
    issues.extend(check_abbreviations(text))
    issues.extend(check_complex_words(text))
    issues.extend(check_contractions(text))
    
    # Create improved text (simple version - can be enhanced)
    improved_text = text
    for issue in sorted(issues, key=lambda x: x.start, reverse=True):
        if issue.type in ["complex_word", "contraction"]:
            improved_text = improved_text[:issue.start] + issue.suggestion.split("'")[1] + improved_text[issue.end:]
    
    return ContentResponse(issues=issues, improved_text=improved_text) 