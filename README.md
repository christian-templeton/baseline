# How It Works

The system uses two types of agents:

(con)template agent: The assessment manager that administers Tau-Bench evaluations (https://github.com/christian-templeton/contempletiva-agent)
- Receives requests specifying which agent to test and what tasks to run
- Sets up the Tau-Bench environment with the specified configuration
- Orchestrates the conversation between the benchmark and the target agent
- Evaluates responses and reports results

(pro)active agent: The target agent being tested
- Can be any agent that implements the A2A protocol
- Receives task instructions and responds with tool calls or messages
- Operates without knowledge of being benchmarked

Agent actions
1. Send a message to the (con)template agent with:
- The URL of the (pro)active agent to test
- The benchmark configuration (domain, task_id, etc.)

2. The Compempletiva Agent:
- Instantiates a Tau-Bench environment
- Forwards user messages to the (pro)active agent
- Collects the (pro)active agent's responses
- Evaluates performance using Tau-Bench's scoring system
- Returns the results
  
3. The (pro)active agent will respond to messages using its tools, unaware it's being evaluated.

# Project Structure

````
├── .github/
│   └── workflows/
│       └── test-and-publish.yml    # CI/CD pipeline for building and testing Docker images
├── src/
│   ├── agent.py                    # Core Agent2Agent agent implementation (Purple Agent)
│   ├── executor.py                 # Logic for executing agent tasks
│   ├── messenger.py                # Utilities for Agents2Agent communication
│   ├── server.py                   # Entry point for the Agents2Agent server
│   ├── setup_data.py               # Data initialization and setup script
│   └── tau2_testing_agent.toml     # Configuration for the agent's identity/card
├── tests/
│   ├── conftest.py                 # Pytest shared fixtures and configuration
│   └── test_agent.py               # Integration and unit tests for agent logic
├── Dockerfile                      # Docker image configuration for containerization and deployment
├── pyproject.toml                  # Project dependencies and metadata (uv-managed)
├── uv.lock                         # Dependency lockfile for reproducible environments
└── README.md                       # Documentation for agent setup and operational flow
````
# Configuring and Running

1. Clone locally\
   ````git clone https://github.com/christian-templeton/baseline````
   
2. Install dependencies\
   ````uv sync````

3. add an .env file to the folder you cloned this repository to in step 1, and add you Gemini API key here as below\
   ````GOOGLE_API_KEY=your_actual_api_key_here````\
   ````AGENT_URL=http://localhost:9002````

4. Run the agent\
   ````uv run src/server.py````

5. Shut down the agent\
   ````CTRL+C````

# Contributing and Testing

1. Add Activa (white) agents you want to evaluate\
   See example at https://github.com/agentbeats/agentify-example-tau-bench/blob/main/src/white_agent/agent.py

2. Install test dependencies\
   ````uv sync --extra test````

3. Start your agent (follow instructions for starting and shutting down above)

4. Open a seperate terminal window 

5. Run tests\
   ````uv run pytest --agent-url http://localhost:9002````

# Attribution

1. Agent logic\
**$\tau^2$-Bench: Evaluating Conversational Agents in a Dual-Control Environment** ````Barres, V., Dong, H., Ray, S., Si, X., & Narasimhan, K. (2025). Tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment*. arXiv preprint arXiv:2506.07982.```` https://arxiv.org/abs/2506.07982

2. Agent names\
**The Human Condition** ````Arendt, Hannah. *The Human Condition*. 2nd ed. Chicago: The University of Chicago Press, 1998.````
