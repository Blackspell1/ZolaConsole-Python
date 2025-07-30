# actions.py

# === Constants ===
TRACER_MAX_CHARGES = 5
TRACER_CHARGE_TIME = 3 * 60
TRACER_ACTIVE_TIME = 4 * 60
TRACER_PROC_DAMAGE = 45

SWING_MAX_CHARGES = 3
SWING_CHARGE_TIME = 6 * 60

GET_OVER_HERE_MAX_CHARGES = 1
GET_OVER_HERE_CHARGE_TIME = 8 * 60

UPPERCUT_MAX_CHARGES = 2
UPPERCUT_CHARGE_TIME = 6 * 60
UPPERCUT_COOLDOWN_TIME = 2 * 60

MELEE_SEQUENCE_WINDOW = 60

BURNTRACER_DAMAGE = 30
BURNTRACER_DOT_TOTAL = 60  # 15/s for 4s

# === Action Indices ===
(
    jump, land, meleePunch, meleePunchB, meleeKick,
    overhead, tracer, swing, swingWhiff,
    getOverHere, getOverHereTargetting,
    uppercut, ffameStack, saporen, burnTracer
) = range(15)

# === Action Names ===
ACTION_NAMES = [
    "jump", "land", "meleePunch", "meleePunchB", "meleeKick",
    "overhead", "tracer", "swing", "swingWhiff",
    "getOverHere", "getOverHereTargetting",
    "uppercut", "ffameStack", "saporen", "burnTracer"
]

# === Cancellability Matrix ===
cancellable = [[False for _ in range(15)] for _ in range(15)]

# Provided cancel logic + burnTracer cancels like swing
cancel_pairs = {
    jump: [tracer, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen],
    meleePunch: [overhead, tracer, swing, swingWhiff, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen],
    meleePunchB: [overhead, tracer, swing, swingWhiff, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen],
    meleeKick: [overhead, tracer, swing, swingWhiff, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen],
    overhead: [tracer, swing, swingWhiff, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen],
    tracer: [swing, swingWhiff, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen],
    swing: [tracer, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen, burnTracer],
    swingWhiff: [tracer, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen, burnTracer],
    getOverHere: [swing, swingWhiff, burnTracer],
    getOverHereTargetting: [swing, swingWhiff, burnTracer],
    uppercut: [swing, swingWhiff, burnTracer],
    ffameStack: [],
    saporen: [],
    burnTracer: [swing, swingWhiff, tracer, getOverHere, getOverHereTargetting, uppercut, ffameStack, saporen],
}

for from_index, to_list in cancel_pairs.items():
    for to_index in to_list:
        cancellable[from_index][to_index] = True

# === Action Class ===
class Action:
    def __init__(self, name, damage, cancel_time, full_time, procs_tracer=False, procs_burn=False):
        self.name = name
        self.damage = damage
        self.cancel_time = cancel_time
        self.delta_time = full_time - cancel_time
        self.procs_tracer = procs_tracer
        self.procs_burn = procs_burn
        self.requires_tracer = False  # Reserved for future use

    def __repr__(self):
        return f"Action(name='{self.name}', dmg={self.damage}, cancel={self.cancel_time}, full={self.cancel_time + self.delta_time})"

# === All Actions List (Updated Damage Values) ===
ACTIONS = [
    Action("jump", 0, 1, 21),
    Action("land", 0, 1, 1),
    Action("meleePunch", 25, 15, 23, True),
    Action("meleePunchB", 40, 15, 23, True),
    Action("meleeKick", 40, 26, 51, True),
    Action("overhead", 40, 39, 55, True),
    Action("tracer", 30, 5, 25),
    Action("swing", 0, 7, 14),
    Action("swingWhiff", 0, 11, 32),
    Action("getOverHere", 25, 20, 53),
    Action("getOverHereTargetting", 55, 37, 60),
    Action("uppercut", 60, 22, 49, True),
    Action("ffameStack", 105, 18, 61, True),
    Action("saporen", 95, 71, 98, True),  # ✅ Updated to 95 damage
    Action("burnTracer", 30, 5, 25, False, True)
]

