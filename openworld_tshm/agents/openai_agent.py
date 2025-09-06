from __future__ import annotations
"""
OpenAI integration layer supporting the modern Responses (Agents) API with
graceful fallback to Chat Completions when Agents is unavailable.

This module performs dynamic imports so that core installs (without
the optional [llm] extras) still work and tests don't require openai.
"""
from typing import Optional
import os


def _get_client():
    """Return OpenAI client instance or raise ImportError if unavailable."""
    from openai import OpenAI  # type: ignore

    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    org = os.getenv("OPENAI_ORG")
    proj = os.getenv("OPENAI_PROJECT")
    kwargs = {"api_key": key}
    if org:
        kwargs["organization"] = org
    if proj:
        kwargs["project"] = proj
    return OpenAI(**kwargs)  # type: ignore


def generate_with_openai(prompt: str, *, model: Optional[str] = None, use_agents: bool = True, temperature: float = 0.2, system_instruction: Optional[str] = None) -> str:
    """
    Generate text using OpenAI APIs.
    - Prefer Responses (Agents) API when `use_agents=True`.
    - Fallback to Chat Completions when Agents path fails or disabled.
    Returns the generated text, or raises on hard failure.
    """
    try:
        client = _get_client()
    except Exception as e:  # pragma: no cover - depends on env
        raise RuntimeError(f"OpenAI client unavailable: {e}")

    mdl = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    sys_inst = system_instruction or "You are a forestry planning expert."

    if use_agents:
        try:  # pragma: no cover - network branch
            # Use the modern Responses API (agents-style)
            resp = client.responses.create(
                model=mdl,
                input=prompt,
                system_instruction=sys_inst,
                temperature=temperature,
            )
            # Extract first text output
            for out in getattr(resp, "output", []) or []:
                if getattr(out, "type", "") == "message":
                    for c in getattr(out, "content", []) or []:
                        if getattr(c, "type", "") == "output_text":
                            return getattr(c, "text", "").strip()
            # Some SDK versions expose a top-level `output_text`
            text = getattr(resp, "output_text", None)
            if text:
                return str(text).strip()
        except Exception:
            # Fall through to chat completions
            pass

    # Chat Completions fallback for broad compatibility
    try:  # pragma: no cover - network branch
        resp = client.chat.completions.create(
            model=mdl,
            messages=[{"role": "system", "content": sys_inst}, {"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI request failed: {e}")

