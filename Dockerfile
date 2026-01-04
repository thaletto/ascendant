FROM python:3.12-slim

WORKDIR /app

# Install git for git-based dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["py", "-m", "api.main"]