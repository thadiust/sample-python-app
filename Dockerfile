FROM python:3.11-slim
RUN useradd --no-create-home --uid 10001 appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser tests ./tests/
USER appuser
CMD ["python", "-m", "pytest", "-q", "tests/"]
