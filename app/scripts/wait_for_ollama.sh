#!/bin/bash

echo "Aguardando Ollama estar disponível em $OLLAMA_URL..."

until curl -s "$OLLAMA_URL/tags" > /dev/null; do
  echo "Esperando Ollama iniciar..."
  sleep 5
done

echo "Ollama está pronto. Iniciando Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 wsgi:application
