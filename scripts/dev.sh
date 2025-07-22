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

# Run API server in background
run-api() {
    echo "Starting API server in background..."
    echo "Logs will be written to api_server.log"
    echo "To stop the server, use: pkill -f 'uv run python scripts/start_api.py'"
    
    # Create logs directory if it doesn't exist
    mkdir -p logs
    
    # Run the API server in background with nohup
    nohup uv run python scripts/start_api.py > logs/api_server.log 2>&1 &
    
    # Save the process ID
    echo $! > logs/api_server.pid
    
    echo "API server started with PID: $(cat logs/api_server.pid)"
    echo "Check logs with: tail -f logs/api_server.log"
}

# Stop API server
stop-api() {
    if [ -f logs/api_server.pid ]; then
        PID=$(cat logs/api_server.pid)
        if ps -p $PID > /dev/null 2>&1; then
            echo "Stopping API server (PID: $PID)..."
            kill $PID
            rm logs/api_server.pid
            echo "API server stopped"
        else
            echo "API server is not running"
            rm logs/api_server.pid
        fi
    else
        echo "No API server PID file found"
    fi
}

# Check API server status
status-api() {
    if [ -f logs/api_server.pid ]; then
        PID=$(cat logs/api_server.pid)
        if ps -p $PID > /dev/null 2>&1; then
            echo "API server is running (PID: $PID)"
            echo "Log file: logs/api_server.log"
        else
            echo "API server is not running (stale PID file)"
            rm logs/api_server.pid
        fi
    else
        echo "API server is not running"
    fi
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
    echo "  run-api      - Start API server in background"
    echo "  stop-api     - Stop API server"
    echo "  status-api   - Check API server status"
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
    run-api)
        run-api
        ;;
    stop-api)
        stop-api
        ;;
    status-api)
        status-api
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