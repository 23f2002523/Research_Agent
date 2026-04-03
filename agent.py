import ollama
import os
import re
from prompt import SYSTEM_PROMPT
from tools import TOOLS


def parse_llm_response(text: str):
    """Extract Action and Input from LLM output."""
    action_match = re.search(r"Action:\s*(.+)", text)
    input_match  = re.search(r"Input:\s*(.+)", text, re.DOTALL)

    action = action_match.group(1).strip() if action_match else None
    inp    = input_match.group(1).strip()  if input_match  else None

    return action, inp


def run_agent(user_query: str, max_steps: int = 6):
    """The main ReAct loop using Ollama locally."""

    print(f"\n[USER]: {user_query}\n")
    print("=" * 50)

    # conversation history
    messages = [
        {"role": "system",  "content": SYSTEM_PROMPT},
        {"role": "user",    "content": user_query}
    ]

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        # 1. THINK — ask local LLM what to do
        response = ollama.chat(
            model="llama3.2",
            messages=messages
        )

        llm_output = response["message"]["content"]
        print(f"[LLM]:\n{llm_output}\n")

        # 2. PARSE — what action did LLM choose?
        action, action_input = parse_llm_response(llm_output)

        if not action:
            print("[AGENT]: Could not parse action. Stopping.")
            break

        # 3. CHECK — is the agent done?
        if action.upper() == "FINISH":
            print("\n" + "=" * 50)
            print("[FINAL ANSWER]:")
            print(action_input)
            return action_input

        # 4. ACT — run the tool
        if action in TOOLS:
            print(f"[TOOL CALL]: {action}('{action_input}')")
            tool_fn     = TOOLS[action]["function"]
            observation = tool_fn(action_input)
            print(f"[OBSERVATION]: {observation[:300]}...")
        else:
            observation = f"Tool '{action}' not found. Available tools: {list(TOOLS.keys())}"

        # 5. REMEMBER — add to conversation history
        messages.append({"role": "assistant", "content": llm_output})
        messages.append({"role": "user",      "content": f"Observation: {observation}"})

    print("[AGENT]: Reached max steps.")
    return "Could not complete research within step limit."