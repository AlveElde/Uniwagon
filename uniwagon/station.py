# Station constants.
MOD_PER_ASM = 4
MOD_PER_BCN = 2
PRD_MOD_PRD = 0.10
PRD_MOD_SPD = -0.15
SPD_MOD_SPD = 0.50
BCN_EFF     = 0.50
ASM_SPD     = 1.25
ASM_PRD     = 1
BCN_SPD     = MOD_PER_BCN * SPD_MOD_SPD * BCN_EFF

# Printout constants.
LINE_LEN = 41

class Station:
    def __init__(self, asm = 2, bcn_per_asm = 8):
        self.asm = asm
        self.bcn_per_asm = bcn_per_asm
        self.crafting_speed = asm * (ASM_SPD * (1 + (BCN_SPD * bcn_per_asm) + (PRD_MOD_SPD * MOD_PER_ASM)))
        self.productivity = ASM_PRD * (1 + (PRD_MOD_PRD * MOD_PER_ASM))
        #TODO: Calculate efficiency


    def print(self):
        print("\n{0:-^{line_len}s}\n".format("Station", line_len=LINE_LEN))
        print("Station crafting speed:", self.crafting_speed)
        print("Station productivity  :", self.productivity)
        print("\n{0:-^{line_len}s}\n".format("", line_len=LINE_LEN))