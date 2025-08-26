# 1) Start from a tiny Python image
FROM python:3.11-slim

# 2) Put us in /app inside the image
WORKDIR /app

# 3) Copy dependency list first (better build cache)
COPY requirements.txt .

# 4) Install only what's needed (requirements.txt will install flask) the rest installs for the tcp banner server
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && apt-get update && apt-get install -y --no-install-recommends supervisor \
 && rm -rf /var/lib/apt/lists/*

# 5) Copy your app code
COPY HTTPserver.py TCPserver.py fakeports.py supervisord.conf ./

# 6) Document that the app listens on 80 (for humans/tools)
EXPOSE 80 1337

# 7) Command the container runs when it starts
CMD ["supervisord", "-c", "/app/supervisord.conf"]
