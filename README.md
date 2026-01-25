# How it works

The system uses two types of agents:

Contempletiva Agent: The assessment manager that administers Tau-Bench evaluations
- Receives requests specifying which agent to test and what tasks to run
- Sets up the Tau-Bench environment with the specified configuration
- Orchestrates the conversation between the benchmark and the target agent
- Evaluates responses and reports results

Activa Agent: The target agent being tested (COMING MARCH 2026)
- Can be any agent that implements the A2A protocol
- Receives task instructions and responds with tool calls or messages
- Operates without knowledge of being benchmarked

Agent actions
1. Send a message to the Contempletiva Agent with:
- The URL of the Activa Agent to test
- The benchmark configuration (domain, task_id, etc.)

2. The Compempletiva Agent:
- Instantiates a Tau-Bench environment
- Forwards user messages to the Activa Agent
- Collects the Activa Agent's responses
- Evaluates performance using Tau-Bench's scoring system
- Returns the results

3. The Activa Agent will respond to messages using its tools, unaware it's being evaluated.

# Configuring and running

1. Clone locally\
   ````git clone https://github.com/christian-templeton/contempletiva-agent````
   
2. Install dependencies\
   ````uv sync````

3. add an .env file to the folder you cloned this repository to in step 1, and add you Gemini API key here as below\
   ````GOOGLE_API_KEY=your_actual_api_key_here````

4. Run the server\
   ````uv run src/server.py````

# Attribution

1. Agent logic\
**$\tau^2$-Bench: Evaluating Conversational Agents in a Dual-Control Environment** ````Barres, V., Dong, H., Ray, S., Si, X., & Narasimhan, K. (2025). Tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment*. arXiv preprint arXiv:2506.07982.```` https://arxiv.org/abs/2506.07982

2. Agent names\
**The Human Condition** ````Arendt, Hannah. *The Human Condition*. 2nd ed. Chicago: The University of Chicago Press, 1998.````
