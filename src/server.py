import argparse
import uvicorn
import tomllib
import pathlib

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from executor import Executor


def main():
    parser = argparse.ArgumentParser(description="Run the A2A agent.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server")
    parser.add_argument("--port", type=int, default=9002, help="Port to bind the server")
    parser.add_argument("--card-url", type=str, help="URL to advertise in the agent card")
    args = parser.parse_args()

    # Load configuration from src/tau2_testing_agent.toml
    config_path = pathlib.Path(__file__).parent / "tau2_testing_agent.toml"
    with open(config_path, "rb") as f:
        config_data = tomllib.load(f)

    skills = [
        AgentSkill(
            id=s["id"],
            name=s["name"],
            description=s["description"],
            tags=s.get("tags", []),
            examples=s.get("examples", [])
        )
        for s in config_data.get("skills", [])
    ]

    agent_card = AgentCard(
        name=config_data.get("name", "baseline-agent"),
        description=config_data.get("description", "A baseline A2A agent."),
        url=args.card_url or f"http://{args.host}:{args.port}/",
        version=config_data.get("version", "1.0.0"),
        default_input_modes=config_data.get("defaultInputModes", ["text"]),
        default_output_modes=config_data.get("defaultOutputModes", ["text"]),
        capabilities=AgentCapabilities(
            streaming=config_data.get("capabilities", {}).get("streaming", True)
        ),
        skills=skills
    )

    request_handler = DefaultRequestHandler(
        agent_executor=Executor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    uvicorn.run(server.build(), host=args.host, port=args.port)


if __name__ == '__main__':
    main()
