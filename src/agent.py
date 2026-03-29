from typing import Any
from pydantic import BaseModel, HttpUrl, ValidationError
from a2a.server.tasks import TaskUpdater
from a2a.types import Message, TaskState, Part, TextPart, DataPart
from a2a.utils import get_message_text, new_agent_text_message

from messenger import Messenger


class EvalRequest(BaseModel):
    """Request format sent by the AgentBeats platform to green agents."""
    participants: dict[str, HttpUrl] # role -> agent URL
    config: dict[str, Any]


class Agent:
    # Fill in: list of required participant roles, e.g. ["pro_debater", "con_debater"]
    required_roles: list[str] = []
    # Fill in: list of required config keys, e.g. ["topic", "num_rounds"]
    required_config_keys: list[str] = []

    def __init__(self):
        self.messenger = Messenger()
        # Initialize other state here

    def validate_request(self, request: EvalRequest) -> tuple[bool, str]:
        missing_roles = set(self.required_roles) - set(request.participants.keys())
        if missing_roles:
            return False, f"Missing roles: {missing_roles}"

        missing_config_keys = set(self.required_config_keys) - set(request.config.keys())
        if missing_config_keys:
            return False, f"Missing config keys: {missing_config_keys}"

        # Add additional request validation here

        return True, "ok"

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        """Implement your agent logic here.

        This agent can handle both EvalRequest JSON (as an Assessment Manager)
        and plain text messages (as a Target Agent).
        """
        input_text = get_message_text(message)

        try:
            # Try to parse as Green Agent evaluation request
            request = EvalRequest.model_validate_json(input_text)
            ok, msg = self.validate_request(request)
            if not ok:
                await updater.reject(new_agent_text_message(msg))
                return

            # Green Agent logic: Acknowledge the request and provide a dummy result
            await updater.update_status(
                TaskState.working, new_agent_text_message("Assessment started...")
            )
            await updater.add_artifact(
                parts=[
                    Part(root=TextPart(text="Baseline assessment complete.")),
                    Part(root=DataPart(data={"pass_rate": 1.0}))
                ],
                name="Result",
            )
            await updater.complete(new_agent_text_message("Assessment finished successfully."))
            return

        except (ValidationError, ValueError):
            # Fallback for plain text messages (Purple Agent role)
            await updater.update_status(
                TaskState.working, new_agent_text_message("Processing message...")
            )
            response_text = f"Echo: {input_text}"
            await updater.complete(new_agent_text_message(response_text))
