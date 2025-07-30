from actions import *

class Combo:
    def __init__(self):
        self.actions = []
        self.damageDealt = 0
        self.timeTaken = 0

        self.tracerActive = 0
        self.burnTracerActive = 0

        self.isAirborne = False
        self.targetAirborne = False

        self.hasDoubleJump = False
        self.hasJumpOverhead = False
        self.hasSwingOverhead = False

        self.hasSeasonalBuff = False
        self.hasMantisBuff = False

        self.allowFfameStack = True
        self.allowSaporen = True

        self.kickOpener = False
        self.timeFromDamage = False

        self.meleeSequence = 0
        self.meleeSequenceWindow = 0

        self.tracerCharges = TRACER_MAX_CHARGES
        self.swingCharges = SWING_MAX_CHARGES
        self.getOverHereCharges = GET_OVER_HERE_MAX_CHARGES
        self.uppercutCharges = UPPERCUT_MAX_CHARGES
        self.uppercutCooldown = 0

        self.lastAnim = land
        self.lastTracerTime = -ACTIONS[tracer].delta_time
        self.webUsed = True
        self.hangtime = 0

    def get_legal_actions(self):
        legal = (1 << tracer) | (1 << burnTracer)
        if self.webUsed and not self.hasJumpOverhead:
            legal |= (1 << swing) | (1 << swingWhiff)
        if not self.isAirborne or self.hasDoubleJump:
            legal |= (1 << jump)
        if self.isAirborne and not self.hasDoubleJump and not self.hasJumpOverhead and self.webUsed:
            legal |= (1 << land)
        if self.lastAnim not in [getOverHere, getOverHereTargetting, ffameStack, saporen]:
            legal |= (1 << getOverHere)
            if self.tracerActive:
                legal |= (1 << getOverHereTargetting)
                if self.allowFfameStack:
                    legal |= (1 << ffameStack)
            if (self.hasJumpOverhead or self.hasSwingOverhead) and self.allowSaporen:
                legal |= (1 << saporen)
        if self.lastAnim != uppercut and not self.hasJumpOverhead:
            legal |= (1 << uppercut)
        if self.hasJumpOverhead or self.hasSwingOverhead:
            legal |= (1 << overhead)
        else:
            if self.kickOpener:
                legal |= (1 << meleePunch) | (1 << meleePunchB) | (1 << meleeKick)
            elif self.meleeSequence == 0:
                legal |= (1 << meleePunch)
            elif self.meleeSequence == 1:
                legal |= (1 << meleePunchB)
            else:
                legal |= (1 << meleeKick)
        return legal

    def add_action(self, index):
        act = ACTIONS[index]
        self.actions.append(index)

        if index == jump:
            if self.isAirborne:
                self.hasDoubleJump = False
                self.hasJumpOverhead = True
                self.hangtime = 74
            else:
                self.hasDoubleJump = True
                self.hangtime = 55
            self.isAirborne = True
            if self.lastAnim == swing:
                self.hasSwingOverhead = True

        if index == uppercut:
            if not self.isAirborne:
                self.hasDoubleJump = True
            self.isAirborne = True
            self.hangtime = 108

        if index == land:
            self.isAirborne = False

        if not self.isAirborne:
            self.hasDoubleJump = False
            self.hasJumpOverhead = False
            self.hasSwingOverhead = False

        if index in (swing, swingWhiff):
            self.webUsed = cancellable[self.lastAnim][index]

        if index == swing or (self.lastAnim == swingWhiff and self.isAirborne):
            self.hasSwingOverhead = True
            self.hasDoubleJump = True
            self.hasJumpOverhead = False
            self.lastAnim = swing

        if index in (getOverHereTargetting, ffameStack, saporen):
            self.hasJumpOverhead = False
            self.hasSwingOverhead = False

        if index == uppercut:
            self.hasDoubleJump = True
            self.hasJumpOverhead = False

        if index == overhead:
            if self.hasSwingOverhead:
                self.hasSwingOverhead = False
            else:
                self.hasJumpOverhead = False
            self.webUsed = True

        cooldown_wait = 0
        if index == land:
            cooldown_wait = self.hangtime

        if index not in (jump, land) and not cancellable[self.lastAnim][index]:
            cooldown_wait += max(0, ACTIONS[self.lastAnim].delta_time)

        def charge_needed(charge, max_charge, charge_time):
            return (1 - charge) * charge_time if charge < 1 else 0

        cooldown_wait = max(cooldown_wait, charge_needed(self.tracerCharges, TRACER_MAX_CHARGES, TRACER_CHARGE_TIME) if index == tracer else 0)
        cooldown_wait = max(cooldown_wait, charge_needed(self.swingCharges, SWING_MAX_CHARGES, SWING_CHARGE_TIME) if index in (swing, swingWhiff) else 0)
        cooldown_wait = max(cooldown_wait, charge_needed(self.getOverHereCharges, GET_OVER_HERE_MAX_CHARGES, GET_OVER_HERE_CHARGE_TIME) if index in (getOverHere, getOverHereTargetting, ffameStack, saporen) else 0)
        cooldown_wait = max(cooldown_wait, charge_needed(self.uppercutCharges, UPPERCUT_MAX_CHARGES, UPPERCUT_CHARGE_TIME) if index in (uppercut, ffameStack) else 0)

        if index in (uppercut, ffameStack) and self.uppercutCooldown > 0:
            cooldown_wait = max(cooldown_wait, self.uppercutCooldown)

        if index == tracer and self.lastTracerTime + ACTIONS[tracer].delta_time > self.timeTaken + cooldown_wait:
            cooldown_wait = self.lastTracerTime + ACTIONS[tracer].delta_time - self.timeTaken

        self.timeTaken += act.cancel_time + cooldown_wait

        self.tracerActive = max(0, self.tracerActive - cooldown_wait)
        self.burnTracerActive = max(0, self.burnTracerActive - cooldown_wait)
        self.tracerCharges = min(TRACER_MAX_CHARGES, self.tracerCharges + cooldown_wait / TRACER_CHARGE_TIME)
        self.swingCharges = min(SWING_MAX_CHARGES, self.swingCharges + cooldown_wait / SWING_CHARGE_TIME)
        self.getOverHereCharges = min(GET_OVER_HERE_MAX_CHARGES, self.getOverHereCharges + cooldown_wait / GET_OVER_HERE_CHARGE_TIME)
        self.uppercutCharges = min(UPPERCUT_MAX_CHARGES, self.uppercutCharges + cooldown_wait / UPPERCUT_CHARGE_TIME)
        self.uppercutCooldown = max(0, self.uppercutCooldown - cooldown_wait)
        self.meleeSequenceWindow = max(0, self.meleeSequenceWindow - cooldown_wait)

        if not self.damageDealt and self.timeFromDamage:
            self.timeTaken = 0

        # Apply action effects
        if index == tracer:
            self.tracerActive = TRACER_ACTIVE_TIME
            self.tracerCharges -= 1
            self.lastTracerTime = self.timeTaken

        if index == burnTracer:
            self.burnTracerActive = TRACER_ACTIVE_TIME

        if index == swing:
            self.swingCharges -= 1

        if index in (getOverHereTargetting, ffameStack, saporen):
            if not self.tracerActive:
                return False
            self.getOverHereCharges -= 1
        elif index == getOverHere:
            self.getOverHereCharges -= 1

        if act.procs_tracer and self.tracerActive:
            self.damageDealt += TRACER_PROC_DAMAGE * (1.1 if self.hasSeasonalBuff else 1) * (1.12 if self.hasMantisBuff else 1)
            self.tracerActive = 0

        if act.procs_burn and self.burnTracerActive:
            self.damageDealt += BURNTRACER_DOT_TOTAL
            self.burnTracerActive = 0

        if index in (uppercut, ffameStack):
            self.uppercutCharges -= 1
            self.uppercutCooldown = UPPERCUT_COOLDOWN_TIME

        if index in (meleePunch, meleePunchB, meleeKick):
            if self.kickOpener:
                self.kickOpener = False
                self.meleeSequence = index - meleePunch
            elif not self.meleeSequenceWindow:
                if index == meleeKick:
                    self.damageDealt -= 15
                self.actions[-1] = meleePunch
                self.meleeSequence = 0
            self.meleeSequence = (self.meleeSequence + 1) % 3
            self.meleeSequenceWindow = MELEE_SEQUENCE_WINDOW

        self.tracerActive = max(0, self.tracerActive - act.cancel_time)
        self.burnTracerActive = max(0, self.burnTracerActive - act.cancel_time)
        self.tracerCharges = min(TRACER_MAX_CHARGES, self.tracerCharges + act.cancel_time / TRACER_CHARGE_TIME)
        self.swingCharges = min(SWING_MAX_CHARGES, self.swingCharges + act.cancel_time / SWING_CHARGE_TIME)
        self.getOverHereCharges = min(GET_OVER_HERE_MAX_CHARGES, self.getOverHereCharges + act.cancel_time / GET_OVER_HERE_CHARGE_TIME)
        self.uppercutCharges = min(UPPERCUT_MAX_CHARGES, self.uppercutCharges + act.cancel_time / UPPERCUT_CHARGE_TIME)
        self.uppercutCooldown = max(0, self.uppercutCooldown - act.cancel_time)
        self.meleeSequenceWindow = max(0, self.meleeSequenceWindow - act.cancel_time)
        self.hangtime = max(0, self.hangtime - cooldown_wait - act.cancel_time)

        self.damageDealt += act.damage * (1.1 if self.hasSeasonalBuff else 1) * (1.12 if self.hasMantisBuff else 1)

        if index not in (jump, land):
            self.lastAnim = index

        return True

    def get_action_string(self):
        encode = ["", "", "p", "P", "k", "o", "t", "s", "w", "g", "G", "u", "f", "n", "b"]
        return "".join(encode[i] for i in self.actions)

    def print(self):
        print(" -> ".join(ACTIONS[i].name for i in self.actions))
        print(f"Time: {self.timeTaken} frames ({self.timeTaken / 60:.2f} seconds)")
        print(f"Damage: {self.damageDealt:.1f}\n")
