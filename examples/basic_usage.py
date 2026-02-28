#!/usr/bin/env python3
"""Basic usage example for SafeMask library."""

from safemask.detectors import PatternDetectors
from safemask.validators import PatternValidator
from safemask.maskers import PatternMasker, MaskingStrategy


def main():
    """Demonstrate basic SafeMask functionality."""
    
    # Sample text with sensitive information
    text = (
        "User Details:\n"
        "Email: john.doe@example.com\n"
        "Phone: +1 (555) 123-4567\n"
        "Credit Card: 4532-0151-1283-0366\n"
        "SSN: 123-45-6789\n"
        "API Key: sk_live_abc123def456ghi789jkl"
    )
    
    print("=" * 60)
    print("Original Text:")
    print("=" * 60)
    print(text)
    print()
    
    # Initialize components
    detectors = PatternDetectors()
    validator = PatternValidator()
    masker = PatternMasker(strategy=MaskingStrategy.ASTERISK)
    
    # Detect all sensitive information
    print("=" * 60)
    print("Detected Sensitive Information:")
    print("=" * 60)
    detections = detectors.detect_all(text)
    
    for detection in detections:
        print(f"Type: {detection.pattern_type}")
        print(f"Value: {detection.text}")
        print(f"Position: {detection.start_pos}-{detection.end_pos}")
        print()
    
    # Validate specific patterns
    print("=" * 60)
    print("Validation Results:")
    print("=" * 60)
    
    email = "john.doe@example.com"
    is_valid_email = validator.validate_email(email)
    print(f"Email '{email}' is valid: {is_valid_email}")
    
    card = "4532-0151-1283-0366"
    is_valid_card = validator.validate_credit_card(card)
    print(f"Credit card '{card}' is valid (Luhn): {is_valid_card}")
    
    ssn = "123-45-6789"
    is_valid_ssn = validator.validate_ssn(ssn)
    print(f"SSN '{ssn}' is valid: {is_valid_ssn}")
    print()
    
    # Mask sensitive information
    print("=" * 60)
    print("Masked Text (Asterisk Strategy):")
    print("=" * 60)
    masked_text = masker.mask_detections(text, detections)
    print(masked_text)
    print()
    
    # Try different masking strategies
    print("=" * 60)
    print("Different Masking Strategies:")
    print("=" * 60)
    
    strategies = [
        MaskingStrategy.HASH,
        MaskingStrategy.REDACT,
        MaskingStrategy.PARTIAL,
    ]
    
    for strategy in strategies:
        masker.set_strategy(strategy)
        masked = masker.mask_detections(text, detections)
        print(f"\n{strategy.name} Strategy:")
        print(masked)


if __name__ == "__main__":
    main()
