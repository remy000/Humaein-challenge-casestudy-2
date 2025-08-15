# Cross-Platform Action Agent

> **AI-Powered Email Automation Across Multiple Platforms**

A sophisticated automation system that uses natural language processing and browser automation to send emails across different web-based email services (Gmail, Outlook, and more). Built with Python, Playwright, and FastAPI.

## Table of Contents

- [Overview](#-overview)
- [Features](#-features) 
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Demo Mode](#-demo-mode)
- [API Documentation](#-api-documentation)

---

## Overview

The Cross-Platform Action Agent solves the challenge of automating email workflows across different web-based email platforms. Instead of writing separate automation scripts for each email service, this system provides a unified interface that can:

- **Understand natural language instructions** like "Send email to alice@company.com about the quarterly review"
- **Automatically navigate** different email interfaces (Gmail, Outlook Web, etc.)
- **Work with any email service** through intelligent UI analysis
- **Provide unified interface** across multiple email providers

### Challenge Requirements Met

This system was built to address a technical challenge with the following requirements:

 **Accept natural language instructions**  
 **Use LLM/mocked reasoning for instruction interpretation**  
 **Browser automation with DOM interaction**  
 **Support multiple providers with different DOM structures**  
 **Abstract provider-specific logic behind unified interface**  
 **Step-by-step logging**
 **Generic UI Agent for any service**
 **CLI interface**
 **FastAPI REST endpoint**

**AI Field Matching**: Semantic element discovery in DOM handler

## Features

### **Core Capabilities**
- **Natural Language Processing**: Convert plain English to email actions
- **Multi-Platform Support**: Gmail, Outlook Web, and extensible to others
- **Browser Automation**: Automated web interaction using Playwright
- **Authentication Handling**: Smart authentication with fallback strategies

### **Advanced Features**
- **Generic UI Agent**: Works with any email service automatically
- **Comprehensive Logging**: Track every step of the automation
- **API Integration**: REST API for business applications
- **Mock Mode**: Safe demo mode for presentations

## Challenge Implementation

This project implements a **Cross-Platform Action Agent** that executes email tasks across multiple web UIs using:
- Natural language processing
- Browser automation (Playwright)
- Provider abstraction
- LLM-guided element discovery

## Project Structure

```
cross-platform-agent/
├── agent.py                # Main entry point & CLI interface
├── demo.py                 # Safe demo for presentations
├── llm_parser.py           # Natural language instruction parser
├── logger.py               # Step-by-step logging system
├── providers/
│   ├── __init__.py
│   ├── gmail.py            # Gmail automation logic
│   └── outlook.py          # Outlook Web automation logic
├── api_server.py           # FastAPI REST endpoint
├── generic_ui_agent.py     # Universal UI agent (experimental)
├── requirements.txt        # Dependencies
└── README.md               # This documentation
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m playwright install

# 2. Run demo (recommended)
python demo.py

# 3. Run interactive agent
python agent.py
```

## Features

### **Core Features (Required)**
- Natural language instruction parsing
- Multi-provider support (Gmail + Outlook)
- Browser automation with Playwright
- Unified provider interface
- Comprehensive error handling

### **Stretch Goals (Implemented)**
- Step-by-step logging
- CLI interface
- Generic UI agent class
- LLM + DOM tree analysis
- Screenshot analysis for debugging
- FastAPI REST endpoint

## Installation

```bash
pip install -r requirements.txt
python -m playwright install
```

## Usage

### **1. Console Demo Mode (Recommended for Presentations)**
```bash
# Shows complete workflow simulation in console only
python demo.py

# Single instruction demo
python demo.py "Send email to john@example.com about the project deadline"
```
**Perfect for:**
-  Presentations and demonstrations
-  Understanding the system workflow
-  Testing without browser dependencies
-  Safe execution without actual email composition
-  **NO BROWSER WINDOWS** - console output only

### **2. Browser Automation Mode (Real Automation)**
```bash
# Basic usage with real browser automation
python agent.py "Send email to john@example.com about the project deadline"

# Interactive mode
python agent.py
```

** How it works:**
- **SENDER**: Uses the Gmail/Outlook account you're logged into in the browser
- **RECEIVER**: Extracts email address from your instruction (e.g., "john@example.com")
- **SUBJECT & BODY**: Generated automatically from your instruction content
- **BROWSER**: Opens actual browser windows and automates email composition

### **3. REST API Endpoint**
```bash
# Start the API server
python api_server.py

# Use the API
curl -X POST "http://localhost:8088/send-email" \
     -H "Content-Type: application/json" \
     -d '{"instruction": "send email to test@example.com saying Hello from API"}'
```

### **4. Generic UI Agent**
```python
from generic_ui_agent import GenericUIAgent

agent = GenericUIAgent()
await agent.execute_email_task("https://mail.google.com", "send email to alice@company.com about meeting")
```

##  Safety Features

- **Email sending disabled by default** for demo safety
- **Mock fallbacks** when automation fails
- **Comprehensive logging** for transparency
- **Error recovery** with graceful degradation

## Architecture Highlights

- **Modular Design**: Easy to extend with new providers
- **Provider Abstraction**: Unified interface across different email services
- **LLM Integration**: Intelligent element discovery and field matching
- **Production Ready**: Robust error handling and logging

##  Example Instructions

- `"Send email to alice@company.com about the quarterly review meeting"`
- `"Email john.doe@startup.com regarding the project deadline extension"`
- `"Send a message to team@example.com saying 'Hello from automation'"`

### ** Email Flow Explanation:**

**Sender (FROM)**: The currently logged-in user in Gmail/Outlook browser
**Receiver (TO)**: Extracted from your natural language instruction

**Example:**
```bash
python agent.py "Send email to alice@company.com about project update"
```
- ** FROM**: your-account@gmail.com (whoever is logged into Gmail)
- ** TO**: alice@company.com (extracted from instruction)  
- ** SUBJECT**: "Project Update" (extracted from instruction)
- ** BODY**: Auto-generated message about the project update

##  Demo

### **For Presentations: Use Demo Mode**
```bash
python demo.py
```

**What the demo shows:**
1. **Natural Language Parsing** - Converts instructions to structured data
2. **Provider Selection** - Chooses Gmail and Outlook automatically  
3. **Simulated Automation** - Shows each step the real system would perform
4. **Complete Workflow** - End-to-end process without browser windows
5. **Error-Free Experience** - No login issues or network dependencies

**Example demo output:**
```
 DEMO 1/3
[STEP] PROCESSING INSTRUCTION: Send email to alice@company.com about quarterly review
[STEP] ✓ Parsed - To: alice@company.com
[STEP] ✓ Parsed - Subject: Quarterly Review  
[STEP] [Gmail] Launching browser for Gmail
[STEP] [Gmail] Filling recipient: alice@company.com
[STEP] [Gmail] Email composed successfully
[STEP] [Outlook Web] Email composed successfully
[STEP] INSTRUCTION COMPLETED SUCCESSFULLY
```

### **For Browser Automation: Use Main Agent**
The main agent automatically:
1. **Parses** your natural language instruction
2. **Opens** browsers for Gmail and Outlook
3. **Navigates** to compose email
4. **Fills** recipient, subject, and body fields
5. **Shows** the composed email (sending disabled for safety)

## Advanced Features

- **Generic Agent**: Works with any email service URL
- **LLM Analysis**: Uses AI to understand and navigate UIs
- **API Interface**: Full REST API for integration
- **Screenshot Analysis**: Visual debugging for failures

---


### 🎯 **Best Practices**

1. **Start with demo mode**: `python demo.py` - perfect for understanding the system
2. **Use for presentations**: Demo mode shows all capabilities without authentication issues
3. **Browser automation**: Shows DOM interaction and provider abstraction concepts
4. **Check logs**: Console output shows detailed step-by-step progress
5. **Test components**: Run files separately for debugging

### 💡 **Pro Tips**

- **Demo mode** demonstrates the complete architecture perfectly
- **Browser automation** shows cross-platform UI interaction capabilities
- **Provider abstraction** makes it easy to add new email services
- **For production deployment** - extend with additional email service providers

---
