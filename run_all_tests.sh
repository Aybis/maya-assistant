#!/bin/bash
# Master script to run all tests (Backend + Frontend)

echo "════════════════════════════════════════════════════════════"
echo "  🚀 Maya Assistant - Complete Test Suite Runner"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BACKEND_PASSED=0
FRONTEND_PASSED=0

# Function to run backend tests
run_backend_tests() {
    echo "┌────────────────────────────────────────────────────────────┐"
    echo "│  📦 BACKEND TESTS (Python/FastAPI)                        │"
    echo "└────────────────────────────────────────────────────────────┘"
    echo ""

    cd backend

    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Install dependencies if needed
    if ! pip show pytest &> /dev/null; then
        echo "${YELLOW}📥 Installing test dependencies...${NC}"
        pip install -q -r requirements.txt
    fi

    # Run tests
    pytest

    if [ $? -eq 0 ]; then
        BACKEND_PASSED=1
        echo ""
        echo "${GREEN}✅ Backend tests passed!${NC}"
    else
        echo ""
        echo "${RED}❌ Backend tests failed!${NC}"
    fi

    deactivate
    cd ..
    echo ""
}

# Function to run frontend tests
run_frontend_tests() {
    echo "┌────────────────────────────────────────────────────────────┐"
    echo "│  🎨 FRONTEND TESTS (Next.js/TypeScript)                   │"
    echo "└────────────────────────────────────────────────────────────┘"
    echo ""

    cd frontend

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "${YELLOW}⚠️  Dependencies not found. Installing...${NC}"
        npm install
    fi

    # Run tests
    npm run test:coverage

    if [ $? -eq 0 ]; then
        FRONTEND_PASSED=1
        echo ""
        echo "${GREEN}✅ Frontend tests passed!${NC}"
    else
        echo ""
        echo "${RED}❌ Frontend tests failed!${NC}"
    fi

    cd ..
    echo ""
}

# Run all tests
run_backend_tests
run_frontend_tests

# Summary
echo "════════════════════════════════════════════════════════════"
echo "  📊 TEST SUMMARY"
echo "════════════════════════════════════════════════════════════"
echo ""

if [ $BACKEND_PASSED -eq 1 ]; then
    echo "${GREEN}✅ Backend Tests: PASSED${NC}"
else
    echo "${RED}❌ Backend Tests: FAILED${NC}"
fi

if [ $FRONTEND_PASSED -eq 1 ]; then
    echo "${GREEN}✅ Frontend Tests: PASSED${NC}"
else
    echo "${RED}❌ Frontend Tests: FAILED${NC}"
fi

echo ""
echo "Coverage Reports:"
echo "  📁 Backend:  backend/htmlcov/index.html"
echo "  📁 Frontend: frontend/coverage/index.html"
echo ""

# Exit with error if any tests failed
if [ $BACKEND_PASSED -eq 1 ] && [ $FRONTEND_PASSED -eq 1 ]; then
    echo "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo "${GREEN}  🎉 ALL TESTS PASSED! 🎉${NC}"
    echo "${GREEN}════════════════════════════════════════════════════════════${NC}"
    exit 0
else
    echo "${RED}════════════════════════════════════════════════════════════${NC}"
    echo "${RED}  ⚠️  SOME TESTS FAILED${NC}"
    echo "${RED}════════════════════════════════════════════════════════════${NC}"
    exit 1
fi
