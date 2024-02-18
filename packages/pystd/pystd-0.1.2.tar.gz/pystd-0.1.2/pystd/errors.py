"""
Errors module for pystd.
"""

class BadConnector(Exception):
    """Exception base class for invalid connectors."""
    def __init__(self, message: str) -> None:
        super().__init__(message)