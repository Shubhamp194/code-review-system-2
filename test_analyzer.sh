#!/bin/bash

# Test script for AI Code Review System

echo "🚀 AI Code Review System - Test Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -q -r requirements.txt

echo ""
echo "========================================"
echo "Test 1: List all rules"
echo "========================================"
python -m src.analyzer.main rules

echo ""
echo "========================================"
echo "Test 2: Analyze BadCode.java (should find violations)"
echo "========================================"
python -m src.analyzer.main file sample-java-project/src/main/java/com/ibm/demo/BadCode.java --show-code

echo ""
echo "========================================"
echo "Test 3: Analyze GoodCode.java (should be clean)"
echo "========================================"
python -m src.analyzer.main file sample-java-project/src/main/java/com/ibm/demo/GoodCode.java --show-code

echo ""
echo "========================================"
echo "Test 4: Analyze entire project"
echo "========================================"
python -m src.analyzer.main project sample-java-project --output test-results.json

echo ""
echo "========================================"
echo "✅ Tests completed!"
echo "========================================"
echo ""
echo "Results saved to: test-results.json"
echo ""
echo "To run manually:"
echo "  source venv/bin/activate"
echo "  python -m src.analyzer.main --help"

# Made with Bob
