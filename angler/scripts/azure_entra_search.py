import argparse
import json
import re
import shlex
import subprocess
import sys
from typing import List, Optional

COMMON_ENDPOINTS = {
    'servicePrincipals': 'https://graph.microsoft.com/v1.0/servicePrincipals',
    'applications': 'https://graph.microsoft.com/v1.0/applications',
    'users': 'https://graph.microsoft.com/v1.0/users',
    'groups': 'https://graph.microsoft.com/v1.0/groups',
    'directoryObjects': 'https://graph.microsoft.com/v1.0/directoryObjects',
    'servicePrincipalSecrets': 'https://graph.microsoft.com/v1.0/servicePrincipals?$expand=keyCredentials',
}


def run_az_rest_get(uri: str, dry_run: bool=False) -> Optional[dict]:
    """Call `az rest --method get --uri "<uri>"` and return parsed JSON, or None on failure."""
    cmd = ['az', 'rest', '--method', 'get', '--uri', uri]
    if dry_run:
        print('DRY:', ' '.join(shlex.quote(p) for p in cmd))
        return None
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    except FileNotFoundError:
        print('ERROR: az CLI not found. Please install Azure CLI.', file=sys.stderr)
        sys.exit(2)
    if p.returncode != 0:
        print(f'az returned {p.returncode}; stderr:\n{p.stderr}', file=sys.stderr)
        return None
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        print('Failed to parse JSON from az output', file=sys.stderr)
        return None


def iterate_endpoint(uri: str, dry_run: bool=False):
    """Yield JSON objects from endpoint, following @odata.nextLink pagination where present."""
    next_uri = uri
    while next_uri:
        js = run_az_rest_get(next_uri, dry_run=dry_run)
        if js is None:
            return
        # if top-level value is a dict with 'value' list, yield each element
        if isinstance(js, dict) and 'value' in js and isinstance(js['value'], list):
            for item in js['value']:
                yield item
            # check nextLink
            nl = js.get('@odata.nextLink') or js.get('nextLink')
            if nl:
                next_uri = nl
                continue
            else:
                break
        else:
            # yield the object itself
            yield js
            break


def json_to_text(obj) -> str:
    """Convert JSON object to compact text for searching."""
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)


def search_in_endpoints(endpoints: List[str], pattern: str, regex: bool=False, dry_run: bool=False):
    compiled = re.compile(pattern) if regex else None
    for ep in endpoints:
        uri = COMMON_ENDPOINTS.get(ep, ep)  # allow full URI passthrough
        print('\n=== Endpoint:', ep, '->', uri)
        for obj in iterate_endpoint(uri, dry_run=dry_run):
            txt = json_to_text(obj)
            found = False
            if regex and compiled is not None:
                if compiled.search(txt):
                    found = True
            else:
                if pattern in txt:
                    found = True
            if found:
                print('\n--- Match in item ---')
                try:
                    print(json.dumps(obj, indent=2, ensure_ascii=False))
                except Exception:
                    print(txt)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--endpoints', '-e', nargs='+', default=['servicePrincipals'],
                    help='List of endpoints to query. Can use keys from COMMON_ENDPOINTS or supply full URI.')
    ap.add_argument('--query', '-q', required=True, help='Substring or regex to search for (for regex set --regex).')
    ap.add_argument('--regex', action='store_true', help='Treat query as a regex.')
    ap.add_argument('--dry-run', action='store_true', help='Print az commands without executing.')
    args = ap.parse_args()
    search_in_endpoints(args.endpoints, args.query, regex=args.regex, dry_run=args.dry_run)
