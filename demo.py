"""
Cross-Platform Email Agent - Console Demo Mode

This demo shows the complete workflow without browser automation.
Perfect for presentations and understanding system capabilities.
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_parser import parse_instruction
from logger import StepLogger

class DemoAgent:
    """Demo version showing workflow without browser automation"""
    
    def __init__(self):
        self.logger = StepLogger()
        
    def demo_instruction(self, instruction):
        """Demonstrate the complete workflow for one instruction"""
        self.logger.log("="*60)
        self.logger.log(f"PROCESSING: {instruction}")
        self.logger.log("="*60)
        
        # Step 1: Parse instruction
        self.logger.log("Step 1: Parsing natural language...")
        parsed = parse_instruction(instruction)
        self.logger.log(f"To: {parsed['to']}")
        self.logger.log(f"Subject: {parsed['subject']}")
        self.logger.log(f"Body: {parsed['body'][:60]}...")
        
        # Step 2: Provider selection
        self.logger.log("\nStep 2: Selecting email providers...")
        providers = ['Gmail', 'Outlook Web']
        for provider in providers:
            self.logger.log(f"Selected: {provider}")
        # Step 3: Simulate automation
        for provider in providers:
            self.logger.log(f"\nStep 3: Simulating {provider} automation...")
            self._simulate_provider_automation(provider, parsed)
        
        self.logger.log(f"\n{'='*60}")
        self.logger.log("INSTRUCTION COMPLETED SUCCESSFULLY")
        self.logger.log("="*60)
        
    def _simulate_provider_automation(self, provider_name, parsed_data):
        """Simulate the automation steps for one provider"""
        automation_steps = [
            "Launching browser",
            f"Navigating to {provider_name.lower().replace(' ', '')}.com", 
            "Checking authentication",
            "Finding compose button",
            "Clicking compose",
            f"Filling recipient: {parsed_data['to']}",
            f"Filling subject: {parsed_data['subject']}",
            f"Filling message body: {parsed_data['body']}",
            "Email composed successfully",
            f"Ready to send via {provider_name}"
        ]
        for step in automation_steps:
            self.logger.log(f"[{provider_name}] {step}")
            time.sleep(0.1)  # Brief pause for readability

def run_comprehensive_demo():
    """Run multiple demo scenarios"""
    print("\n Cross-Platform Email Agent - Comprehensive Demo")
    print("=" * 65)
    print("This demonstrates the complete workflow without browser automation")
    print("Perfect for presentations and system understanding")
    print("=" * 65)
    
    agent = DemoAgent()
    
    # Demo scenarios
    scenarios = [
        "Send an email to alice@company.com about the quarterly review meeting",
        "Email john.doe@startup.com regarding the project deadline extension",
        "Send a message to team@example.com about the system maintenance window"
    ]
    
    for i, instruction in enumerate(scenarios, 1):
        print(f"\n DEMO SCENARIO {i}/3")
        print("-" * 50)
        agent.demo_instruction(instruction)
        
        if i < len(scenarios):
            print(f"\n{'-' * 80}")
            time.sleep(0.5)
    
    print(f"\n All demo scenarios completed!")
    print("\n Next Steps:")
    print("For real automation: python agent.py 'your instruction'")
    print("For API access: python api_server.py")
    print("For interactive mode: python agent.py")

async def main():
    """Main entry point for demo"""
    if len(sys.argv) > 1:
        # Single instruction demo
        instruction = " ".join(sys.argv[1:])
        print(" Console Demo Mode - Single Instruction")
        print("=" * 50)
        print("This shows the workflow without opening browsers")
        print("=" * 50)
        agent = DemoAgent()
        agent.demo_instruction(instruction)
    else:
        # Comprehensive demo
        run_comprehensive_demo()

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n Demo interrupted by user")
    except Exception as e:
        print(f"\ns Demo error: {e}")
        import traceback
        traceback.print_exc()
