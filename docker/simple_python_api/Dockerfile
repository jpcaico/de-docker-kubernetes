#imports a Python container based on the alpine Linux distribution.
FROM python:3.11-alpine
#installs fastapi and uvicorn
RUN pip3 --no-cache-dir install fastapi uvicorn
#listen on port 8087 at runtime
EXPOSE 8087
#copies all the code inside our local /app folder to a /app folder inside the container
COPY ./api /api
# specifies the command to run when the container starts.
CMD uvicorn api.main:app --host 0.0.0.0 --port 8087