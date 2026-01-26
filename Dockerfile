FROM ghcr.io/astral-sh/uv:python3.13-bookworm

RUN adduser agent
USER agent
WORKDIR /home/agent

COPY --chown=agent:agent pyproject.toml uv.lock README.md ./
COPY --chown=agent:agent src src

RUN \
    --mount=type=cache,target=/home/agent/.cache/uv,uid=1000 \
    uv sync --locked

RUN uv add python-dotenv gymnasium
RUN uv add "tau2 @ git+https://github.com/sierra-research/tau2-bench"
RUN uv add "agentify-tau-bench @ git+https://github.com/sierra-research/tau2-bench#subdirectory=src/experiments/agentify_tau_bench"

RUN curl -L https://github.com/sierra-research/tau2-bench/archive/refs/heads/main.tar.gz | \
    tar -xz --strip-components=1 -C /home/agent && \
    mkdir -p /home/agent/.venv/lib/python3.13/data/tau2 && \
    cp -r /home/agent/src/tau2/domains /home/agent/.venv/lib/python3.13/data/tau2/

ENTRYPOINT ["uv", "run", "src/server.py"]
CMD ["--host", "0.0.0.0"]
EXPOSE 9009
