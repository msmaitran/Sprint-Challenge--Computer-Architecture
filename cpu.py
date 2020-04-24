"""CPU functionality."""

import sys

program_filename = sys.argv[1]
# print(program_filename)
# sys.exit()

LDI = 130
PRN = 71
HLT = 1
MUL = 162
PUSH = 69
POP = 70
CALL = 80
RET = 17
ADD = 160
SP = 7

CMP = 167
JMP = 84
JEQ = 85
JNE = 86

E = None
L = None
G = None

AND = 168
OR = 170
XOR = 171
NOT = 105
SHL = 172
SHR = 173
MOD = 164

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, ram_index):
        return self.ram[ram_index]

    def ram_write(self, ram_index, ram_value):
        self.ram[ram_index] = ram_value

    def load(self, program_filename):
        """Load a program into memory."""

        address = 0
        with open(program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                inst = int(line, 2)
                self.ram[address] = inst
                address += 1
        
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            inst = self.ram[self.pc]
            if inst == LDI:
                index = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[index] = value
                self.pc += 3
            elif inst == PRN:
                index = self.ram_read(self.pc + 1)
                print(self.reg[index])
                self.pc += 2
            elif inst == HLT:
                running = False
            elif inst == MUL:
                num_one = self.ram_read(self.pc + 1)
                num_two = self.ram_read(self.pc + 2)
                multiplier = self.ram_read(num_one)
                multiplicand = self.ram_read(num_two)
                self.ram_write(num_one, multiplier * multiplicand)
                self.pc += 3
            elif inst == PUSH:
                index = self.ram_read(self.pc + 1)
                value = self.reg[index]
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], value)
                self.pc += 2
            elif inst == POP:
                index = self.ram_read(self.pc + 1)
                value = self.ram_read(self.reg[SP])
                self.reg[index] = value
                self.reg[SP] += 1
                self.pc += 2
            elif inst == CALL:
                return_addr = self.pc + 2
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], return_addr)
                reg_num = self.ram_read(self.pc + 1)
                dest_addr = self.reg[reg_num]
                self.pc = dest_addr
            elif inst == RET:
                return_addr = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                self.pc = return_addr
            elif inst == ADD:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                value_a = self.reg[reg_a]
                value_b = self.reg[reg_b]
                self.reg[reg_a] = value_a + value_b
                self.pc += 3
            elif inst == CMP:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                value_a = self.reg[reg_a]
                value_b = self.reg[reg_b]
                if value_a == value_b:
                    E = 1
                    L = 0
                    G = 0
                elif value_a < value_b:
                    E = 0
                    L = 1
                    G = 0
                elif value_a > value_b:
                    E = 0
                    L = 0
                    G = 1
                self.pc += 3
            elif inst == JMP:
                reg = self.ram_read(self.pc + 1)
                dest_addr = self.reg[reg]
                self.pc = dest_addr
            elif inst == JEQ:
                if E == 1:
                    reg = self.ram_read(self.pc + 1)
                    dest_addr = self.reg[reg]
                    self.pc = dest_addr
                else: self.pc += 2
            elif inst == JNE:
                if E == 0:
                    reg = self.ram_read(self.pc + 1)
                    dest_addr = self.reg[reg]
                    self.pc = dest_addr
                else:
                    self.pc += 2
            elif inst == AND:
                self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
                self.pc += 3
            elif inst == OR:
                self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
                self.pc += 3
            elif inst == XOR:
                self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
                self.pc += 3
            elif inst == NOT:
                self.reg[reg_a] = ~ self.reg[reg_a]
                self.pc += 2
            elif inst == SHL:
                shift = self.reg[reg_b]
                value = self.reg[reg_a] << shift
                self.reg[reg_a] == value
                self.pc += 3
            elif inst == SHR:
                shift = self.reg[reg_b]
                value = self.reg[reg_a] >> shift
                self.reg[reg_a] == value
                self.pc += 3
            elif inst == MOD:
                if self.reg[reg_b] == 0:
                    HLT
                self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
                self.pc += 3
            else:
                print("Unknown instruction")

cpu = CPU()
cpu.load(program_filename)
# cpu.run()