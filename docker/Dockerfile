FROM python:3.9-slim

WORKDIR /app

COPY agent-tests/ /app/agent-tests/
COPY scripts/run_tests.sh /app/run_tests.sh

RUN chmod +x /app/run_tests.sh

ENTRYPOINT ["/app/run_tests.sh"]
