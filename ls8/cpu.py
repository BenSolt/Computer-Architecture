"""CPU functionality."""

import sys

#MY CODE Day 1
HLT = 0b00000001 #HALT (exit)
LDI = 0b10000010 # Set the value of a register to an integer.
PRN = 0b01000111 # Print 

# MY CODE DAY 2
MUL = 0b10100010 #MULTIPLY

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #MY CODE DAY 1
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        #==============


    def load(self, program):
        """Load a program into memory."""

        address = 0

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

        with open(program) as f:

            for line in f:
                line = line.split("#")

                try: 
                    value = int(line[0],2)

                except ValueError:
                    continue
                
                self.ram[address] = value
                address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        #MY CODE Day 2 - multiply
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #=================
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
        # MY CODE DAY 1
        running = True

        while running:
            # ram = registers 1 - 8
            command = self.ram[self.pc]

            # LDI INSTRUCTION
            if command == LDI:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                move = (command >> 6) + 1
                self.pc += move

            # HLT INSTRUCTION       
            elif command == HLT:
                running = False    
            
            # PRN INSTRUCTION
            elif command == PRN:
                print(self.reg[self.ram[self.pc + 1]])
                move = (command >> 6) + 1
                self.pc += move

            # MY CODE DAY 2
            # MULTIPLY INSTRUCTION
            elif command == MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2]) 
                move = (command >> 6) + 1
                self.pc += move

            else:
                print(f'Unknown instruction {command} at address {self.pc}')
                sys.exit(1)
          

  #MY CODE DAY 1 Functions

    def ram_read(self, mar):
    
    #MAR: Memory Address Register, holds the memory address we're reading or writing

       mdr = self.ram[mar]
       return mdr

    def ram_write(self, mdr, mar):
 
    #MDR: Memory Data Register, holds the value to write or the value just read
    
        self.ram[mar] = mdr

#===================================================