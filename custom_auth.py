"""
Custom LiteLLM callback for x-user-email authentication
This file gets mounted into the LiteLLM docker container
"""
from fastapi import Request, HTTPException


def is_email_allowed(email: str) -> bool:
    """
    Trivial auth logic - customize as needed
    """
    if not email or "@" not in email:
        return False

    # For demo: allow any valid-looking email
    # Customize this to check against a database, specific domains, etc.
    print(f"[AUTH] Checking email: {email}")
    return True


async def custom_auth_check(request: Request):
    """
    This function is called before every request to LiteLLM
    Extracts and validates the x-user-email header
    """
    # Extract x-user-email header
    user_email = request.headers.get("x-user-email")

    print(f"\n{'='*50}")
    print(f"[AUTH] Incoming request to: {request.url.path}")
    print(f"[AUTH] x-user-email: {user_email}")
    print(f"[AUTH] All headers: {dict(request.headers)}")
    print(f"{'='*50}\n")

    # Only check auth for /chat/completions endpoint
    if request.url.path in ["/chat/completions", "/v1/chat/completions"]:
        if not user_email:
            print("[AUTH] ❌ REJECTED - Missing x-user-email header")
            raise HTTPException(
                status_code=401,
                detail="Missing x-user-email header"
            )

        if not is_email_allowed(user_email):
            print(f"[AUTH] ❌ REJECTED - Email not authorized: {user_email}")
            raise HTTPException(
                status_code=403,
                detail=f"Email {user_email} is not authorized"
            )

        print(f"[AUTH] ✓ AUTHORIZED - User: {user_email}")

    return user_email


# Register the custom auth function with LiteLLM
# This will be called automatically before each request
print("[AUTH] Custom auth callback loaded!")
