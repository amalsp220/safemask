"""Pattern detectors for sensitive information."""
import re
from abc import ABC, abstractmethod
from typing import List, Tuple, Pattern
from dataclasses import dataclass


@dataclass
class Detection:
    """Represents a detected sensitive pattern."""
    text: str
    pattern_type: str
    start_pos: int
    end_pos: int
    confidence: float = 0.95


class BaseDetector(ABC):
    """Base class for pattern detectors."""
    
    def __init__(self, pattern: Pattern, pattern_type: str):
        self.pattern = pattern
        self.pattern_type = pattern_type
    
    @abstractmethod
    def detect(self, text: str) -> List[Detection]:
        """Detect pattern in text."""
        pass


class RegexDetector(BaseDetector):
    """Detects patterns using regex."""
    
    def detect(self, text: str) -> List[Detection]:
        """Find all regex matches in text."""
        detections = []
        for match in self.pattern.finditer(text):
            detections.append(
                Detection(
                    text=match.group(),
                    pattern_type=self.pattern_type,
                    start_pos=match.start(),
                    end_pos=match.end(),
                )
            )
        return detections


class PatternDetectors:
    """Main detector class for all sensitive information patterns."""
    
    def __init__(self):
        """Initialize detectors for all sensitive pattern types."""
        # Aadhaar: 12 digits with optional spaces
        self.aadhaar = RegexDetector(
            re.compile(r'\d{4}\s?\d{4}\s?\d{4}'),
            'AADHAAR'
        )
        
        # PAN: AAAAA9999A format
        self.pan = RegexDetector(
            re.compile(r'[A-Z]{5}[0-9]{4}[A-Z]{1}'),
            'PAN'
        )
        
        # Passport: Pattern 1-3 letters followed by 6-9 digits
        self.passport = RegexDetector(
            re.compile(r'[A-Z]{1,3}\d{6,9}'),
            'PASSPORT'
        )
        
        # Voter ID: Format with alphanumeric
        self.voter_id = RegexDetector(
            re.compile(r'[A-Z]{3}\d{7}'),
            'VOTER_ID'
        )
        
        # Driving License: State code + digits
        self.driving_license = RegexDetector(
            re.compile(r'[A-Z]{2}\d{13}'),
            'DRIVING_LICENSE'
        )
        
        # Credit Card: 13-19 digits with optional spaces/dashes
        self.credit_card = RegexDetector(
            re.compile(r'\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{3,4}'),
            'CREDIT_CARD'
        )
        
        # Email addresses
        self.email = RegexDetector(
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'EMAIL'
        )
        
        # Phone numbers: Multiple formats
        self.phone = RegexDetector(
            re.compile(r'(?:\+\d{1,3})?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'),
            'PHONE'
        )
        
        # SSN: XXX-XX-XXXX format
        self.ssn = RegexDetector(
            re.compile(r'\d{3}-\d{2}-\d{4}'),
            'SSN'
        )
        
        # API Keys: Common patterns
        self.api_key = RegexDetector(
            re.compile(r'(?:api[_-]?)?key[\s:=]+([\w\-]{20,})', re.IGNORECASE),
            'API_KEY'
        )
        
        # AWS Secret Key
        self.aws_secret = RegexDetector(
            re.compile(r'aws_secret_access_key[\s:=]+([\w/+=]{40})'),
            'AWS_SECRET'
        )
        
        # Private Key
        self.private_key = RegexDetector(
            re.compile(r'-----BEGIN (RSA|DSA|EC|PGP)?\s?PRIVATE KEY-----'),
            'PRIVATE_KEY'
        )
        
        # Password patterns
        self.password = RegexDetector(
            re.compile(r'["\']?(?:password|passwd)["\']?[\s:=]+["\']?([^\s"\'\']{6,})["\']?', re.IGNORECASE),
            'PASSWORD'
        )
        
        # IPv4 addresses
        self.ipv4 = RegexDetector(
            re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            'IPV4'
        )
        
        # URLs
        self.url = RegexDetector(
            re.compile(r'https?://[^\s]+'),
            'URL'
        )
    
    def detect_all(self, text: str) -> List[Detection]:
        """Detect all sensitive patterns in text."""
        detections = []
        
        detections.extend(self.aadhaar.detect(text))
        detections.extend(self.pan.detect(text))
        detections.extend(self.passport.detect(text))
        detections.extend(self.voter_id.detect(text))
        detections.extend(self.driving_license.detect(text))
        detections.extend(self.credit_card.detect(text))
        detections.extend(self.email.detect(text))
        detections.extend(self.phone.detect(text))
        detections.extend(self.ssn.detect(text))
        detections.extend(self.api_key.detect(text))
        detections.extend(self.aws_secret.detect(text))
        detections.extend(self.private_key.detect(text))
        detections.extend(self.password.detect(text))
        detections.extend(self.ipv4.detect(text))
        detections.extend(self.url.detect(text))
        
        return detections
    
    def detect_by_type(self, text: str, pattern_type: str) -> List[Detection]:
        """Detect specific pattern type."""
        detector_map = {
            'AADHAAR': self.aadhaar,
            'PAN': self.pan,
            'PASSPORT': self.passport,
            'VOTER_ID': self.voter_id,
            'DRIVING_LICENSE': self.driving_license,
            'CREDIT_CARD': self.credit_card,
            'EMAIL': self.email,
            'PHONE': self.phone,
            'SSN': self.ssn,
            'API_KEY': self.api_key,
            'AWS_SECRET': self.aws_secret,
            'PRIVATE_KEY': self.private_key,
            'PASSWORD': self.password,
            'IPV4': self.ipv4,
            'URL': self.url,
        }
        detector = detector_map.get(pattern_type)
        return detector.detect(text) if detector else []
