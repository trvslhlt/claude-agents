"""
Quick test script for the PM Agent
Run this to test the agent without interactive mode
"""

import os
from main import ProductManagerAgent


def test_agent():
    """Test the PM agent with sample queries."""

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nSet it with: export ANTHROPIC_API_KEY='your-api-key'")
        return

    print("=" * 60)
    print("🧪 Testing PM Agent")
    print("=" * 60)

    agent = ProductManagerAgent(api_key)

    # Test queries
    test_queries = [
        "Calculate the RICE score for a feature that reaches 5000 users per month, has high impact (2), 75% confidence, and takes 2 months to build",
        "What does our current roadmap look like?",
        "Check the backend team's capacity for the next sprint"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Test {i}: {query}")
        print(f"{'=' * 60}")

        try:
            response = agent.run(query)
            print(f"\n🤖 Response:\n{response}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

    print("=" * 60)
    print("✅ Testing complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_agent()
