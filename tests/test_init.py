"""Test if e5renewer.__init__ works."""

import sys
import json
from pathlib import Path
from e5renewer import main


def test_main(tmp_path: str, secret: str, unused_tcp_port: int):
    """Check if main is correct."""
    test_config = {
        "auth_token": secret,
        "listen_addr": "127.0.0.1",
        "listen_port": unused_tcp_port,
        "users": [
            {
                "name": "me@test.com",
                "client_id": "test-client-id",
                "secret": secret,
                "tenant_id": "test-tenant",
                "from_time": "00:00:00",
                "to_time": "00:00:00",
            },
        ],
    }
    tpath = Path(tmp_path)
    tmp_conf = tpath / "config.json"
    with tmp_conf.open("w", encoding="utf-8") as writer:
        json.dump(test_config, writer)
    argv = sys.argv
    sys.argv = [sys.argv[0], "-c", str(tmp_conf.absolute())]
    main(True)
    sys.argv = argv
