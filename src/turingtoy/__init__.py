from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)


def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List, bool]:
    blank = machine['blank']
    start_state = machine['start state']
    final_state = set(machine['final states'])
    table = machine['table']
    input = list(input_)
    pos = 0
    history = []

    step = 0
    while steps is None or step < steps:
        if pos < 0:
            input.insert(0, blank)
            pos = 0
        if pos >= len(input):
            input.append(blank)
        symbol = input[pos]
        if start_state in table and symbol in table[start_state]:
            transition = table[start_state][symbol]
            history.append({"state": start_state,"reading": symbol,"position": pos,"memory": "".join(input),"transition": transition})
            if isinstance(transition, str):
                if transition == "R":
                    pos += 1
                if transition == "L":
                    pos -= 1
            else:
                if 'write' in transition:
                    input[pos] = transition['write']
                if 'R' in transition:
                    start_state = transition['R']
                    pos += 1
                if 'L' in transition:
                    start_state = transition['L']
                    pos -= 1
            step += 1
            if start_state in final_state:
                break
        else:
            history.append({"state": start_state,"reading": symbol,"position": pos,"memory": "".join(input),"transition": None})
            break

    return ''.join(input).strip(blank), history, start_state in final_state
