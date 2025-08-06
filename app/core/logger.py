import logging
import sys
from typing import Optional


def get_logger(
    name: str = __name__,
    level: str = "INFO",
    format_string: Optional[str] = None,
    include_timestamp: bool = True,
    include_level: bool = True,
    include_name: bool = True
) -> logging.Logger:
    """
    Retorna um logger configurado e otimizado para Docker.
    """
    logger = logging.getLogger(name)
    
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(numeric_level)
        if format_string is None:
            format_parts = []
            
            if include_timestamp:
                format_parts.append("%(asctime)s")
            
            if include_level:
                format_parts.append("[%(levelname)s]")
            
            if include_name:
                format_parts.append("%(name)s")
                
            format_parts.append("%(message)s")
            format_string = " - ".join(format_parts)
        
        formatter = logging.Formatter(
            format_string,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.propagate = False
    
    return logger
