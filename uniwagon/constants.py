class Constants:
    # Train contants.
    INITAL_OUTPUT = 1

    # Wagon constants.
    STACK_CAPACITY = 40

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