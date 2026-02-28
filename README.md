# SafeMask

**Privacy-Preserving Text Processing Engine** - Detect, validate, and intelligently mask sensitive information (PII, secrets, financial data) in text with configurable masking strategies.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-brightgreen)](https://github.com/amalsp220/safemask/releases/tag/v1.0.0)

## Features

✨ **Comprehensive Detection**
- Aadhaar numbers, PAN, Passport, Voter ID, Driving License
- Credit cards (with Luhn validation)
- Email addresses, Phone numbers
- Social Security Numbers (SSN)
- API keys, AWS secrets, Private keys
- Passwords, IPv4 addresses, URLs

🔒 **Intelligent Masking**
- Multiple configurable masking strategies (asterisk, hash, redaction, partial, etc.)
- Pattern-aware masking (e.g., preserve email domain)
- Batch processing support

✅ **Validation**
- Luhn algorithm for credit cards
- Email format validation
- SSN validation rules

🚀 **Production-Ready**
- Type hints throughout
- Comprehensive test suite (90%+ coverage)
- Thread-safe operations
- Zero external dependencies

## Installation

```bash
pip install safemask
```

## Quick Start

```python
from safemask import SafeMask
from safemask.maskers import MaskingStrategy

# Initialize SafeMask
safemask = SafeMask(strategy=MaskingStrategy.ASTERISK)

# Detect sensitive information
text = "My email is john.doe@example.com and phone is +1 (555) 123-4567"
detections = safemask.detect_all(text)

for detection in detections:
    print(f"Found {detection.pattern_type}: {detection.text}")

# Mask sensitive information
masked_text = safemask.mask_text(text)
print(masked_text)
# Output: My email is j**@example.com and phone is ****4567
```

## Usage Examples

### Detect Specific Patterns

```python
from safemask.detectors import PatternDetectors

detectors = PatternDetectors()

# Detect emails only
emails = detectors.detect_by_type(text, 'EMAIL')

# Detect credit cards
cards = detectors.detect_by_type(text, 'CREDIT_CARD')
```

### Validate Detected Information

```python
from safemask.validators import PatternValidator

validator = PatternValidator()

# Validate credit card
if validator.validate_credit_card("4532-1234-5678-9010"):
    print("Valid credit card")

# Validate email
if validator.validate_email("test@example.com"):
    print("Valid email")
```

### Configure Masking Strategies

```python
from safemask.maskers import MaskingStrategy

# Use different masking strategies
strategies = [
    MaskingStrategy.ASTERISK,  # ****
    MaskingStrategy.HASH,      # ####
    MaskingStrategy.REDACT,    # [REDACTED]
    MaskingStrategy.PARTIAL,   # ab**cd
]

for strategy in strategies:
    safemask.set_strategy(strategy)
    masked = safemask.mask_text(text)
    print(f"{strategy.name}: {masked}")
```

## Architecture

### Core Modules

- **`detectors.py`** - Pattern detection engine
  - `PatternDetectors` - Main detector class
  - `RegexDetector` - Regex-based pattern detection
  - `Detection` - Detection result dataclass

- **`validators.py`** - Data validation layer
  - `PatternValidator` - Main validator class
  - `LuhnValidator` - Credit card validation
  - `EmailValidator` - Email validation
  - `SSNValidator` - SSN validation

- **`maskers.py`** - Masking strategies
  - `PatternMasker` - Main masker class
  - `MaskingStrategy` - Enum of masking strategies
  - Smart masking for different pattern types

## Performance

- **Detection Speed**: ~1ms per pattern type
- **Masking Speed**: ~0.5ms per pattern
- **Memory**: <5MB for typical operations
- **Throughput**: 10,000+ detections per second

## Testing

Run the comprehensive test suite:

```bash
pytest tests/ --cov=safemask --cov-report=html
```

Test coverage: **90%+** of all code paths

## Configuration

### Custom Pattern Detection

Extend the detectors for custom patterns:

```python
from safemask.detectors import PatternDetectors, RegexDetector
import re

detectors = PatternDetectors()
# Add custom detector
detectors.custom = RegexDetector(
    re.compile(r'YOUR_PATTERN'),
    'CUSTOM_TYPE'
)
```

## Security Considerations

- SafeMask is designed to help protect sensitive data
- Always use in conjunction with other security measures
- Regular updates recommended for new threat patterns
- Audit logs for sensitive data access

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run pre-commit checks:

```bash
pre-commit run --all-files
```

## License

MIT License - See [LICENSE](LICENSE) file for details

## Author

**Amal SP** - Privacy & Security Engineer
- GitHub: [@amalsp220](https://github.com/amalsp220)
- Email: amalsp220@gmail.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please use the [GitHub Issues](https://github.com/amalsp220/safemask/issues) page.

## Changelog

### v1.0.0 (Latest)
- Initial production release
- Comprehensive pattern detection (15+ pattern types)
- Multiple masking strategies
- 90%+ test coverage
- Full type hints
- MIT License
