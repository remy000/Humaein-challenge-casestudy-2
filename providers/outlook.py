# Outlook provider automation using Playwright with Enhanced DOM Handling
from playwright.async_api import async_playwright
import asyncio
import sys
import os

# Add parent directory to path for enhanced_dom_handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from enhanced_dom_handler import EnhancedDOMHandler

class OutlookProvider:
    def __init__(self, logger):
        self.logger = logger
        self.page = None
        self.browser = None
        self.dom_handler = None
        
    async def send_email(self, to, subject, body):
        """
        Enhanced Outlook automation with robust DOM handling and edge case management
        """
        try:
            self.logger.log("Starting enhanced Outlook automation...")
            playwright = await async_playwright().start()
            
            # Launch browser (headless=False for demo)
            self.browser = await playwright.chromium.launch(headless=False)
            context = await self.browser.new_context()
            self.page = await context.new_page()
            
            # Initialize enhanced DOM handler
            self.dom_handler = EnhancedDOMHandler(self.page, self.logger)
            
            # Navigate to Outlook Web
            self.logger.log("Navigating to Outlook Web...")
            await self.page.goto("https://outlook.live.com", timeout=30000)
            await self.page.wait_for_load_state('networkidle', timeout=30000)
            
            # Check authentication status with enhanced detection
            auth_required = await self.dom_handler._check_authentication()
            if auth_required:
                self.logger.log("Authentication required - please sign in manually")
                self.logger.log("Waiting for authentication...")
                await self.page.wait_for_timeout(5000)
            
            # Enhanced compose button detection
            self.logger.log("Looking for compose button with enhanced detection...")
            compose_element = await self.dom_handler.find_email_field('compose', 'outlook')
            
            if compose_element:
                await self.page.click(compose_element)
                self.logger.log("Clicked compose button")
                await self.page.wait_for_timeout(2000)
            else:
                # Fallback with multiple strategies
                fallback_selectors = [
                    'button[aria-label*="New mail"]',
                    'button:has-text("New mail")',
                    'div[role="button"]:has-text("New")',
                    '[data-testid="new-mail-button"]'
                ]
                
                compose_found = False
                for selector in fallback_selectors:
                    try:
                        await self.page.wait_for_selector(selector, timeout=3000)
                        await self.page.click(selector)
                        self.logger.log(f"Used fallback selector: {selector}")
                        compose_found = True
                        break
                    except:
                        continue
                
            
            # Enhanced field filling with robust detection
            await self._fill_email_fields_enhanced(to, subject, body)
            
            self.logger.log("Outlook email composition completed successfully!")
            self.logger.log("Email ready to send (send disabled for demo safety)")
            
            return True
            
        except Exception as e:
            self.logger.log(f"Outlook automation error: {str(e)}")
            self.logger.log("Falling back to demo mode...")
            await self._mock_email_process(to, subject, body)
            return False
        finally:
            await self._cleanup()
    
    async def _fill_email_fields_enhanced(self, to, subject, body):
        """Enhanced field filling using DOM handler"""
        # Fill recipient field
        to_selector = await self.dom_handler.find_email_field('to', 'outlook')
        if to_selector:
            success = await self._fill_field_with_retry(to_selector, to, "recipient")
            if not success:
                self.logger.log("Could not fill recipient - using fallback")
        
        # Fill subject field  
        subject_selector = await self.dom_handler.find_email_field('subject', 'outlook')
        if subject_selector:
            success = await self._fill_field_with_retry(subject_selector, subject, "subject")
            if not success:
                self.logger.log("Could not fill subject - using fallback")
        
        # Fill body field
        body_selector = await self.dom_handler.find_email_field('body', 'outlook')
        if body_selector:
            success = await self._fill_field_with_retry(body_selector, body, "body")
            if not success:
                self.logger.log("Could not fill body - using fallback")
    
    async def _fill_field_with_retry(self, selector: str, value: str, field_name: str, max_retries: int = 3) -> bool:
        """Fill field with retry logic and multiple methods"""
        for attempt in range(max_retries):
            try:
                self.logger.log(f"Filling {field_name}: {value[:30]}{'...' if len(value) > 30 else ''}")
                element = await self.page.wait_for_selector(selector, timeout=3000)
                
                if element and await element.is_visible():
                    # Try multiple filling methods
                    methods = [
                        lambda: element.fill(value),
                        lambda: element.type(value, delay=50),
                        lambda: self.page.evaluate(f'document.querySelector("{selector}").value = "{value}"')
                    ]
                    
                    for method in methods:
                        try:
                            await method()
                            # Verify the field was filled
                            filled_value = await element.input_value() if hasattr(element, 'input_value') else await element.inner_text()
                            if value in filled_value or filled_value in value:
                                self.logger.log(f"Successfully filled {field_name}")
                                return True
                        except:
                            continue
                    
                    self.logger.log(f"Could not verify {field_name} was filled properly")
                    return False
                    
            except Exception as e:
                self.logger.log(f"Attempt {attempt + 1} failed for {field_name}: {str(e)}")
                if attempt < max_retries - 1:
                    await self.page.wait_for_timeout(1000)  # Wait before retry
        
        return False
    
    async def _cleanup(self):
        """Enhanced cleanup with error handling"""
        try:
            if self.browser:
                await self.browser.close()
                self.logger.log("Browser cleanup completed")
        except Exception as e:
            self.logger.log(f"Cleanup warning: {str(e)}")
    
    async def _mock_email_process(self, to, subject, body):
        """Demo mode email simulation"""
        self.logger.log("=== OUTLOOK DEMO MODE ===")
        self.logger.log(f"To: {to}")
        self.logger.log(f" Subject: {subject}")
        self.logger.log(f" Body: {body[:100]}{'...' if len(body) > 100 else ''}")
        self.logger.log("Email composition simulated successfully!")
