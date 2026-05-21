import logging
import sys
import json
from typing import Dict, Any

def setup_enterprise_logger(name: str) -> logging.Logger:
    """
    Configures a standardized logger outputting JSON format.
    Structured logging is essential for ingestion by tools like Promtail/Loki or ELK.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate logs if the logger is instantiated multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        
        # Simple JSON formatter for the portfolio
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_record = {
                    "time": self.formatTime(record, self.datefmt),
                    "name": record.name,
                    "level": record.levelname,
                    "message": record.getMessage()
                }
                return json.dumps(log_record)
                
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        
    return logger

def format_api_response(thread_id: str, content: str, tokens_used: int = 0) -> Dict[str, Any]:
    """
    Standardizes the JSON payload returned by the FastAPI endpoints.
    """
    return {
        "status": "success",
        "thread_id": thread_id,
        "data": {
            "message": content,
        },
        "metadata": {
            "tokens_estimated": tokens_used
        }
    }