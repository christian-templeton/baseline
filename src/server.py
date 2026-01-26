import argparse
from agent import start_green_agent
def main():
    parser = argparse.ArgumentParser(description="Run the A2A agent.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server")
    parser.add_argument("--port", type=int, default=9009, help="Port to bind the server")
    args = parser.parse_args()
    # Launch the agent using its built-in startup function
    start_green_agent(agent_name="tau2_testing_agent", host=args.host, port=args.port)
if __name__ == '__main__':
    main()
