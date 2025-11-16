#!/bin/bash
# Script to run all backend tests with coverage

echo "🧪 Running Backend Tests..."
echo "================================"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run pytest with coverage
pytest

# Check exit code
if [ $? -eq 0 ]; then
    echo "================================"
    echo "✅ All tests passed!"
    echo "📊 Coverage report generated in htmlcov/"
else
    echo "================================"
    echo "❌ Tests failed!"
    exit 1
fi
