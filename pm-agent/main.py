"""
Product Manager Agent
A simple agent that helps with product management tasks using Claude.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from credentials/.env
credentials_dir = Path(__file__).parent.parent / "credentials"
dotenv_path = credentials_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)


class ProductManagerAgent:
    """An AI agent that acts as a product manager assistant."""

    def __init__(self, api_key: str = None):
        """Initialize the PM agent."""
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-5-20250929"
        self.tools = self._define_tools()
        self.system_prompt = """You are an experienced product manager at a startup.
You help with:
- Feature prioritization using frameworks like RICE
- Creating well-structured user stories
- Analyzing product metrics and user feedback
- Planning roadmaps and checking team capacity
- Competitive analysis
- Generating stakeholder updates

Always ask clarifying questions when needed and provide data-driven recommendations.
Use the available tools to gather information before making decisions."""

    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define the tools available to the PM agent."""
        return [
            {
                "name": "calculate_rice_score",
                "description": "Calculate RICE score (Reach × Impact × Confidence / Effort) for feature prioritization",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "feature_name": {
                            "type": "string",
                            "description": "Name of the feature being evaluated"
                        },
                        "reach": {
                            "type": "number",
                            "description": "Number of users/customers affected per time period"
                        },
                        "impact": {
                            "type": "number",
                            "description": "Impact score: 0.25=minimal, 0.5=low, 1=medium, 2=high, 3=massive"
                        },
                        "confidence": {
                            "type": "number",
                            "description": "Confidence percentage (e.g., 80 for 80%)"
                        },
                        "effort": {
                            "type": "number",
                            "description": "Effort in person-months"
                        }
                    },
                    "required": ["feature_name", "reach", "impact", "confidence", "effort"]
                }
            },
            {
                "name": "create_user_story",
                "description": "Generate a well-formatted user story with acceptance criteria",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "user_type": {
                            "type": "string",
                            "description": "Type of user (e.g., 'customer', 'admin', 'developer')"
                        },
                        "goal": {
                            "type": "string",
                            "description": "What the user wants to accomplish"
                        },
                        "benefit": {
                            "type": "string",
                            "description": "Why the user wants this (the value/benefit)"
                        },
                        "acceptance_criteria": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of acceptance criteria (optional)"
                        }
                    },
                    "required": ["user_type", "goal", "benefit"]
                }
            },
            {
                "name": "analyze_product_metrics",
                "description": "Get simulated product metrics (in real implementation, would connect to analytics)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "metric_type": {
                            "type": "string",
                            "enum": ["dau", "wau", "mau", "retention", "nps", "conversion"],
                            "description": "Type of metric to retrieve"
                        },
                        "time_period": {
                            "type": "string",
                            "description": "Time period (e.g., 'last_week', 'last_month', 'last_quarter')"
                        }
                    },
                    "required": ["metric_type", "time_period"]
                }
            },
            {
                "name": "get_roadmap",
                "description": "Retrieve current product roadmap (simulated data)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "quarter": {
                            "type": "string",
                            "description": "Which quarter to view (e.g., 'current', 'next', 'Q1_2024')"
                        }
                    },
                    "required": ["quarter"]
                }
            },
            {
                "name": "check_team_capacity",
                "description": "Check engineering team capacity (simulated data)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "team": {
                            "type": "string",
                            "description": "Team name (e.g., 'backend', 'frontend', 'mobile')"
                        },
                        "time_period": {
                            "type": "string",
                            "description": "Time period (e.g., 'next_sprint', 'next_month')"
                        }
                    },
                    "required": ["team", "time_period"]
                }
            }
        ]

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """Execute a tool call and return the result."""

        if tool_name == "calculate_rice_score":
            reach = tool_input["reach"]
            impact = tool_input["impact"]
            confidence = tool_input["confidence"] / 100  # Convert to decimal
            effort = tool_input["effort"]

            rice_score = (reach * impact * confidence) / effort

            return {
                "feature": tool_input["feature_name"],
                "rice_score": round(rice_score, 2),
                "breakdown": {
                    "reach": reach,
                    "impact": impact,
                    "confidence": f"{tool_input['confidence']}%",
                    "effort": f"{effort} person-months"
                },
                "interpretation": self._interpret_rice_score(rice_score)
            }

        elif tool_name == "create_user_story":
            story = f"As a {tool_input['user_type']}, I want {tool_input['goal']} so that {tool_input['benefit']}."

            result = {
                "user_story": story,
                "format": "standard",
                "components": {
                    "user_type": tool_input["user_type"],
                    "goal": tool_input["goal"],
                    "benefit": tool_input["benefit"]
                }
            }

            if "acceptance_criteria" in tool_input:
                result["acceptance_criteria"] = tool_input["acceptance_criteria"]

            return result

        elif tool_name == "analyze_product_metrics":
            # Simulated metrics (in real implementation, fetch from analytics platform)
            metric_type = tool_input["metric_type"]
            time_period = tool_input["time_period"]

            # Sample data
            metrics_data = {
                "dau": {"current": 15420, "previous": 14850, "change": "+3.8%"},
                "wau": {"current": 45200, "previous": 43100, "change": "+4.9%"},
                "mau": {"current": 125000, "previous": 118000, "change": "+5.9%"},
                "retention": {"day_1": "72%", "day_7": "45%", "day_30": "28%"},
                "nps": {"score": 42, "promoters": "45%", "detractors": "15%"},
                "conversion": {"rate": "3.2%", "funnel": {"visitors": 10000, "signups": 320}}
            }

            return {
                "metric": metric_type.upper(),
                "time_period": time_period,
                "data": metrics_data.get(metric_type, {}),
                "note": "This is simulated data. Connect to your analytics platform for real metrics."
            }

        elif tool_name == "get_roadmap":
            quarter = tool_input["quarter"]

            # Simulated roadmap
            roadmap = {
                "current": {
                    "quarter": "Q4 2024",
                    "features": [
                        {"name": "User authentication v2", "status": "in_progress", "priority": "P0", "owner": "Backend team"},
                        {"name": "Mobile app redesign", "status": "planning", "priority": "P1", "owner": "Mobile team"},
                        {"name": "Analytics dashboard", "status": "completed", "priority": "P0", "owner": "Frontend team"}
                    ]
                },
                "next": {
                    "quarter": "Q1 2025",
                    "features": [
                        {"name": "AI-powered recommendations", "status": "planned", "priority": "P1", "owner": "ML team"},
                        {"name": "Team collaboration features", "status": "planned", "priority": "P0", "owner": "Backend team"},
                        {"name": "Advanced reporting", "status": "planned", "priority": "P2", "owner": "Frontend team"}
                    ]
                }
            }

            return roadmap.get(quarter, {"error": "Quarter not found. Try 'current' or 'next'"})

        elif tool_name == "check_team_capacity":
            team = tool_input["team"]
            time_period = tool_input["time_period"]

            # Simulated capacity data
            capacity_data = {
                "backend": {"total_points": 50, "committed": 38, "available": 12, "engineers": 5},
                "frontend": {"total_points": 40, "committed": 35, "available": 5, "engineers": 4},
                "mobile": {"total_points": 30, "committed": 25, "available": 5, "engineers": 3}
            }

            team_data = capacity_data.get(team.lower(), {})

            if team_data:
                utilization = (team_data["committed"] / team_data["total_points"]) * 100
                return {
                    "team": team,
                    "time_period": time_period,
                    "capacity": team_data,
                    "utilization": f"{utilization:.1f}%",
                    "recommendation": "Good capacity" if utilization < 85 else "Team is at capacity"
                }
            else:
                return {"error": f"Team '{team}' not found. Available teams: backend, frontend, mobile"}

        return {"error": f"Unknown tool: {tool_name}"}

    def _interpret_rice_score(self, score: float) -> str:
        """Interpret RICE score and provide guidance."""
        if score >= 100:
            return "Very High Priority - Strong candidate for immediate development"
        elif score >= 50:
            return "High Priority - Should be prioritized in upcoming sprint"
        elif score >= 20:
            return "Medium Priority - Good addition to roadmap"
        else:
            return "Low Priority - Consider for future or deprioritize"

    def run(self, user_message: str) -> str:
        """Run the agent with a user message."""
        messages = [{"role": "user", "content": user_message}]

        print(f"\n🤖 PM Agent thinking...\n")

        # Agent loop
        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=self.tools,
                messages=messages
            )

            # Check if we're done
            if response.stop_reason == "end_turn":
                final_response = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_response += block.text
                return final_response

            # Process tool uses
            if response.stop_reason == "tool_use":
                # Add assistant's response to messages
                messages.append({"role": "assistant", "content": response.content})

                # Execute tools and collect results
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"🔧 Using tool: {block.name}")
                        print(f"   Input: {json.dumps(block.input, indent=2)}")

                        tool_result = self._execute_tool(block.name, block.input)

                        print(f"   Result: {json.dumps(tool_result, indent=2)}\n")

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(tool_result)
                        })

                # Add tool results to messages
                messages.append({"role": "user", "content": tool_results})
            else:
                # Unexpected stop reason
                return f"Unexpected stop reason: {response.stop_reason}"


def main():
    """Main entry point for the PM agent."""

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nSet it with: export ANTHROPIC_API_KEY='your-api-key'")
        return

    print("=" * 60)
    print("🚀 Product Manager Agent")
    print("=" * 60)
    print("\nThis agent helps with product management tasks:")
    print("  • Feature prioritization (RICE scores)")
    print("  • User story creation")
    print("  • Product metrics analysis")
    print("  • Roadmap planning")
    print("  • Team capacity planning")
    print("\nType 'quit' or 'exit' to stop.\n")
    print("=" * 60)

    agent = ProductManagerAgent(api_key)

    # Interactive mode
    while True:
        try:
            user_input = input("\n💬 You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye!\n")
                break

            response = agent.run(user_input)
            print(f"\n🤖 PM Agent:\n{response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
