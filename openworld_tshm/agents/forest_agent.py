from __future__ import annotations
import os, subprocess, json
from typing import Optional
from ..config import get_settings
from .openai_agent import generate_with_openai  # safe to import; resolves dynamically


def generate_narrative(summary_inputs: dict, use_llm: str = "auto", use_agents: Optional[bool] = None) -> str:
    """
    Generate a narrative report using OpenAI Agents SDK if OPENAI_API_KEY set,
    else try 'llm' CLI with ollama model if installed, else return a deterministic fallback.
    use_llm: "auto" | "openai" | "local" | "fallback"
    """
    prompt = (
        "You are a forest management assistant. Create a concise narrative summarizing "
        "tree species distribution, height statistics, and health, and recommend harvest timelines, "
        "planting densities, and regeneration targets.\n"
        f"Inputs JSON:\n{json.dumps(summary_inputs, indent=2)}\n"
        "Return 3-5 paragraphs."
    )

    if use_llm in ("openai", "auto") and os.getenv("OPENAI_API_KEY"):
        try:  # pragma: no cover - requires network
            s = get_settings()
            return generate_with_openai(
                prompt,
                model=s.openai_model,
                use_agents=(s.openai_use_agents if use_agents is None else use_agents),
                temperature=0.2,
                system_instruction="You are a forestry planning expert.",
            )
        except Exception:
            # fall through to other modes or deterministic fallback
            pass  # pragma: no cover

    if use_llm in ("local", "auto") and os.getenv("OLLAMA_MODEL"):
        try:  # pragma: no cover - external binary branch
            model = os.getenv("OLLAMA_MODEL", "llama3")  # pragma: no cover
            text = subprocess.check_output(["llm", "-m", f"ollama:{model}", prompt], text=True, timeout=3)  # pragma: no cover
            return text.strip()  # pragma: no cover
        except Exception:
            pass  # pragma: no cover

    # Deterministic fallback
    trees = summary_inputs.get("num_trees", 0)
    avg_h = summary_inputs.get("avg_height", 0)
    return (
        f"This stand contains approximately {trees} trees with an average height of {avg_h:.1f} m. "
        "Health indicators suggest stable vigor with localized variability.\n"
        "We recommend staggered harvest windows aligned with species-specific rotation ages, "
        "and replanting at densities suitable for site class II. Regeneration targets should aim "
        "for 85–90% survival at year 3 with supplemental fill-in planting as needed."
    )
