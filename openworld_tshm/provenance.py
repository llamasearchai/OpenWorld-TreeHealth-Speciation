from __future__ import annotations
import json, os, time, hashlib, getpass, socket, subprocess
from dataclasses import dataclass, asdict
from typing import Any
import sys, platform
from .utils.hashing import sha256_file


@dataclass
class ProvenanceRecord:
    timestamp: float
    actor: str
    host: str
    step: str
    params: dict[str, Any]
    inputs: list[str]
    outputs: list[str]
    code_version: str | None
    digest: str


class ProvenanceStore:
    def __init__(self, ledger_path: str) -> None:
        os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
        self.ledger_path = ledger_path

    def _code_version(self) -> str | None:
        try:
            out = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)  # pragma: no cover
            return out.decode().strip()  # pragma: no cover
        except Exception:
            return None

    def _digest(self, payload: dict[str, Any]) -> str:
        h = hashlib.sha256()
        h.update(json.dumps(payload, sort_keys=True, default=str).encode())
        return h.hexdigest()

    def log(self, step: str, params: dict[str, Any], inputs: list[str], outputs: list[str]) -> ProvenanceRecord:
        record_base = {
            "timestamp": time.time(),
            "actor": getpass.getuser(),
            "host": socket.gethostname(),
            "step": step,
            "params": params,
            "inputs": inputs,
            "outputs": outputs,
            "code_version": self._code_version(),
        }
        # Attach hashes for existing files
        try:
            input_hashes = {p: sha256_file(p) for p in inputs if os.path.exists(p)}
            output_hashes = {p: sha256_file(p) for p in outputs if os.path.exists(p)}
        except Exception:
            input_hashes, output_hashes = {}, {}
        env = {
            "python": sys.version.split(" ")[0],
            "platform": platform.platform(),
            "input_hashes": input_hashes,
            "output_hashes": output_hashes,
        }
        digest = self._digest(record_base)
        rec = ProvenanceRecord(**record_base, digest=digest)
        rec_dict = asdict(rec)
        rec_dict["env"] = env
        # Atomic-ish append and fsync for durability
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec_dict) + "\n")
            try:
                f.flush()
                os.fsync(f.fileno())
            except Exception:
                pass
        return rec

