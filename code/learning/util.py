__author__ = 'Marcelo d\'Almeida'

from collections import namedtuple

POWER = "Power"
POWER_0_to_10_PERCENT = "Power 0% to 10%"
POWER_10_to_30_PERCENT = "Power 10% to 30%"
POWER_30_to_50_PERCENT = "Power 30% to 50%"
POWER_50_to_70_PERCENT = "Power 50% to 70%"
POWER_70_to_90_PERCENT = "Power 70% to 90%"
POWER_90_to_100_PERCENT = "Power 90% to 100%"

power_state_dict = {POWER_0_to_10_PERCENT  : 0,
                    POWER_10_to_30_PERCENT : 1,
                    POWER_30_to_50_PERCENT : 2,
                    POWER_50_to_70_PERCENT : 3,
                    POWER_70_to_90_PERCENT : 4,
                    POWER_90_to_100_PERCENT: 5,

                    0: POWER_0_to_10_PERCENT ,
                    1: POWER_10_to_30_PERCENT,
                    2: POWER_30_to_50_PERCENT,
                    3: POWER_50_to_70_PERCENT,
                    4: POWER_70_to_90_PERCENT,
                    5: POWER_90_to_100_PERCENT}

COST = "Cost"
COST_0_to_10_PERCENT = "Cost 0% to 10%"
COST_10_to_30_PERCENT = "Cost 10% to 30%"
COST_30_to_50_PERCENT = "Cost 30% to 50%"
COST_50_to_70_PERCENT = "Cost 50% to 70%"
COST_70_to_90_PERCENT = "Cost 70% to 90%%"
COST_90_to_100_PERCENT = "Cost 90% to 100%"

cost_state_dict = {COST_0_to_10_PERCENT  : 0,
                   COST_10_to_30_PERCENT : 1,
                   COST_30_to_50_PERCENT : 2,
                   COST_50_to_70_PERCENT : 3,
                   COST_70_to_90_PERCENT : 4,
                   COST_90_to_100_PERCENT: 5,

                   0: COST_0_to_10_PERCENT,
                   1: COST_10_to_30_PERCENT,
                   2: COST_30_to_50_PERCENT,
                   3: COST_50_to_70_PERCENT,
                   4: COST_70_to_90_PERCENT,
                   5: COST_90_to_100_PERCENT}

DELAY = "Delay"
DELAY_0_to_10_PERCENT = "Delay 0% to 10%"
DELAY_10_to_30_PERCENT = "Delay 10% to 30%"
DELAY_30_to_50_PERCENT = "Delay 30% to 50%"
DELAY_50_to_70_PERCENT = "Delay 50% to 70%"
DELAY_70_to_90_PERCENT = "Delay 70% to 90%"
DELAY_90_to_100_PERCENT = "Delay 90% to 100%"

delay_state_dict = {DELAY_0_to_10_PERCENT   : 0,
                    DELAY_10_to_30_PERCENT  : 1,
                    DELAY_30_to_50_PERCENT  : 2,
                    DELAY_50_to_70_PERCENT  : 3,
                    DELAY_70_to_90_PERCENT  : 4,
                    DELAY_90_to_100_PERCENT : 5,

                    0: DELAY_0_to_10_PERCENT,
                    1: DELAY_10_to_30_PERCENT,
                    2: DELAY_30_to_50_PERCENT,
                    3: DELAY_50_to_70_PERCENT,
                    4: DELAY_70_to_90_PERCENT,
                    5: DELAY_90_to_100_PERCENT}

PERCENTAGE_0_to_10 = "0% to 10%"
PERCENTAGE_10_to_30 = "10% to 30%"
PERCENTAGE_30_to_50 = "30% to 50%"
PERCENTAGE_50_to_70 = "50% to 70%"
PERCENTAGE_70_to_90 = "70% to 90%"
PERCENTAGE_90_to_100 = "90% to 100%"

percentage_dict = {PERCENTAGE_0_to_10   : 0,
                   PERCENTAGE_10_to_30  : 1,
                   PERCENTAGE_30_to_50  : 2,
                   PERCENTAGE_50_to_70  : 3,
                   PERCENTAGE_70_to_90  : 4,
                   PERCENTAGE_90_to_100 : 5,

                   0: PERCENTAGE_0_to_10,
                   1: PERCENTAGE_10_to_30,
                   2: PERCENTAGE_30_to_50,
                   3: PERCENTAGE_50_to_70,
                   4: PERCENTAGE_70_to_90,
                   5: PERCENTAGE_90_to_100}

LIGHT_MACHINE = "Light Machine"
MEDIUM_MACHINE = "Medium Machine"
HEAVY_MACHINE = "Heavy Machine"

LIGHT_TASK = "Light Task"
MEDIUM_TASK = "Medium Task"
HEAVY_TASK = "Heavy Task"


DO_NOTHING = "Do Nothing+Do Nothing"
LIGHT_TASK_LIGHT_MACHINE   = LIGHT_TASK  + "+" + LIGHT_MACHINE
LIGHT_TASK_MEDIUM_MACHINE  = LIGHT_TASK  + "+" + MEDIUM_MACHINE
LIGHT_TASK_HEAVY_MACHINE   = LIGHT_TASK  + "+" + HEAVY_MACHINE
MEDIUM_TASK_LIGHT_MACHINE  = MEDIUM_TASK + "+" + LIGHT_MACHINE
MEDIUM_TASK_MEDIUM_MACHINE = MEDIUM_TASK + "+" + MEDIUM_MACHINE
MEDIUM_TASK_HEAVY_MACHINE  = MEDIUM_TASK + "+" + HEAVY_MACHINE
HEAVY_TASK_LIGHT_MACHINE   = HEAVY_TASK  + "+" + LIGHT_MACHINE
HEAVY_TASK_MEDIUM_MACHINE  = HEAVY_TASK  + "+" + MEDIUM_MACHINE
HEAVY_TASK_HEAVY_MACHINE   = HEAVY_TASK  + "+" + HEAVY_MACHINE


actions_dict = {DO_NOTHING                : 0,
                LIGHT_TASK_LIGHT_MACHINE  : 1,
                LIGHT_TASK_MEDIUM_MACHINE : 2,
                LIGHT_TASK_HEAVY_MACHINE  : 3,
                MEDIUM_TASK_LIGHT_MACHINE : 4,
                MEDIUM_TASK_MEDIUM_MACHINE: 5,
                MEDIUM_TASK_HEAVY_MACHINE : 6,
                HEAVY_TASK_LIGHT_MACHINE  : 7,
                HEAVY_TASK_MEDIUM_MACHINE : 8,
                HEAVY_TASK_HEAVY_MACHINE  : 9,

                0: DO_NOTHING,
                1: LIGHT_TASK_LIGHT_MACHINE,
                2: LIGHT_TASK_MEDIUM_MACHINE,
                3: LIGHT_TASK_HEAVY_MACHINE,
                4: MEDIUM_TASK_LIGHT_MACHINE,
                5: MEDIUM_TASK_MEDIUM_MACHINE,
                6: MEDIUM_TASK_HEAVY_MACHINE,
                7: HEAVY_TASK_LIGHT_MACHINE,
                8: HEAVY_TASK_MEDIUM_MACHINE,
                9: HEAVY_TASK_HEAVY_MACHINE}


StateInfo = namedtuple("StateInfo", "power_state cost_state delay_state, time_state")

SEPARATOR = "--------------------------------------------------------------------------------------------------------------------------------------"