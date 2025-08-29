# Dockerfile (additions for hard flag)
FROM python:3.11-slim
WORKDIR /app

# Copy your servers (existing ones + new HTTPS)
COPY HTTPServer.py TCPServer.py fakeports.py HTTPSServer_hard.py supervisord.conf ./

# Install supervisor + openssl and make a self-signed cert
RUN apt-get update && apt-get install -y --no-install-recommends openssl && rm -rf /var/lib/apt/lists/*

# The flag is embedded in CN and SAN so ssl-cert script prints it
RUN openssl req -x509 -newkey rsa:2048 -days 365 -nodes \
  -keyout /app/key.pem -out /app/cert.pem \
  -subj "/CN=flag{tls_certificate_hunter}/O=Root@UT-CTF" \
  -addext "subjectAltName=DNS:ctf.local,DNS:flag{tls_certificate_hunter}"

# Expose ports
EXPOSE 8080 2222 8443

# Supervisor entrypoint (matches your existing pattern)
RUN pip install --no-cache-dir supervisor
CMD ["supervisord", "-c", "/app/supervisord.conf"]
