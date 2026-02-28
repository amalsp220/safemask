"""Tests for validators module."""
import pytest
from safemask.validators import PatternValidator, LuhnValidator


class TestLuhnValidator:
    """Test suite for Luhn validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = LuhnValidator()
    
    def test_valid_credit_card(self):
        """Test valid credit card numbers."""
        valid_cards = [
            "4532015112830366",  # Visa
            "5425233010103442",  # MasterCard
            "378282246310005",   # American Express
        ]
        for card in valid_cards:
            assert self.validator.validate(card)
    
    def test_invalid_credit_card(self):
        """Test invalid credit card numbers."""
        invalid_cards = [
            "1234567890123456",
            "0000000000000000",
            "4532015112830367",  # Invalid checksum
        ]
        for card in invalid_cards:
            assert not self.validator.validate(card)
    
    def test_formatted_credit_card(self):
        """Test credit card with formatting."""
        assert self.validator.validate("4532-0151-1283-0366")
        assert self.validator.validate("4532 0151 1283 0366")


class TestEmailValidator:
    """Test suite for email validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = PatternValidator()
    
    def test_valid_email(self):
        """Test valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@example.co.uk",
            "user+tag@example.com",
            "123@example.com",
        ]
        for email in valid_emails:
            assert self.validator.validate_email(email)
    
    def test_invalid_email(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "invalid.email",
            "@example.com",
            "user@",
            "user @example.com",
        ]
        for email in invalid_emails:
            assert not self.validator.validate_email(email)


class TestSSNValidator:
    """Test suite for SSN validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = PatternValidator()
    
    def test_valid_ssn(self):
        """Test valid SSN formats."""
        valid_ssns = [
            "123-45-6789",
            "987-65-4321",
        ]
        for ssn in valid_ssns:
            assert self.validator.validate_ssn(ssn)
    
    def test_invalid_ssn_format(self):
        """Test invalid SSN formats."""
        invalid_ssns = [
            "12345678",
            "123-45-678",
            "123456789",
        ]
        for ssn in invalid_ssns:
            assert not self.validator.validate_ssn(ssn)
    
    def test_invalid_ssn_values(self):
        """Test SSN with invalid values."""
        # Area number 000
        assert not self.validator.validate_ssn("000-45-6789")
        # Area number 666
        assert not self.validator.validate_ssn("666-45-6789")
        # Area number 900+
        assert not self.validator.validate_ssn("900-45-6789")
        # Group number 00
        assert not self.validator.validate_ssn("123-00-6789")
        # Serial number 0000
        assert not self.validator.validate_ssn("123-45-0000")


class TestPatternValidator:
    """Test suite for PatternValidator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = PatternValidator()
    
    def test_validate_pattern_by_type(self):
        """Test validate_pattern method."""
        # Credit card
        assert self.validator.validate_pattern(
            "4532-0151-1283-0366", "CREDIT_CARD"
        )
        # Email
        assert self.validator.validate_pattern(
            "test@example.com", "EMAIL"
        )
        # Unknown type defaults to True
        assert self.validator.validate_pattern(
            "anything", "UNKNOWN_TYPE"
        )
