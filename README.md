# LiteLLM with Custom Email-Based Auth

LiteLLM with custom authentication that validates the `x-user-email` header using LiteLLM's built-in `custom_auth` feature.

## Architecture

```
Client Request → LiteLLM (port 4000) → LLM Providers
                    ↓
              Custom Auth Hook (custom_auth.py)
              Checks x-user-email header
```

This approach extends LiteLLM directly without needing a separate gateway/proxy.

## How It Works

1. **custom_auth.py** - Python module with auth logic
2. **litellm_config.yaml** - References custom auth function
3. **Docker mount** - Custom module mounted into container
4. **Environment variables** - API keys loaded from .env file

LiteLLM automatically calls the custom auth function before processing each request.

## Setup

### 1. Configure API Keys

Copy the example env file and add your API keys:

```bash
cp .env.example .env
```

Then edit `.env` with your actual API keys:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GROQ_API_KEY=gsk-your-groq-key-here
```

**Important:** The `.env` file is gitignored and will never be committed to version control.

### 2. Run LiteLLM

```bash
# Start LiteLLM with custom auth
make run
```

That's it! The docker container will:
- Mount `litellm_config.yaml` (includes custom_auth config)
- Mount `custom_auth.py` (your auth logic)
- Start on port 4000 with auth enabled

## Usage

### ✅ Successful Request (with x-user-email header)
```bash
make curl
```

Or manually:
```bash
curl -X POST 'http://localhost:4000/chat/completions' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-1234567890' \
  -H 'x-user-email: user@example.com' \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### ❌ Failed Request (missing x-user-email header)
```bash
make curl-noauth
```

Returns 401: `Missing x-user-email header`

## Customizing Auth Logic

Edit `custom_auth.py` and modify the `is_email_allowed()` function:

```python
def is_email_allowed(email: str) -> bool:
    # Example: only allow specific domains
    allowed_domains = ["company.com", "partner.com"]
    domain = email.split("@")[1]
    return domain in allowed_domains

    # Or check against a database, API, etc.
```

## What Gets Logged

The auth hook logs to stdout:
- All incoming request headers
- The `x-user-email` value
- Auth success/failure for each request

View logs in the terminal running `make run`.

## Key Files

- **custom_auth.py** - Your custom auth logic (mounted into container)
- **litellm_config.yaml** - LiteLLM config with `general_settings.custom_auth` and env var references
- **.env** - Your API keys (gitignored, never committed)
- **.env.example** - Template for required environment variables
- **Makefile** - Docker run command with volume mounts and env file
- **.gitignore** - Ensures .env is never committed to git
