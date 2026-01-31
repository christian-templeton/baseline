FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src src

RUN \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync

RUN mkdir -p /app/data/tau2 && \
    mkdir -p /tmp/tau2-bench && \
    curl -L https://github.com/sierra-research/tau2-bench/archive/refs/heads/main.tar.gz | \
    tar -xz --strip-components=1 -C /tmp/tau2-bench && \
    cp -r /tmp/tau2-bench/src/tau2/domains /app/data/tau2/ && \
    rm -rf /tmp/tau2-bench

ENV TAU2_DATA_DIR=/app/data

ENTRYPOINT ["uv", "run", "src/server.py"]
CMD ["--host", "0.0.0.0"]
EXPOSE 9002
