"""
Handler for the hidden 'api' action (raw API calls).
"""

from ._helpers import merge_fields_with_stdin, output


def handle_api(client, args):
    """Make a raw API call and output the response."""
    path = "/".join(args.path) if args.path else ""
    url = f"{client.base_url}/api/{path}"
    body = merge_fields_with_stdin(args) or None
    method = args.method.lower()
    response = getattr(client.session, method)(url, json=body, timeout=client.timeout)
    client._check_response(response)
    data = response.json()
    output(data, args.format)
