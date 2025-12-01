"""
Helper script to check if .env is loaded correctly
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from credentials/.env
credentials_dir = Path(__file__).parent.parent / "credentials"
dotenv_path = credentials_dir / ".env"

print(f"Looking for .env file at: {dotenv_path}")
print(f"File exists: {dotenv_path.exists()}")

if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
    print("\n✅ .env file loaded!")
else:
    print("\n⚠️  .env file not found. Using environment variables if set.")

# Check if API key is available
api_key = os.environ.get("ANTHROPIC_API_KEY")
if api_key:
    # Show only first few characters for security
    masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else api_key[:3] + "..."
    print(f"✅ ANTHROPIC_API_KEY found: {masked_key}")
else:
    print("❌ ANTHROPIC_API_KEY not found!")
    print("\nTo fix this:")
    print(f"1. Create file: {dotenv_path}")
    print("2. Add this line: ANTHROPIC_API_KEY=your-api-key-here")
