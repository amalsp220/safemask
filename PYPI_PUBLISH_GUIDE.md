# PyPI Publishing Guide for SafeMask

## Current Status

The SafeMask package has been successfully built and is ready to be published to PyPI. However, there's one final step required to complete the publication.

## The Issue: OIDC Trusted Publisher

The GitHub Actions workflow is configured to use **OIDC Trusted Publishers** for secure, passwordless authentication with PyPI. This is the recommended best practice.

However, the trust relationship between GitHub and PyPI needs to be configured in your PyPI account first.

## Solution: Two Options

### Option 1: Configure OIDC Trusted Publisher (RECOMMENDED)

Follow these steps in your PyPI account:

1. Go to https://pypi.org/manage/account/
2. Click on **Publishing** in the left sidebar
3. Click **"Add a new pending publisher"**
4. Fill in the following details:
   - **GitHub repository owner**: amalsp220
   - **GitHub repository name**: safemask
   - **GitHub workflow name**: python-publish.yml
   - **GitHub environment name**: pypi
5. Click **"Add pending publisher"**
6. The pending publisher will appear in your account. Once you verify it in GitHub (which should happen automatically), it becomes active.

Once configured, the next release will automatically publish to PyPI!

### Option 2: Manual Publication with API Token

If you prefer, you can manually publish using a PyPI API token:

```bash
# Clone the repo
git clone https://github.com/amalsp220/safemask.git
cd safemask

# Install build dependencies
pip install build twine

# Build the package
python -m build

# Publish to PyPI (you'll be prompted for credentials)
# Use __token__ as username and your PyPI API token as password
twine upload dist/*
```

## Trigger the Next Build

Once you've configured the OIDC trusted publisher in your PyPI account, create a new release:

1. Go to https://github.com/amalsp220/safemask/releases/new
2. Create a new tag (e.g., v1.0.2)
3. Add release notes
4. Publish the release

The workflow will automatically build and publish to PyPI!

## Verification

Once published, verify your package at:
https://pypi.org/project/safemask/

You can also check it's listed under your account:
https://pypi.org/user/amalsp220/

## Support

For more information about OIDC trusted publishers, see:
https://docs.pypi.org/trusted-publishers/using-trusted-publishers/
