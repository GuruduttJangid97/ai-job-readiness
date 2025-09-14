"""
Text processing and validation utilities for AI Job Readiness Platform

This module provides utilities for text processing, cleaning, and validation
that are used throughout the application.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import re
import unicodedata
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse
import phonenumbers
from phonenumbers import NumberParseException


def clean_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Clean and normalize text by removing extra whitespace and normalizing unicode.
    
    Args:
        text: Text to clean
        max_length: Maximum length to truncate to
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Truncate if max_length is specified
    if max_length and len(text) > max_length:
        text = text[:max_length].rstrip()
    
    return text


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text by splitting on common delimiters.
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length
        
    Returns:
        List[str]: List of unique keywords
    """
    if not text:
        return []
    
    # Split on common delimiters
    keywords = re.split(r'[,\s;|&]+', text.lower())
    
    # Clean and filter keywords
    keywords = [
        clean_text(keyword) 
        for keyword in keywords 
        if clean_text(keyword) and len(clean_text(keyword)) >= min_length
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str, country_code: str = "US") -> bool:
    """
    Validate phone number format using phonenumbers library.
    
    Args:
        phone: Phone number to validate
        country_code: Country code for validation (default: US)
        
    Returns:
        bool: True if phone is valid, False otherwise
    """
    if not phone:
        return False
    
    try:
        parsed_number = phonenumbers.parse(phone, country_code)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    if not url:
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def slugify(text: str, max_length: int = 50) -> str:
    """
    Convert text to URL-friendly slug.
    
    Args:
        text: Text to slugify
        max_length: Maximum length of the slug
        
    Returns:
        str: URL-friendly slug
    """
    if not text:
        return ""
    
    # Convert to lowercase and normalize unicode
    slug = unicodedata.normalize('NFKD', text.lower())
    
    # Remove non-alphanumeric characters except spaces and hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    
    # Replace spaces and multiple hyphens with single hyphen
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Truncate to max_length
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    
    return slug


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract skills from text using common skill patterns.
    
    Args:
        text: Text to extract skills from
        
    Returns:
        List[str]: List of potential skills
    """
    if not text:
        return []
    
    # Common skill patterns (case insensitive)
    skill_patterns = [
        r'\b(?:python|java|javascript|typescript|react|angular|vue)\b',
        r'\b(?:sql|mysql|postgresql|mongodb|redis)\b',
        r'\b(?:docker|kubernetes|aws|azure|gcp)\b',
        r'\b(?:git|github|gitlab|jenkins|ci/cd)\b',
        r'\b(?:machine learning|ml|ai|artificial intelligence)\b',
        r'\b(?:data science|analytics|statistics)\b',
        r'\b(?:project management|agile|scrum)\b',
        r'\b(?:leadership|team management|mentoring)\b',
    ]
    
    skills = set()
    text_lower = text.lower()
    
    for pattern in skill_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        skills.update(matches)
    
    return list(skills)


def extract_experience_years(text: str) -> Optional[float]:
    """
    Extract years of experience from text.
    
    Args:
        text: Text to extract experience from
        
    Returns:
        Optional[float]: Years of experience or None if not found
    """
    if not text:
        return None
    
    # Patterns for years of experience
    patterns = [
        r'(\d+(?:\.\d+)?)\s*years?\s*(?:of\s*)?experience',
        r'(\d+(?:\.\d+)?)\s*years?\s*in\s*(?:the\s*)?field',
        r'(\d+(?:\.\d+)?)\s*years?\s*working',
        r'(\d+(?:\.\d+)?)\s*years?\s*professional',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue
    
    return None


def extract_education_level(text: str) -> Optional[str]:
    """
    Extract education level from text.
    
    Args:
        text: Text to extract education from
        
    Returns:
        Optional[str]: Education level or None if not found
    """
    if not text:
        return None
    
    # Education level patterns
    education_levels = [
        ("PhD", r'\b(?:phd|doctorate|doctor\s*of\s*philosophy)\b'),
        ("Master's Degree", r'\b(?:master|m\.?s\.?|m\.?a\.?|mba|m\.?e\.?d\.?)\b'),
        ("Bachelor's Degree", r'\b(?:bachelor|b\.?s\.?|b\.?a\.?|b\.?e\.?|b\.?tech)\b'),
        ("Associate's Degree", r'\b(?:associate|a\.?a\.?|a\.?s\.?)\b'),
        ("High School", r'\b(?:high\s*school|secondary\s*school|diploma)\b'),
    ]
    
    text_lower = text.lower()
    
    for level, pattern in education_levels:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return level
    
    return None


def clean_html(html_text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        html_text: HTML text to clean
        
    Returns:
        str: Plain text without HTML tags
    """
    if not html_text:
        return ""
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', html_text)
    
    # Decode HTML entities
    html_entities = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&nbsp;': ' ',
    }
    
    for entity, char in html_entities.items():
        clean_text = clean_text.replace(entity, char)
    
    return clean_text.strip()


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to specified length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncating
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def extract_contact_info(text: str) -> Dict[str, List[str]]:
    """
    Extract contact information from text.
    
    Args:
        text: Text to extract contact info from
        
    Returns:
        Dict[str, List[str]]: Dictionary with extracted contact information
    """
    if not text:
        return {"emails": [], "phones": [], "urls": []}
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    # Phone pattern (basic)
    phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
    phones = re.findall(phone_pattern, text)
    phones = [f"({match[0]}) {match[1]}-{match[2]}" for match in phones]
    
    # URL pattern
    url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
    urls = re.findall(url_pattern, text)
    
    return {
        "emails": list(set(emails)),
        "phones": list(set(phones)),
        "urls": list(set(urls))
    }
