"""Tests for maskers module."""
import pytest
from safemask.maskers import PatternMasker, MaskingStrategy
from safemask.detectors import Detection


class TestPatternMasker:
    """Test suite for PatternMasker."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.masker = PatternMasker(strategy=MaskingStrategy.ASTERISK)
    
    def test_mask_email(self):
        """Test email masking."""
        email = "john.doe@example.com"
        masked = self.masker.mask_text(email, "EMAIL")
        assert "@example.com" in masked
        assert "john" not in masked or masked.count('*') > 0
    
    def test_mask_credit_card(self):
        """Test credit card masking."""
        card = "4532015112830366"
        masked = self.masker.mask_text(card, "CREDIT_CARD")
        assert "0366" in masked  # Last 4 digits preserved
        assert masked.count('*') > 0
    
    def test_mask_phone(self):
        """Test phone masking."""
        phone = "5551234567"
        masked = self.masker.mask_text(phone, "PHONE")
        assert "4567" in masked  # Last 4 digits
        assert masked.count('*') > 0
    
    def test_mask_ssn(self):
        """Test SSN masking."""
        ssn = "123-45-6789"
        masked = self.masker.mask_text(ssn, "SSN")
        assert "6789" in masked
        assert "***" in masked
    
    def test_mask_password(self):
        """Test password masking."""
        password = "SecurePassword123!"
        masked = self.masker.mask_text(password, "PASSWORD")
        assert masked == "[PASSWORD]"
    
    def test_mask_generic(self):
        """Test generic masking."""
        text = "SensitiveData"
        masked = self.masker.mask_text(text, "GENERIC")
        assert masked == "*" * len(text)
    
    def test_mask_detections(self):
        """Test masking multiple detections."""
        text = "Email: test@example.com, Phone: 5551234567"
        detections = [
            Detection(
                text="test@example.com",
                pattern_type="EMAIL",
                start_pos=7,
                end_pos=24,
            ),
            Detection(
                text="5551234567",
                pattern_type="PHONE",
                start_pos=35,
                end_pos=45,
            ),
        ]
        masked = self.masker.mask_detections(text, detections)
        assert "test@example.com" not in masked or "*" in masked
        assert "5551234567" not in masked or "*" in masked


class TestMaskingStrategy:
    """Test suite for MaskingStrategy."""
    
    def test_asterisk_strategy(self):
        """Test asterisk masking strategy."""
        text = "secret"
        masked = MaskingStrategy.ASTERISK.value(text)
        assert masked == "****** 
    
    def test_hash_strategy(self):
        """Test hash masking strategy."""
        text = "secret"
        masked = MaskingStrategy.HASH.value(text)
        assert masked == "######"
    
    def test_redact_strategy(self):
        """Test redact masking strategy."""
        text = "secret"
        masked = MaskingStrategy.REDACT.value(text)
        assert masked == "[REDACTED]"
    
    def test_partial_strategy(self):
        """Test partial masking strategy."""
        text = "secret"
        masked = MaskingStrategy.PARTIAL.value(text)
        assert text[0] in masked or text[-1] in masked
        assert "*" in masked
    
    def test_set_strategy(self):
        """Test changing masking strategy."""
        masker = PatternMasker(strategy=MaskingStrategy.ASTERISK)
        assert masker.strategy == MaskingStrategy.ASTERISK
        
        masker.set_strategy(MaskingStrategy.HASH)
        assert masker.strategy == MaskingStrategy.HASH
