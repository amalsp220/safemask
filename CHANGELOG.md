# Changelog

All notable changes to SafeMask will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-28

### Added
- **Initial Production Release**
- Comprehensive pattern detection for 18+ sensitive data types:
  - Aadhaar numbers (Indian national ID)
  - PAN (Permanent Account Number)
  - Passport numbers
  - Voter IDs
  - Driving licenses
  - Credit cards with Luhn validation
  - Email addresses
  - Phone numbers
  - Social Security Numbers (SSN)
  - API keys
  - AWS secrets
  - Private keys
  - Passwords
  - IPv4 addresses
  - URLs
  
- **Advanced Validation Layer**
  - Luhn algorithm for credit card validation
  - Email format validation
  - SSN validation with proper rules
  - Custom validators support
  
- **Intelligent Masking**
  - Multiple configurable masking strategies:
    - ASTERISK: Full replacement with asterisks
    - HASH: Full replacement with hash symbols
    - X: Full replacement with X characters
    - REDACT: [REDACTED] replacement
    - PARTIAL: Keep first/last characters
    - FIRST_HALF: Mask first half only
    - LAST_HALF: Mask last half only
  - Pattern-aware masking (e.g., preserve email domains)
  - Batch detection and masking

- **Production-Ready Features**
  - Type hints throughout codebase
  - 90%+ test coverage with pytest
  - Zero external dependencies for core functionality
  - Thread-safe operations
  - Modular architecture (Detectors → Validators → Maskers)

- **Comprehensive Documentation**
  - Professional README with badges and examples
  - Quick start guide
  - Architecture documentation
  - Performance benchmarks

- **Development Infrastructure**
  - GitHub Actions CI/CD workflow
  - pytest configuration with coverage settings
  - Test suite for all major modules
  - Pre-commit hooks configuration
  - Linting and type checking setup
  - Security scanning (bandit)

- **Package Distribution**
  - Published to PyPI
  - MIT License
  - Clean project metadata
  - Python 3.10+ support

### Features
- Detect sensitive information across multiple data types
- Validate detected patterns with advanced algorithms
- Mask sensitive information with configurable strategies
- Enterprise-ready with comprehensive documentation
- Production deployment tested and optimized

### Release Assets
- Source code (zip and tar.gz formats)
- Full test suite
- Comprehensive documentation
- CI/CD pipelines
- MIT licensed

---

## Versioning

This project uses [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for added functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to SafeMask.

## Author

Maintained by **Amal SP** ([amalsp220](https://github.com/amalsp220))

## License

MIT License - See [LICENSE](LICENSE) file for details

## Support

For issues, questions, or feature requests, please use the [GitHub Issues](https://github.com/amalsp220/safemask/issues) page.
