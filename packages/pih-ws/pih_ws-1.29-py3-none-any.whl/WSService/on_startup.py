import importlib.util
import sys

pih_exists = importlib.util.find_spec("pih") is not None
if not pih_exists:
    sys.path.append("//pih/facade")
from pih import A

server_name: str = A.SE.arg(0)
if server_name is None:
    server_name = A.SYS.host()

A.E.server_was_started(server_name)