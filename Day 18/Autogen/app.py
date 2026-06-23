import os
import asyncio
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient


load_dotenv()


async def run_team():
    # Fetch the Groq API key from .env
    groq_key = os.environ["GROQ_API_KEY"]

    # Define Groq model clients
    researcher_model = OpenAIChatCompletionClient(
        model="llama-3.1-8b-instant",
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_key,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "family": "unknown"
        }
    )

    editor_model = OpenAIChatCompletionClient(
        model="llama-3.3-70b-versatile",
        base_url="https://api.groq.com/openai/v1",
        api_key=groq_key,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "family": "unknown"
        }
    )

    # Define the individual Agents
    researcher = AssistantAgent(
        name="Researcher",
        model_client=researcher_model,
        system_message="You are an expert researcher. Provide a highly detailed summary using clear Markdown formatting."
    )

    editor = AssistantAgent(
        name="Editor",
        model_client=editor_model,
        system_message="You are a strict editor. Critique the researcher's work and optimize it for professional delivery."
    )

    # Orchestrate the workflow team
    team = RoundRobinGroupChat(
        participants=[researcher, editor],
        termination_condition=MaxMessageTermination(max_messages=4)
    )

    # Run the prompt
    print("--- Starting Multi-Agent Session ---")
    async for message in team.run_stream(
        task="Explain why Groq LPUs provide higher throughput for LLMs than standard GPUs."
    ):
        if hasattr(message, "source") and hasattr(message, "content"):
            print(f"\n\033[1m[{message.source}]\033[0m: {message.content}")
            print("-" * 40)
        else:
            print("\n--- Final Result ---")
            print(message)
            print("-" * 40)


if __name__ == "__main__":
    asyncio.run(run_team())