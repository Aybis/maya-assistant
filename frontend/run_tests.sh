#!/bin/bash
# Script to run all frontend tests with coverage

echo "🧪 Running Frontend Tests..."
echo "================================"

# Run vitest with coverage
npm run test:coverage

# Check exit code
if [ $? -eq 0 ]; then
    echo "================================"
    echo "✅ All tests passed!"
    echo "📊 Coverage report generated in coverage/"
else
    echo "================================"
    echo "❌ Tests failed!"
    exit 1
fi
