import os
import random
from typing import List, Tuple, Optional

try:
    from langchain_openai import AzureChatOpenAI  # type: ignore
    from langchain.schema import HumanMessage  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    AzureChatOpenAI = None  # type: ignore
    HumanMessage = None  # type: ignore

from moves import to_algebraic


class LLMAgent:
    def __init__(self):
        self.available = False
        self.model = None
        # Configure from env vars to avoid hardcoding secrets
        api_version = os.getenv('AZURE_OPENAI_API_VERSION') or '2023-12-01-preview'
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        api_key = os.getenv('AZURE_OPENAI_API_KEY')

        if AzureChatOpenAI and deployment and endpoint and api_key:
            try:
                self.model = AzureChatOpenAI(
                    openai_api_version=api_version,
                    azure_deployment=deployment,
                    azure_endpoint=endpoint,
                    api_key=api_key,
                    temperature=0.2,
                )
                self.available = True
            except Exception:
                self.available = False

    def _format_prompt(self, color: str, moves: List[Tuple[Tuple[int,int], Tuple[int,int]]]) -> str:
        color_name = 'White' if color == 'W' else 'Black'
        options = [f"{to_algebraic(s)} {to_algebraic(e)}" for s, e in moves]
        joined = "\n".join(f"- {m}" for m in options)
        return (
            f"You are playing {color_name} in a text chess game. Choose exactly one legal move from the list and reply with only the move in the format 'E2 E4'.\n"
            f"Legal moves:\n{joined}\n"
            f"Respond with only one line containing the chosen move."
        )

    def choose_move(self, color: str, legal_moves: List[Tuple[Tuple[int,int], Tuple[int,int]]]) -> Optional[Tuple[Tuple[int,int], Tuple[int,int]]]:
        if not legal_moves:
            return None
        # Fallback to random if LLM is not available
        if not self.available:
            return random.choice(legal_moves)

        prompt = self._format_prompt(color, legal_moves)
        try:
            msg = HumanMessage(content=prompt)
            res = self.model.invoke([msg])
            text = res.content.strip().upper()
            # parse like 'E2 E4'
            parts = text.split()
            if len(parts) == 2 and len(parts[0]) in (2,3) and len(parts[1]) in (2,3):
                # map back to move list
                option_set = {f"{to_algebraic(s)} {to_algebraic(e)}": (s, e) for s, e in legal_moves}
                return option_set.get(f"{parts[0]} {parts[1]}") or random.choice(legal_moves)
        except Exception:
            pass
        return random.choice(legal_moves)


def get_agent():
    return LLMAgent()
