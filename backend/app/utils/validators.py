"""
Input validation utilities
"""
from typing import Optional
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    # Check if it's all digits and reasonable length
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15

def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))

def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize user input text"""
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()

def is_valid_answer(text: str, min_words: int = 5) -> bool:
    """Check if answer is valid (not too short or nonsense)"""
    if not text or len(text.strip()) == 0:
        return False
    
    words = text.split()
    if len(words) < min_words:
        return False
    
    # Check for nonsense (e.g., repeated characters)
    if len(set(text.replace(' ', ''))) < 3:
        return False
    
    return True

def detect_profanity(text: str) -> bool:
    """Basic profanity detection (expandable)"""
    # Basic list - expand as needed
    profanity_list = ['badword1', 'badword2']  # Add actual words as needed
    text_lower = text.lower()
    return any(word in text_lower for word in profanity_list)
