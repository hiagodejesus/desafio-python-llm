#!/bin/bash

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Verificando se Ollama está instalado..."

if ! command_exists ollama; then
    echo "Ollama não encontrado. Por favor, instale antes."
    exit 1
fi

echo "Fazendo pull do modelo 'gemma'..."
ollama pull gemma:2b

echo "Iniciando o modelo 'gemma' em background..."
nohup ollama run gemma:2b > ollama_gemma.log 2>&1 &

echo "Ollama rodando com modelo 'gemma' em background."
echo "Veja o log em ollama_gemma.log"

cat ollama_mistral.log
