# Entry point for the cross-platform action agent
import sys
import asyncio
from llm_parser import parse_instruction
from providers.gmail import GmailProvider
from providers.outlook import OutlookProvider
from logger import StepLogger

class CrossPlatformAgent:
    def __init__(self):
        self.logger = StepLogger()
        self.providers = {
            'gmail': GmailProvider(self.logger),
            'outlook': OutlookProvider(self.logger)
        }
    
    async def execute_instruction(self, instruction: str, provider_choice: str = None):
        """
        Main execution flow:
        1. Parse natural language instruction
        2. Select provider(s)
        3. Execute action via provider
        """
        self.logger.log(f"Received instruction: {instruction}")
        
        # Parse instruction using LLM/mock parser
        parsed = parse_instruction(instruction)
        self.logger.log(f"Parsed instruction: {parsed}")
        
        if parsed['action'] != 'send_email':
            self.logger.log(f"Unsupported action: {parsed['action']}")
            return False
        
        # Select provider(s)
        if provider_choice and provider_choice in self.providers:
            selected_providers = [provider_choice]
        elif provider_choice == 'both':
            selected_providers = ['gmail', 'outlook']
        else:
            # Default to both providers
            selected_providers = ['gmail', 'outlook']
        
        # Execute action for each provider
        success = True
        for provider_name in selected_providers:
            try:
                self.logger.log(f"Starting {provider_name} automation...")
                provider = self.providers[provider_name]
                await provider.send_email(
                    to=parsed['to'],
                    subject=parsed['subject'],
                    body=parsed['body']
                )
                self.logger.log(f"Successfully completed {provider_name} automation")
            except Exception as e:
                self.logger.log(f"Error with {provider_name}: {str(e)}")
                success = False
        
        return success

async def main():
    """CLI entry point"""
    agent = CrossPlatformAgent()
    
    if len(sys.argv) > 1:
        # Command line argument
        instruction = " ".join(sys.argv[1:])
        await agent.execute_instruction(instruction)
    else:
        # Interactive mode
        print("Cross-Platform Email Agent")
        print("Example: 'Send an email to john@example.com about the project deadline'")
        print("Type 'quit' to exit\n")
        
        while True:
            instruction = input("Enter instruction: ")
            if instruction.lower() in ['quit', 'exit']:
                break
            
            if instruction.strip():
                await agent.execute_instruction(instruction)
                print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
