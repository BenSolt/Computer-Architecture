"""CPU functionality."""

import sys

#MY CODE Day 1
HLT = 0b00000001 #HALT (exit)
LDI = 0b10000010 # Set the value of a register to an integer.
PRN = 0b01000111 # Print 

# MY CODE DAY 2
MUL = 0b10100010 #MULTIPLY
ADD = 0b10100000 # adds numbers together

PUSH = 0b01000101 # Add
POP = 0b01000110 # Remove
CALL = 0b01010000
RET = 0b00010001 

#SPRINT========

CMP = 0b10100111 
JMP = 0b01010100 
JEQ = 0b01010101 
JNE = 0b01010110 



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #MY CODE DAY 1
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xf4 # SP = STACK/F4, register 7.
        self.reg[7] = self.sp
        
        #SPRINT
        self.equal = 0
        self.less = 0
        self.great = 0


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

        # SPRINT =============================
 
        elif op == "CMP":
            """
            Compare registers regA and regB
            If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            """   

            self.equal = 0
            self.less = 0
            self.great = 0
            # register, memory, program counter 1
            # register, memory, program counter 2
            reg_a = self.reg[self.ram[self.pc +1]]
            reg_b = self.reg[self.ram[self.pc +2]]

            # if reg program counter 1 == reg program counter 2
            if reg_a == reg_b: 
                self.equal = 1
            
            # less than
            elif reg_a < reg_b:
                self.less = 1

            # greater than   
            elif reg_a > reg_b:
                self.great = 1

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

            elif command == ADD:
                self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2]) 
                move = (command >> 6) + 1
                self.pc += move

            #MY CODE DAY 3
            elif command == PUSH:
                
                """
                Push the value in the given register on the stack.
                Decrement the SP.
                Copy the value in the given register to the address pointed to by SP.
                """
                # decrement stack pointer, SP = R7
                self.sp -= 1

                # get a value from the given register
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]    

                #put the value at the stack pointer address
                self.ram[self.sp] = value

                self.pc += 2

            elif command == POP:
                
                """
                Pop the value at the top of the stack into the given register.
                Copy the value from the address pointed to by SP to the given register.
                Increment SP.
                """
                reg_num2 = self.ram[self.pc +1]
                self.reg[reg_num2] = self.ram[self.sp]
                # increment stack pointer
                self.sp += 1
                # increment program counter
                self.pc += 2


            # MY CODE DAY 4
            elif command == CALL:
                """
                Calls a subroutine (function) at the address stored in the register.
                1.The address of the instruction directly after CALL is 
                pushed onto the stack. This allows us to return to where
                we left off when the subroutine finishes executing.
                2.The PC is set to the address stored in the given register. 
                We jump to that location in RAM and execute the first instruction in the subroutine. 
                The PC can move forward or backwards from its current location
               
                """
                return_address = self.pc + 2 # going to RET 2
                #push on the stack
                self.sp -= 1
                self.ram[self.sp] = return_address
                # get address to call
                reg_num = self.ram[self.pc +1]
                subrouting_address = self.reg[reg_num]
                # call it
                self.pc = subrouting_address


            elif command == RET:
                """
                Return from subroutine
                Pop the value from the top of the stack and store it in PC
                """
                #program counter (PC) = memory and stack
                self.pc = self.ram[self.sp]
                #stack
                self.sp += 1


            #SPRINT CODE ======================================
          


            elif command == CMP:
                """
                If they are equal, set the Equal E flag to 1, otherwise set it to 0.
                If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
                If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
                """
                self.alu("CMP", self.ram[self.pc + 1], self.ram[self.pc + 2]) 
                move = (command >> 6) + 1
                self.pc += move
                

            
            elif command == JMP:
                """JMP"""
                # get address stored in register, aka memory(ram)
                reg_num = self.ram[self.pc + 1]
                # jump adddress
                jump_address = self.reg[reg_num]
                # Set the PC to the address stored in the given register.
                self.pc = jump_address
                


           
            elif command == JEQ:
                """
                JEQ - If equal flag is set (true) jump to the address stored in the given register.  
                """
                if self.equal == 1:
                    reg_num = self.ram[self.pc +1]
                    # jump to the address stored in the given register. 
                    jump_address = self.reg[reg_num] 
                    self.pc = jump_address

                else:
                    move = (command >> 6) + 1
                    self.pc += move


           
            elif command == JNE:
                """
                JNE - If equal flag is clear (false, 0), jump to the address stored in the given register.
                """
                if self.equal == 0:
                    reg_num = self.ram[self.pc +1]
                    # jump to the address stored in the given register. 
                    jump_address = self.reg[reg_num] 
                    self.pc = jump_address
                
                else:
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