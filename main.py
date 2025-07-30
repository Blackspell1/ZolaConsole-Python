from combo import Combo
from actions import (
    ACTION_NAMES, jump, land, meleePunch, meleePunchB, meleeKick, overhead,
    tracer, swing, swingWhiff, getOverHere, getOverHereTargetting, uppercut,
    ffameStack, saporen, burnTracer
)

def combo_action_code(index):
    mapping = {
        jump: 'j', land: 'l',
        meleePunch: 'p', meleePunchB: 'P', meleeKick: 'k',
        overhead: 'o', tracer: 't', swing: 's', swingWhiff: 'w',
        getOverHere: 'g', getOverHereTargetting: 'G',
        uppercut: 'u', ffameStack: 'f', saporen: 'n', burnTracer: 'b'
    }
    return mapping.get(index, '?')

def list_actions():
    print("Available actions:")
    for idx, name in enumerate(ACTION_NAMES):
        print(f" - '{combo_action_code(idx)}' = {name}")

def parse_action_sequence(seq):
    char_to_index = {
        'j': jump, 'l': land, 'p': meleePunch, 'P': meleePunchB,
        'k': meleeKick, 'o': overhead, 't': tracer, 's': swing,
        'w': swingWhiff, 'g': getOverHere, 'G': getOverHereTargetting,
        'u': uppercut, 'f': ffameStack, 'n': saporen, 'b': burnTracer
    }
    return [char_to_index[c] for c in seq if c in char_to_index]

def handle_calc(seq, init_state):
    combo = Combo()
    combo.__dict__.update(init_state.__dict__)
    for idx in parse_action_sequence(seq):
        legal = combo.get_legal_actions()
        if not (legal & (1 << idx)):
            print(f"warning: '{combo_action_code(idx)}' is not a legal action.")
        combo.add_action(idx)
    combo.print()

def print_properties(state):
    for key, value in vars(state).items():
        print(f" - '{key}' = {value}")

def main():
    init_state = Combo()
    initial_sequence = ""

    print("Combo Console (Python Version)")
    print("Type 'help' for a list of commands.\n")

    while True:
        try:
            command = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not command:
            continue

        tokens = command.split()
        if not tokens:
            continue

        cmd = tokens[0]
        args = tokens[1:]

        if cmd == "help":
            print(
                " - calc [string actions] : simulate and evaluate a combo sequence\n"
                " - actions : show available action key mappings\n"
                " - set [property] [value] : configure initial state\n"
                " - properties : list current properties\n"
                " - exit : quit the console"
            )

        elif cmd == "calc":
            sequence = args[0] if args else ""
            full_seq = initial_sequence + sequence
            handle_calc(full_seq, init_state)

        elif cmd == "actions":
            list_actions()

        elif cmd == "set":
            if len(args) < 2:
                print("usage: set [property] [value]")
                continue
            prop, val = args[0], args[1]
            if prop == "initialSequence":
                initial_sequence = val
                continue
            try:
                curr_type = type(getattr(init_state, prop))
                if curr_type == bool:
                    setattr(init_state, prop, val.lower() in ["1", "true", "yes"])
                elif curr_type == int:
                    setattr(init_state, prop, int(val))
                elif curr_type == float:
                    setattr(init_state, prop, float(val))
                else:
                    print(f"Unsupported property type: {curr_type}")
            except AttributeError:
                print(f"Unknown property: '{prop}'")
            except ValueError:
                print(f"Invalid value: '{val}' for {prop}")

        elif cmd == "properties":
            print_properties(init_state)

        elif cmd == "exit":
            break

        else:
            print("Unknown command. Type 'help' for help.")

if __name__ == "__main__":
    main()
