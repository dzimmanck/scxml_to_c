from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow)

state_machine_result_t = Enum('state_machine_result_t', prefix='EVENT_')
state_machine_result_t.add_value("UN_HANDLED", 1)

if __name__ == "__main__":
    print(f'{st`ate_machine_result_t.values[0]}')