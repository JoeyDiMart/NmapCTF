#  install image for Python
FROM python:3.11-slim

WORKDIR /app

COPY start_ctf.py .

EXPOSE
CMD ["python", "start_ctf.py"]


