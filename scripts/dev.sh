#!/bin/bash
# Author: Peng Fei
# Development scripts for job requirement generator

# Install dependencies
install() {
    echo "Installing dependencies with uv..."
    uv sync
}

# Run the application
run() {
    echo "Running job requirement generator..."
    uv run main.py
}

# Run tests
test() {
    echo "Running tests..."
    uv run pytest
}

# Format code
format() {
    echo "Formatting code with black..."
    uv run black .
}

# Lint code
lint() {
    echo "Linting code with flake8..."
    uv run flake8 .
}

# Install dev dependencies
install-dev() {
    echo "Installing development dependencies..."
    uv sync --extra dev
}

# Show help
help() {
    echo "Available commands:"
    echo "  install      - Install dependencies"
    echo "  install-dev  - Install development dependencies"
    echo "  run          - Run the application"
    echo "  test         - Run tests"
    echo "  format       - Format code"
    echo "  lint         - Lint code"
    echo "  help         - Show this help"
}

# Main script logic
case "${1:-help}" in
    install)
        install
        ;;
    install-dev)
        install-dev
        ;;
    run)
        run
        ;;
    test)
        test
        ;;
    format)
        format
        ;;
    lint)
        lint
        ;;
    help|*)
        help
        ;;
esac 