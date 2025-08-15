# Enhanced Agent with FastAPI Endpoint
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
import uvicorn
import time
import logging
from typing import Optional
from agent import CrossPlatformAgent
from logger import StepLogger

# Configure logging for better performance monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cross-Platform Email Agent API",
    description="AI-powered email automation across multiple platforms",
    version="1.0.0"
)

class EmailRequest(BaseModel):
    instruction: str
    provider: str = "both"  # "gmail", "outlook", or "both"
    async_mode: bool = False  # For background processing
    timeout: Optional[int] = 30  # Timeout in seconds

class EmailResponse(BaseModel):
    success: bool
    message: str
    logs: list[str]
    execution_time: Optional[float] = None
    task_id: Optional[str] = None  # For async processing

# Global agent instance for better performance (reuse)
_agent_instance = None

async def get_agent():
    """Get or create agent instance for better performance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = CrossPlatformAgent()
    return _agent_instance

@app.post("/send-email", response_model=EmailResponse)
async def send_email_endpoint(request: EmailRequest, background_tasks: BackgroundTasks):
    """
    FastAPI endpoint for sending emails via natural language instructions
    
    Enhanced with performance optimizations:
    - Agent instance reuse
    - Execution time tracking
    - Optional async processing
    - Timeout handling
    
    Example usage:
    POST /send-email
    {
        "instruction": "send email to joe@example.com saying 'Hello from my automation system'",
        "provider": "both",
        "async_mode": false,
        "timeout": 30
    }
    """
    start_time = time.time()
    
    try:
        # Get reusable agent instance
        agent = await get_agent()
        
        if request.async_mode:
            # Process in background for better performance
            task_id = f"task_{int(time.time())}"
            background_tasks.add_task(
                _execute_email_task, 
                agent, 
                request.instruction, 
                request.provider,
                task_id
            )
            return EmailResponse(
                success=True,
                message=f"Email task queued for background processing",
                logs=[f"Task {task_id} started in background"],
                execution_time=time.time() - start_time,
                task_id=task_id
            )
        
        # Synchronous execution with timeout
        try:
            success = await asyncio.wait_for(
                agent.execute_instruction(
                    instruction=request.instruction,
                    provider_choice=request.provider
                ),
                timeout=request.timeout
            )
        except asyncio.TimeoutError:
            logger.warning(f"Request timed out after {request.timeout} seconds")
            raise HTTPException(
                status_code=408, 
                detail=f"Request timed out after {request.timeout} seconds"
            )
        
        execution_time = time.time() - start_time
        logger.info(f"Email automation completed in {execution_time:.2f} seconds")
        
        return EmailResponse(
            success=success,
            message="Email automation completed successfully" if success else "Email automation failed",
            logs=agent.logger.get_log(),
            execution_time=execution_time
        )
        
    except Exception as e:
        logger.error(f"Email automation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def _execute_email_task(agent, instruction: str, provider: str, task_id: str):
    """Background task execution for async mode"""
    try:
        logger.info(f"Starting background task {task_id}")
        success = await agent.execute_instruction(
            instruction=instruction,
            provider_choice=provider
        )
        logger.info(f"Background task {task_id} completed with success: {success}")
    except Exception as e:
        logger.error(f"Background task {task_id} failed: {str(e)}")

@app.post("/send-email-batch")
async def send_email_batch(requests: list[EmailRequest]):
    """
    Batch email processing for better performance
    Process multiple email requests concurrently
    """
    start_time = time.time()
    
    try:
        agent = await get_agent()
        
        # Process all requests concurrently for better performance
        tasks = []
        for req in requests:
            task = agent.execute_instruction(
                instruction=req.instruction,
                provider_choice=req.provider
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                responses.append({
                    "success": False,
                    "message": f"Failed: {str(result)}",
                    "logs": [],
                    "request_index": i
                })
            else:
                responses.append({
                    "success": result,
                    "message": "Email automation completed successfully" if result else "Email automation failed",
                    "logs": agent.logger.get_log(),
                    "request_index": i
                })
        
        execution_time = time.time() - start_time
        logger.info(f"Batch processing completed in {execution_time:.2f} seconds")
        
        return {
            "batch_success": True,
            "total_requests": len(requests),
            "execution_time": execution_time,
            "results": responses
        }
        
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with usage instructions"""
    return {
        "message": "Cross-Platform Email Agent API",
        "usage": {
            "endpoint": "/send-email",
            "method": "POST",
            "example": {
                "instruction": "send email to joe@example.com saying 'Hello from my automation system'",
                "provider": "both"
            }
        },
        "cli_equivalent": "python agent.py \"send email to joe@example.com saying 'Hello from my automation system'\""
    }

@app.get("/health")
async def health_check():
    """Enhanced health check with performance metrics"""
    try:
        agent = await get_agent()
        return {
            "status": "healthy", 
            "service": "email-automation-agent",
            "agent_ready": agent is not None,
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "email-automation-agent", 
            "error": str(e),
            "timestamp": time.time()
        }

@app.get("/test")
async def run_performance_test():
    """
    Performance test endpoint with optimized test instructions
    Tests multiple scenarios concurrently for better performance analysis
    """
    test_instructions = [
        {
            "instruction": "Send email to joe@example.com saying 'Hello from automation system'",
            "provider": "gmail",
            "description": "Basic Gmail test"
        },
        {
            "instruction": "Send email to jane@company.com about quarterly meeting tomorrow at 2pm", 
            "provider": "outlook",
            "description": "Outlook with detailed content"
        },
        {
            "instruction": "Email admin@startup.com regarding server maintenance scheduled",
            "provider": "both", 
            "description": "Multi-provider test"
        },
        {
            "instruction": "Send urgent message to team@example.com about deployment status",
            "provider": "both",
            "description": "Urgent communication test"
        }
    ]
    
    start_time = time.time()
    results = []
    
    try:
        agent = await get_agent()
        
        # Run tests concurrently for better performance
        test_tasks = []
        for test_case in test_instructions:
            task = _run_single_test(agent, test_case)
            test_tasks.append(task)
        
        # Execute all tests concurrently
        test_results = await asyncio.gather(*test_tasks, return_exceptions=True)
        
        for i, result in enumerate(test_results):
            if isinstance(result, Exception):
                results.append({
                    "test_case": test_instructions[i]["description"],
                    "success": False,
                    "error": str(result),
                    "execution_time": 0
                })
            else:
                results.append(result)
        
        total_time = time.time() - start_time
        
        return {
            "performance_test": "completed",
            "total_execution_time": total_time,
            "concurrent_tests": len(test_instructions),
            "average_time_per_test": total_time / len(test_instructions),
            "results": results,
            "performance_summary": {
                "total_tests": len(results),
                "successful_tests": sum(1 for r in results if r.get("success", False)),
                "failed_tests": sum(1 for r in results if not r.get("success", False)),
                "success_rate": f"{(sum(1 for r in results if r.get('success', False)) / len(results) * 100):.1f}%"
            }
        }
        
    except Exception as e:
        logger.error(f"Performance test failed: {str(e)}")
        return {
            "performance_test": "failed",
            "error": str(e),
            "execution_time": time.time() - start_time
        }

async def _run_single_test(agent, test_case):
    """Run a single test case with performance monitoring"""
    test_start = time.time()
    
    try:
        # Execute the test instruction
        success = await agent.execute_instruction(
            instruction=test_case["instruction"],
            provider_choice=test_case["provider"]
        )
        
        execution_time = time.time() - test_start
        
        return {
            "test_case": test_case["description"],
            "instruction": test_case["instruction"],
            "provider": test_case["provider"],
            "success": success,
            "execution_time": execution_time,
            "logs": agent.logger.get_log()[-5:]  # Last 5 log entries
        }
        
    except Exception as e:
        return {
            "test_case": test_case["description"],
            "success": False,
            "error": str(e),
            "execution_time": time.time() - test_start
        }

if __name__ == "__main__":
    print("🚀 Starting Cross-Platform Email Agent API")
    print("📊 Performance Enhancements Enabled:")
    print("  ✓ Agent instance reuse")
    print("  ✓ Concurrent request processing") 
    print("  ✓ Background task support")
    print("  ✓ Timeout handling")
    print("  ✓ Batch processing endpoint")
    print("  ✓ Performance monitoring")
    print("  ✓ Enhanced test suite")
    print()
    print("📡 Available Endpoints:")
    print("  • POST /send-email - Single email automation")
    print("  • POST /send-email-batch - Batch email processing")
    print("  • GET /test - Performance test suite")
    print("  • GET /health - Health check with metrics")
    print("  • GET / - API documentation")
    print()
    print("🌐 Server starting on http://localhost:8088")
    print("📖 API Docs available at http://localhost:8088/docs")
    print("🧪 Performance Tests at http://localhost:8088/test")
    
    # Performance-optimized test instructions for load testing
    sample_test_instructions = [
        "Send email to performance@test.com saying 'Performance test message'",
        "Email loadtest@example.com about system performance monitoring", 
        "Send urgent notification to alerts@system.com regarding server status",
        "Email team@performance.com about load testing results"
    ]
    
    print(f"\n🧪 {len(sample_test_instructions)} sample test instructions loaded")
    print("💡 Tip: Use /test endpoint for concurrent performance testing")
    
    uvicorn.run(
        app, 
        host="localhost", 
        port=8088,
        log_level="info",
        access_log=True
    )
