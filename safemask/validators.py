"""Validators for sensitive information patterns."""
import re
from abc import ABC, abstractmethod
from typing import Callable


class BaseValidator(ABC):
    """Base class for validators."""
    
    @abstractmethod
    def validate(self, text: str) -> bool:
        """Validate if text matches pattern."""
        pass


class LuhnValidator(BaseValidator):
    """Validates credit card numbers using Luhn algorithm."""
    
    def validate(self, text: str) -> bool:
        """Check if credit card passes Luhn validation."""
        # Remove spaces and dashes
        digits = re.sub(r'[\s-]', '', text)
        
        # Only digits
        if not digits.isdigit() or len(digits) < 13 or len(digits) > 19:
            return False
        
        # Luhn algorithm
        def luhn_sum(num_str: str) -> int:
            total = 0
            for i, digit in enumerate(reversed(num_str)):
                n = int(digit)
                if i % 2 == 1:
                    n *= 2
                    if n > 9:
                        n -= 9
                total += n
            return total
        
        return luhn_sum(digits) % 10 == 0


class EmailValidator(BaseValidator):
    """Validates email addresses."""
    
    def validate(self, text: str) -> bool:
        """Check if email is valid."""
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return bool(re.match(pattern, text))


class SSNValidator(BaseValidator):
    """Validates US Social Security Numbers."""
    
    def validate(self, text: str) -> bool:
        """Check if SSN is valid."""
        # SSN format: XXX-XX-XXXX
        if not re.match(r'^\d{3}-\d{2}-\d{4}$', text):
            return False
        
        # Check for invalid patterns
        parts = text.split('-')
        if parts[0] == '000' or parts[0] == '666' or int(parts[0]) >= 900:
            return False
        if parts[1] == '00':
            return False
        if parts[2] == '0000':
            return False
        
        return True


class PatternValidator:
    """Main validator class."""
    
    def __init__(self):
        """Initialize validators."""
        self.luhn_validator = LuhnValidator()
        self.email_validator = EmailValidator()
        self.ssn_validator = SSNValidator()
    
    def validate_credit_card(self, text: str) -> bool:
        """Validate credit card."""
        return self.luhn_validator.validate(text)
    
    def validate_email(self, text: str) -> bool:
        """Validate email."""
        return self.email_validator.validate(text)
    
    def validate_ssn(self, text: str) -> bool:
        """Validate SSN."""
        return self.ssn_validator.validate(text)
    
    def validate_pattern(self, text: str, pattern_type: str) -> bool:
        """Validate pattern by type."""
        validators = {
            'CREDIT_CARD': self.validate_credit_card,
            'EMAIL': self.validate_email,
            'SSN': self.validate_ssn,
        }
        
        validator = validators.get(pattern_type)
        return validator(text) if validator else True
