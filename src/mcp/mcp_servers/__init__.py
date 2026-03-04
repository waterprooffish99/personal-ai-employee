"""Specific MCP server implementations for the AI Employee System"""

from .email_mcp import EmailMCPServer, get_email_mcp
from .odoo_mcp import OdooMCPServer, get_odoo_mcp
from .social_mcp import SocialMCPServer, get_social_mcp
