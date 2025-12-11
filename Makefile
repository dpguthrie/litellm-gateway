# Run LiteLLM backend with custom auth (port 4000)
run-litellm:
	docker run \
		--env-file .env \
		-v $$(pwd)/litellm_config.yaml:/app/config.yaml \
		-v $$(pwd)/custom_auth.py:/app/custom_auth.py \
		-p 4000:4000 \
		ghcr.io/berriai/litellm:main-latest \
		--config /app/config.yaml --detailed_debug

# Alias for run-litellm (simpler command)
run:
	@make run-litellm

# Test WITH x-user-email header (should succeed)
curl:
	curl -X POST 'http://0.0.0.0:4000/chat/completions' \
		-H 'Content-Type: application/json' \
		-H 'Authorization: Bearer sk-1234567890' \
		-H 'x-user-email: user@example.com' \
		-d '{"model": "gpt-4o", "messages": [{"role": "system", "content": "You are an LLM named gpt-4o"}, {"role": "user", "content": "what is your name?"}]}'

# Test WITHOUT x-user-email header (should fail with 401)
curl-noauth:
	curl -X POST 'http://0.0.0.0:4000/chat/completions' \
		-H 'Content-Type: application/json' \
		-H 'Authorization: Bearer sk-1234567890' \
		-d '{"model": "gpt-4o", "messages": [{"role": "system", "content": "You are an LLM named gpt-4o"}, {"role": "user", "content": "what is your name?"}]}'

.PHONY: run run-litellm curl curl-noauth


