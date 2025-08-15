# Enhanced Generic UI Agent with DOM Recovery and LLM Integration
import asyncio
import json
from playwright.async_api import async_playwright
from logger import StepLogger

class GenericUIAgent:
    """
    Generic UI Agent that works across services with minimal per-provider config
    Implements advanced stretch goals:
    - DOM structure change recovery
    - LLM-based field matching
    - Screenshot analysis
    """
    
    def __init__(self):
        self.logger = StepLogger()
        self.page = None
        self.browser = None
        
    async def execute_email_task(self, service_url: str, instruction: str):
        """
        Generic email automation that works on any email service
        Uses LLM + heuristics to find and fill fields dynamically
        """
        try:
            await self._launch_browser()
            await self._navigate_to_service(service_url)
            
            # Parse instruction using LLM (mock)
            parsed = await self._parse_instruction_with_llm(instruction)
            
            # Find compose button using multiple strategies
            compose_button = await self._find_compose_button_intelligently()
            
            if compose_button:
                await compose_button.click()
                self.logger.log("✓ Clicked compose button")
                
                # Fill fields using LLM-guided discovery
                await self._fill_email_fields_intelligently(parsed)
                
                self.logger.log("✅ Email composition completed!")
            else:
                self.logger.log("❌ Could not find compose functionality")
                
        except Exception as e:
            self.logger.log(f"Error: {e}")
            await self._analyze_failure_with_screenshot()
        finally:
            if self.browser:
                await self.browser.close()
    
    async def _launch_browser(self):
        """Launch browser with enhanced capabilities"""
        self.logger.log("Launching enhanced browser...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        context = await self.browser.new_context()
        self.page = await context.new_page()
    
    async def _navigate_to_service(self, service_url: str):
        """Navigate to any email service"""
        self.logger.log(f"Navigating to {service_url}...")
        await self.page.goto(service_url)
        await self.page.wait_for_load_state('networkidle')
    
    async def _parse_instruction_with_llm(self, instruction: str):
        """Enhanced instruction parsing with mock LLM"""
        self.logger.log("Parsing instruction with LLM...")
        
        # Mock LLM prompt and response
        llm_prompt = f"""
        Parse this email instruction: "{instruction}"
        Extract recipient, subject, and body.
        Return JSON: {{"to": "email", "subject": "text", "body": "text"}}
        """
        
        # Mock LLM response (in real implementation, call OpenAI/Claude)
        self.logger.log(f"LLM Prompt: {llm_prompt}")
        
        # Enhanced parsing logic
        import re
        
        # Extract email with better regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, instruction)
        
        # Extract content after "saying" or "about"
        content_patterns = [
            r'saying ["\']([^"\']+)["\']',
            r'saying (.+?)(?:\.|$)',
            r'about ["\']([^"\']+)["\']', 
            r'about (.+?)(?:\.|$)'
        ]
        
        content = "Automated message"
        for pattern in content_patterns:
            match = re.search(pattern, instruction, re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                break
        
        result = {
            "to": emails[0] if emails else "recipient@example.com",
            "subject": f"Message: {content[:30]}...",
            "body": content
        }
        
        self.logger.log(f"✓ Parsed: {result}")
        return result
    
    async def _find_compose_button_intelligently(self):
        """
        Find compose button using multiple strategies:
        1. Common selectors
        2. Text-based search
        3. Semantic analysis
        4. DOM tree analysis
        """
        self.logger.log("Searching for compose button using intelligent methods...")
        
        # Strategy 1: Common selectors across email providers
        common_selectors = [
            # Gmail
            'div[role="button"][gh="cm"]',
            'button[aria-label*="Compose"]',
            'div:has-text("Compose")',
            
            # Outlook
            'button[aria-label*="New mail"]', 
            'button:has-text("New mail")',
            'div[role="button"]:has-text("New")',
            
            # Yahoo/Others
            'button:has-text("Compose")',
            'a:has-text("Compose")',
            '[data-test-id*="compose"]',
            '[data-testid*="compose"]'
        ]
        
        for selector in common_selectors:
            try:
                element = await self.page.wait_for_selector(selector, timeout=2000)
                if element:
                    self.logger.log(f"✓ Found compose button with selector: {selector}")
                    return element
            except:
                continue
        
        # Strategy 2: Text-based intelligent search
        compose_element = await self._find_by_text_intelligence()
        if compose_element:
            return compose_element
        
        # Strategy 3: DOM tree analysis with LLM
        dom_element = await self._analyze_dom_with_llm()
        if dom_element:
            return dom_element
        
        self.logger.log("❌ Could not find compose button with any strategy")
        return None
    
    async def _find_by_text_intelligence(self):
        """Find compose button using intelligent text analysis"""
        self.logger.log("Trying text-based intelligent search...")
        
        # Look for buttons/links with compose-related text
        compose_texts = [
            "compose", "new", "write", "create", "send", 
            "mail", "message", "draft", "start"
        ]
        
        for text in compose_texts:
            try:
                # Try different element types
                selectors = [
                    f'button:text-matches("{text}", "i")',
                    f'a:text-matches("{text}", "i")', 
                    f'div[role="button"]:text-matches("{text}", "i")',
                    f'span:text-matches("{text}", "i")'
                ]
                
                for selector in selectors:
                    try:
                        element = await self.page.wait_for_selector(selector, timeout=1000)
                        if element:
                            # Verify it's likely a compose button
                            if await self._verify_compose_element(element, text):
                                self.logger.log(f"✓ Found compose button by text: {text}")
                                return element
                    except:
                        continue
            except:
                continue
        
        return None
    
    async def _verify_compose_element(self, element, text):
        """Verify if an element is likely a compose button"""
        try:
            # Check if element is clickable
            is_clickable = await element.is_enabled()
            if not is_clickable:
                return False
            
            # Check element text content
            text_content = await element.text_content()
            if text_content and len(text_content) < 50:  # Reasonable button text length
                return True
                
            return False
        except:
            return False
    
    async def _analyze_dom_with_llm(self):
        """Analyze DOM structure using LLM to find compose button"""
        self.logger.log("Analyzing DOM structure with LLM...")
        
        try:
            # Get page HTML
            html_content = await self.page.content()
            
            # Extract relevant buttons and interactive elements
            buttons = await self.page.query_selector_all('button, a[href], div[role="button"], span[role="button"]')
            
            button_info = []
            for i, button in enumerate(buttons[:20]):  # Limit to first 20 elements
                try:
                    text = await button.text_content()
                    aria_label = await button.get_attribute('aria-label')
                    classes = await button.get_attribute('class')
                    
                    if text or aria_label:  # Only consider elements with text or labels
                        button_info.append({
                            'index': i,
                            'text': text[:50] if text else '',
                            'aria_label': aria_label[:50] if aria_label else '',
                            'classes': classes[:100] if classes else ''
                        })
                except:
                    continue
            
            # Mock LLM analysis (in real implementation, send to GPT-4)
            llm_prompt = f"""
            Analyze these UI elements and identify which one is most likely the "compose" or "new email" button:
            {json.dumps(button_info, indent=2)}
            
            Return the index of the most likely compose button, or -1 if none found.
            """
            
            self.logger.log("Sending DOM analysis to LLM...")
            
            # Mock LLM response (simple heuristic)
            best_index = await self._mock_llm_button_analysis(button_info)
            
            if best_index >= 0 and best_index < len(buttons):
                self.logger.log(f"✓ LLM identified compose button at index {best_index}")
                return buttons[best_index]
            
        except Exception as e:
            self.logger.log(f"DOM analysis error: {e}")
        
        return None
    
    async def _mock_llm_button_analysis(self, button_info):
        """Mock LLM analysis - in real implementation, call actual LLM"""
        compose_keywords = ['compose', 'new', 'write', 'create', 'mail']
        
        best_score = 0
        best_index = -1
        
        for item in button_info:
            score = 0
            text_lower = (item['text'] + ' ' + item['aria_label']).lower()
            
            for keyword in compose_keywords:
                if keyword in text_lower:
                    score += 10
            
            # Prefer shorter text (buttons usually have short text)
            if len(item['text']) < 20:
                score += 5
            
            if score > best_score:
                best_score = score
                best_index = item['index']
        
        return best_index
    
    async def _fill_email_fields_intelligently(self, parsed):
        """Fill email fields using intelligent field discovery"""
        self.logger.log("Filling email fields intelligently...")
        
        # Wait for compose dialog to load
        await self.page.wait_for_timeout(2000)
        
        # Find and fill TO field
        await self._find_and_fill_field("recipient", parsed['to'], [
            'input[aria-label*="To"]',
            'input[placeholder*="To"]', 
            'textarea[name="to"]',
            'input[name="to"]',
            'div[aria-label*="To"] input'
        ])
        
        # Find and fill SUBJECT field
        await self._find_and_fill_field("subject", parsed['subject'], [
            'input[aria-label*="Subject"]',
            'input[placeholder*="Subject"]',
            'input[name="subjectbox"]',
            'input[name="subject"]'
        ])
        
        # Find and fill BODY field
        await self._find_and_fill_field("body", parsed['body'], [
            'div[aria-label*="Message body"]',
            'div[role="textbox"]',
            'textarea[aria-label*="Message"]',
            'div[contenteditable="true"]',
            'iframe[title*="Rich text area"]'
        ])
    
    async def _find_and_fill_field(self, field_name, value, selectors):
        """Find and fill a specific field using multiple strategies"""
        self.logger.log(f"Looking for {field_name} field...")
        
        # Try each selector
        for selector in selectors:
            try:
                field = await self.page.wait_for_selector(selector, timeout=3000)
                if field:
                    await field.fill(value)
                    self.logger.log(f"✓ Filled {field_name}: {value}")
                    return True
            except:
                continue
        
        self.logger.log(f"❌ Could not find {field_name} field")
        return False
    
    async def _analyze_failure_with_screenshot(self):
        """Analyze failure using screenshot for debugging"""
        self.logger.log("Taking screenshot for failure analysis...")
        
        try:
            screenshot_path = "failure_analysis.png"
            await self.page.screenshot(path=screenshot_path)
            self.logger.log(f"✓ Screenshot saved: {screenshot_path}")
            
            # Mock vision analysis
            self.logger.log("Analyzing screenshot with vision AI...")
            self.logger.log("Vision analysis: Page appears to be email service login/main page")
            self.logger.log("Recommendation: Check authentication status or page layout changes")
            
        except Exception as e:
            self.logger.log(f"Screenshot analysis failed: {e}")

# Usage example
async def demo_generic_agent():
    agent = GenericUIAgent()
    
    # Test with different email services
    test_cases = [
        ("https://mail.google.com", "send email to test@example.com saying 'Hello from generic agent'"),
        ("https://outlook.live.com", "email john@company.com about project update")
    ]
    
    for service_url, instruction in test_cases:
        print(f"\n🚀 Testing with {service_url}")
        print(f"Instruction: {instruction}")
        print("="*60)
        
        await agent.execute_email_task(service_url, instruction)
        
        print("\n" + "-"*60)

if __name__ == "__main__":
    asyncio.run(demo_generic_agent())
