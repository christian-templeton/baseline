"""
Tau2 Agent - Purple agent that solves tau-bench tasks.

This is the agent being tested. It:
1. Receives task descriptions with available tools from the green agent
2. Decides which tool to call or how to respond"""

import os
from dotenv import load_dotenv
from litellm import completion
from loguru import logger
from a2a.types import Part, TextPart
from a2a.utils import get_message_text
# Load environment variables (API keys, etc.)
load_dotenv()
SYSTEM_PROMPT = """You are a helpful customer service agent. Follow the policy and tool instructions provided in each message."""
class Agent:
    def __init__(self, model: str = None):
        """
        Initializes the agent. 
        Compatible with executor.py which calls 'Agent()'.
        """
        # Uses the model from environment or defaults to gpt-4o
        self.model = model or os.getenv("AGENT_MODEL", "openai/gpt-4o")
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    async def run(self, message, updater):
        """
        The main loop for the agent. 
        Matches the signature: async def run(self, msg, updater) from executor.py.
        """
        # Safely extract text from the incoming A2A message
        user_input = get_message_text(message)
        self.messages.append({"role": "user", "content": user_input})
        
        logger.info(f"Agent received input: {user_input[:100]}...")
        try:
            # Calls the LLM via litellm (which supports Gemini, OpenAI, etc.)
            response = completion(
                messages=self.messages,
                model=self.model,
                temperature=0.0,
            )
            assistant_content = response.choices[0].message.content
            logger.info(f"LLM response: {assistant_content[:100]}...")
            
            # Save to conversation history
            self.messages.append({"role": "assistant", "content": assistant_content})
            
            # Report the final answer back to the benchmark as an artifact
            await updater.add_artifact([Part(root=TextPart(text=assistant_content))])
            
        except Exception as e:
            logger.error(f"Error during agent execution: {e}")
            # Send an error message back so the benchmark doesn't hang
            await updater.add_artifact([
                Part(root=TextPart(text=f"I encountered an error processing your request: {e}"))
            ])
