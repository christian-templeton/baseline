FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src src

RUN uv pip compile pyproject.toml -o uv.lock

RUN \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

RUN uv add python-dotenv gymnasium \
    "tau2 @ git+https://github.com/sierra-research/tau2-bench" \
    "agentify-tau-bench @ git+https://github.com/sierra-research/tau2-bench#subdirectory=src/experiments/agentify_tau_bench"

RUN mkdir -p /tmp/tau2-bench && \
    curl -L https://github.com/sierra-research/tau2-bench/archive/refs/heads/main.tar.gz | \
    tar -xz --strip-components=1 -C /tmp/tau2-bench && \
    SITE_PACKAGES=$(uv run python -c 'import site; print(site.getsitepackages()[0])') && \
    cp -r /tmp/tau2-bench/src/tau2/domains "${SITE_PACKAGES}/tau2/" && \
    rm -rf /tmp/tau2-bench

ENTRYPOINT ["uv", "run"]
CMD ["src/server.py", "--host", "0.0.0.0", "--port", "9009"]
EXPOSE 9009
