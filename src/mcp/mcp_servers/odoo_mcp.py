import os
from typing import Dict, Any, Optional
import json
import requests

from ...utils.logger import log_action
from ...utils.dry_run import is_dry_run
from ...utils.env_manager import get_env
from ...utils.decorators import with_retry

class OdooMCPServer:
    """MCP server for interacting with Odoo Community via JSON-RPC (Odoo 19+)."""

    def __init__(self):
        self.url = get_env("ODOO_URL", "http://localhost:8069")
        self.db = get_env("ODOO_DB", "odoo")
        self.username = get_env("ODOO_USERNAME", "admin")
        self.password = get_env("ODOO_PASSWORD", "admin")
        self.session_id = None
        self.uid = None
        self.enabled = bool(get_env("ODOO_URL"))

    def _json_rpc(self, url, method, params):
        data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()

    @with_retry(max_retries=3, backoff_factor=2.0)
    def authenticate(self) -> bool:
        """Authenticate with Odoo using JSON-RPC."""
        if not self.enabled:
            return False

        if is_dry_run():
            log_action("Odoo MCP (JSON-RPC): Would authenticate", actor="system", result="info", dry_run=True)
            return True

        try:
            url = f"{self.url}/jsonrpc"
            # In Odoo JSON-RPC, we usually authenticate via common service
            res = self._json_rpc(url, "call", {
                "service": "common",
                "method": "login",
                "args": [self.db, self.username, self.password]
            })
            self.uid = res.get("result")
            if self.uid:
                log_action("Odoo MCP (JSON-RPC): Authenticated successfully", actor="system", result="success")
                return True
            return False
        except Exception as e:
            log_action("Odoo MCP: JSON-RPC Connection error", actor="system", result="error", details={"error": str(e)})
            raise

    @with_retry(max_retries=3, backoff_factor=2.0)
    def create_invoice(self, partner_id: int, lines: list) -> Dict[str, Any]:
        """Create an invoice draft via JSON-RPC."""
        if not self.enabled:
            return {"status": "error", "message": "Odoo not configured"}

        if is_dry_run():
            return {"status": "success", "message": "Dry run: invoice not created", "invoice_id": 999}

        if not self.uid and not self.authenticate():
            return {"status": "error", "message": "Auth failed"}

        try:
            url = f"{self.url}/jsonrpc"
            invoice_lines = []
            for line in lines:
                invoice_lines.append((0, 0, {
                    'product_id': line.get('product_id'),
                    'quantity': line.get('quantity', 1),
                    'price_unit': line.get('price_unit', 0.0),
                }))

            res = self._json_rpc(url, "call", {
                "service": "object",
                "method": "execute_kw",
                "args": [self.db, self.uid, self.password, 'account.move', 'create', [{
                    'partner_id': partner_id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': invoice_lines,
                }]]
            })
            invoice_id = res.get("result")
            log_action("Odoo MCP: Created invoice", actor="system", result="success", details={"invoice_id": invoice_id})
            return {"status": "success", "message": "Invoice created", "invoice_id": invoice_id}
        except Exception as e:
            log_action("Odoo MCP: Error creating invoice", actor="system", result="error", details={"error": str(e)})
            raise

    @with_retry(max_retries=3, backoff_factor=2.0)
    def post_invoice(self, invoice_id: int) -> Dict[str, Any]:
        """Post/Finalize invoice via JSON-RPC."""
        if not self.enabled: return {"status": "error"}
        if is_dry_run(): return {"status": "success"}
        if not self.uid and not self.authenticate(): return {"status": "error"}

        try:
            url = f"{self.url}/jsonrpc"
            self._json_rpc(url, "call", {
                "service": "object",
                "method": "execute_kw",
                "args": [self.db, self.uid, self.password, 'account.move', 'action_post', [invoice_id]]
            })
            return {"status": "success", "message": f"Invoice {invoice_id} posted"}
        except Exception as e:
            log_action("Odoo MCP: Error posting", actor="system", result="error", details={"error": str(e)})
            raise

def get_odoo_mcp():
    return OdooMCPServer()

def get_odoo_mcp():
    return OdooMCPServer()
