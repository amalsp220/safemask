"""Masking strategies for sensitive information."""
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional


class MaskingStrategy(Enum):
    """Available masking strategies."""
    ASTERISK = lambda x: '*' * len(x)
    HASH = lambda x: '#' * len(x)
    X = lambda x: 'X' * len(x)
    REDACT = lambda x: '[REDACTED]'
    PARTIAL = lambda x: x[:2] + '*' * (len(x) - 4) + x[-2:] if len(x) > 4 else '[MASKED]'
    FIRST_HALF = lambda x: '*' * (len(x) // 2) + x[len(x) // 2:]
    LAST_HALF = lambda x: x[:len(x) // 2] + '*' * (len(x) // 2)


class BaseMasker(ABC):
    """Base class for maskers."""
    
    def __init__(self, strategy: MaskingStrategy):
        self.strategy = strategy
    
    @abstractmethod
    def mask(self, text: str) -> str:
        """Mask sensitive information."""
        pass


class SimpleMasker(BaseMasker):
    """Simple masker using strategy function."""
    
    def mask(self, text: str) -> str:
        """Apply masking strategy to text."""
        return self.strategy.value(text)


class PatternMasker:
    """Main masker class for all patterns."""
    
    def __init__(self, strategy: MaskingStrategy = MaskingStrategy.ASTERISK):
        """Initialize masker with strategy."""
        self.strategy = strategy
        self.simple_masker = SimpleMasker(strategy)
    
    def mask_text(self, text: str, pattern_type: str) -> str:
        """Mask sensitive data in text by type."""
        if pattern_type == 'EMAIL':
            return self._mask_email(text)
        elif pattern_type == 'CREDIT_CARD':
            return self._mask_credit_card(text)
        elif pattern_type == 'PHONE':
            return self._mask_phone(text)
        elif pattern_type == 'SSN':
            return self._mask_ssn(text)
        elif pattern_type == 'PASSWORD':
            return self._mask_password(text)
        else:
            return self.simple_masker.mask(text)
    
    def _mask_email(self, email: str) -> str:
        """Mask email while preserving domain."""
        if '@' not in email:
            return self.simple_masker.mask(email)
        
        local, domain = email.split('@')
        masked_local = local[0] + '*' * (len(local) - 1)
        return f"{masked_local}@{domain}"
    
    def _mask_credit_card(self, card: str) -> str:
        """Mask credit card showing last 4 digits."""
        digits = re.sub(r'[\s-]', '', card)
        if len(digits) >= 4:
            return '*' * (len(digits) - 4) + digits[-4:]
        return self.simple_masker.mask(card)
    
    def _mask_phone(self, phone: str) -> str:
        """Mask phone showing last 4 digits."""
        digits = re.sub(r'[\s()-]', '', phone)
        if len(digits) >= 4:
            return '*' * (len(digits) - 4) + digits[-4:]
        return self.simple_masker.mask(phone)
    
    def _mask_ssn(self, ssn: str) -> str:
        """Mask SSN showing last 4 digits."""
        digits = ssn.replace('-', '')
        if len(digits) == 9:
            return '***-**-' + digits[-4:]
        return self.simple_masker.mask(ssn)
    
    def _mask_password(self, password: str) -> str:
        """Mask password completely."""
        return '[PASSWORD]'
    
    def mask_detections(self, text: str, detections: list) -> str:
        """Mask all detected sensitive information in text."""
        result = text
        
        # Sort detections by position (reverse to maintain indices)
        sorted_detections = sorted(detections, key=lambda x: x.start_pos, reverse=True)
        
        for detection in sorted_detections:
            masked = self.mask_text(detection.text, detection.pattern_type)
            result = result[:detection.start_pos] + masked + result[detection.end_pos:]
        
        return result
    
    def set_strategy(self, strategy: MaskingStrategy) -> None:
        """Change masking strategy."""
        self.strategy = strategy
        self.simple_masker = SimpleMasker(strategy)
