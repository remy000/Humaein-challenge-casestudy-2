# Mocked LLM parser for natural language instructions
import re

def parse_instruction(instruction: str) -> dict:
    """
    Parses a natural language instruction and returns a dict with action details.
    Uses simple regex patterns to extract email components.
    """
    instruction_lower = instruction.lower()
    
    # Extract recipient (to field)
    to_patterns = [
        r"send.*?email.*?to\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        r"email\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        r"to\s+([a-zA-Z@.]+)",
        r"send.*?to\s+(\w+)"
    ]
    
    recipient = "example@email.com"  # default
    for pattern in to_patterns:
        match = re.search(pattern, instruction_lower)
        if match:
            recipient = match.group(1)
            break
    
    # Extract subject from context
    subject_patterns = [
        r"about\s+(.+?)(?:\.|$)",
        r"regarding\s+(.+?)(?:\.|$)",
        r"subject\s+(.+?)(?:\.|$)"
    ]
    
    subject = "Automated Message"  # default
    for pattern in subject_patterns:
        match = re.search(pattern, instruction_lower)
        if match:
            subject = match.group(1).strip()
            break
    
    # Generate body based on instruction
    body = f"Hello,\n\nThis is an automated message regarding: {subject}\n\nBest regards"
    
    return {
        "action": "send_email",
        "to": recipient,
        "subject": subject.title(),
        "body": body
    }
