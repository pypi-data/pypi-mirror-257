class RiSC16:
    """
    A simulation of the RiSC-16 (Ridiculously Simple Computer - 16 bit) processor.

    Attributes:
        registers (list): An array of 8 general-purpose registers for operations.
        pc (int): The Program Counter register that tracks the current instruction address.
        memory (list): A simulated main memory with a fixed size of 256 words.
        instructions (dict): A mapping of instruction mnemonics to their implementation methods.
    """

    def __init__(self, verbose=2):
        """
        Initializes the RiSC-16 simulator with default values.
        :param verbose: no print if 0, only prints visualisation if 1, details every step if 2
        """
        self.registers = [0] * 8
        self._pc = 0  # Make PC private
        self._memory = [0] * 256  # Make memory private
        self._halt = False  # Make halt private
        self.instructions = {
            'ADD': self.add,
            'ADDI': self.addi,
            'NAND': self.nand,
            'LUI': self.lui,
            'SW': self.sw,
            'LW': self.lw,
            'BEQ': self.beq,
            'JALR': self.jalr
        }
        self.instructions_queue = []  # Add an instructions queue
        self.verbose = verbose  # automatically shows the state when "run" is called or not
        self.user_message("a RiSC-16 got initialised with self.verbose=2", "__init__")

    @property
    def pc(self):
        """Property to access the program counter."""
        return self._pc

    @pc.setter
    def pc(self, value):
        """Property setter to update the program counter in a controlled manner."""
        if isinstance(value, int):
            self._pc = value
            self.user_message(f"changed self._pc to {value}", "@pc.setter")
        else:
            raise ValueError("PC must be an integer")

    @property
    def memory(self):
        """Property to access the memory. Returns a copy to prevent direct modification."""
        return self._memory[:]

    def write_memory(self, address, value):
        """
        Writes a value to a specific address in the memory.
        This method ensures that memory modifications are controlled and can enforce any additional rules or checks.
        """
        if not (0 <= address < len(self._memory)):
            raise ValueError("Address out of bounds")
        if not isinstance(value, int):
            raise ValueError("Memory value must be an integer")

        self._memory[address] = value
        self.user_message(f"address {address} of memory set to {value}", "write_memory")

    def fetch(self):
        """
        Fetches the instruction from memory at the current PC location and increments the PC.

        Returns:
            int: The fetched instruction.
        """
        instruction = self.memory[self.pc]
        self.pc += 1
        self.user_message(f"incremented self.pc to {self.pc}", "fetch")
        return instruction

    def decode(self, instruction):
        """
        Decodes an instruction to extract the opcode.

        Parameters:
            instruction (int): The instruction word to decode.

        Returns:
            int: The opcode extracted from the instruction.
        """
        opcode = (instruction >> 12) & 0xF
        self.user_message(f"instruction {instruction} decoded as opcode {opcode}", "decode")
        return opcode

    def execute(self, opcode, *args):
        """
        Executes the instruction corresponding to the given opcode with provided arguments.

        Parameters:
            opcode (int): The opcode that determines which instruction to execute.
            *args: Arguments needed by the instruction methods.
        """
        if opcode in self.instructions:
            self.user_message(f"executing instruction at opcode {opcode}...", "execute")
            self.instructions[opcode](*args)
        else:
            print("Unknown instruction")

    def add(self, regA, regB, regC):
        """
        Implements the ADD instruction to add values of two registers and store the result in another.

        Parameters:
            regA (int): The index of the destination register.
            regB (int), regC (int): The indices of the source registers.
        """
        self.registers[regA] = self.registers[regB] + self.registers[regC]
        self.user_message(f"ADD was executed: self.registers[{regA}]={self.registers[regA]}",
                          "add")

    def addi(self, regA, regB, immediate):
        """
        Implements the ADDI instruction to add a register value and an immediate value.

        Parameters:
            regA (int): The index of the destination register.
            regB (int): The index of the source register.
            immediate (int): The immediate value to add.
        """
        self.registers[regA] = self.registers[regB] + immediate
        self.user_message(f"ADDI was executed: self.registers[{regA}]={self.registers[regA]}",
                          "addi")

    def nand(self, regA, regB, regC):
        """
        Implements the NAND instruction, performing a bitwise NAND on two registers.

        Parameters:
            regA (int): The index of the destination register.
            regB (int), regC (int): The indices of the source registers.
        """
        self.registers[regA] = ~(self.registers[regB] & self.registers[regC])
        self.user_message(f"NAND was executed: self.registers[{regA}]={self.registers[regA]}",
                          "nand")

    def lui(self, regA, regB, immediate=None):
        """
        Implements the LUI (Load Upper Immediate) instruction to load an immediate value into the upper bits of a register.

        Parameters:
            regA (int): The index of the destination register.
            immediate (int): The immediate value to load.
        """
        if immediate is None:
            immediate = regB

        self.registers[regA] = immediate << 6
        self.user_message(f"LUI was executed: self.registers[{regA}]={self.registers[regA]}",
                          "lui")

    def sw(self, regA, regB, immediate):
        """
        Implements the SW (Store Word) instruction to store a register's value into memory.

        Parameters:
            regA (int): The index of the source register.
            regB (int): The index of the base address register.
            immediate (int): The offset to add to the base address.
        """
        address = self.registers[regB] + immediate
        self.write_memory(address, self.registers[regA])
        self.user_message(f"SW was executed: self.memory[{address}]={self.memory[address]}",
                          "sw")

    def lw(self, regA, regB, immediate):
        """
        Implements the LW (Load Word) instruction to load a memory value into a register.

        Parameters:
            regA (int): The index of the destination register.
            regB (int): The index of the base address register.
            immediate (int): The offset to add to the base address.
        """
        address = self.registers[regB] + immediate
        self.registers[regA] = self.memory[address]
        self.user_message(f"LW was executed: self.registers[{regA}]={self.registers[regA]}",
                          "lw")

    def beq(self, regA, regB, immediate):
        """
        Implements the BEQ (Branch if Equal) instruction to alter the program flow if two registers are equal.

        Parameters:
            regA (int), regB (int): The indices of the registers to compare.
            immediate (int): The value to add to the PC if the comparison is true.
        """
        if self.registers[regA] == self.registers[regB]:
            self.pc += immediate
        self.user_message(f"BEQ was executed: self.pc={self.pc}","beq")

    def jalr(self, regA, regB, immediate=None):
        """
        Implements the JALR (Jump And Link Register) instruction for function calls.

        Parameters:
            regA (int): The index of the register to store the return address.
            regB (int): The index of the register containing the jump target address.
        """
        self.registers[regA] = self.pc
        self.pc = self.registers[regB]
        self.user_message(f"JALR was executed: self.pc={self.pc}","jalr")


    def run(self):
        """
        Continuously fetches, decodes, and executes instructions from memory.

        This method implements the main execution loop of the RiSC-16 processor simulation.
        It fetches instructions from the memory at the address pointed to by the program counter (PC),
        decodes the fetched instruction to identify the opcode and extract any arguments,
        and then executes the instruction using the appropriate method.

        The loop continues indefinitely until a halt condition is met. This condition could be
        a specific instruction, a memory address, or an external signal, depending on the implementation.
        """
        while not self._halt:
            self.user_message("START NEW RUN ITERATION...", "run")
            if self.verbose > 0:
                self.visualize_state()  # Optional: Visualize state before executing the next instruction
            instruction = self.fetch()
            opcode = self.decode(instruction)
            args = self.extract_args(instruction)
            self.execute(opcode, *args)

            # Check if the halt condition is met (e.g., R7 is set to a specific value)
            if self.registers[7] == 1:  # Assuming writing 1 to R7 signals halt
                self.user_message("HALT DETECTED. STOP RUNNING.", "run")
                self._halt = True

    def extract_args(self, instruction):
        """
        Extracts arguments from an instruction word based on the RiSC-16 instruction format.

        Parameters:
            instruction (int): The instruction word from which to extract arguments.

        Returns:
            list: A list of arguments extracted from the instruction. This could include
                  register indices and immediate values, depending on the instruction type.
        """
        # Example extraction logic for a simple format where instructions are assumed
        # to have up to two arguments following the opcode.
        arg1 = (instruction >> 6) & 0x3F  # Extract bits 6-11 as arg1
        arg2 = instruction & 0x3F        # Extract bits 0-5 as arg2
        self.user_message(f"Extracted arg1 and arg2 from instruction {instruction}", "extract_args")
        return [arg1, arg2]

    def visualize_state(self):
        """
        Prints a visualization of the current state of the RiSC-16 simulator.

        This includes the value of all registers, the program counter (PC), and the current instruction
        being executed. For educational purposes, showing a snippet of memory around the current
        instruction could also be valuable, but is left as an enhancement for brevity.
        """
        print("Current State:")
        print("--------------")
        print(f"PC: {self.pc}")
        print("Registers:")
        for i, val in enumerate(self.registers):
            print(f"R{i}: {val}")
        # Optionally, show the current instruction in a more readable format
        # This requires translating the instruction back to assembly-like notation
        # which might involve reversing the decoding process or mapping opcodes to mnemonics
        instruction = self.memory[self.pc] if self.pc < len(self.memory) else 'N/A'
        opcode = self.decode(instruction)
        mnemonic = next((k for k, v in self.instructions.items() if v.__name__.upper() == opcode), 'UNKNOWN')
        print(f"Next Instruction: {mnemonic} (Raw: {instruction})")
        print("--------------\n")

    def encode_instruction(self, mnemonic, regA, regB, immediate=0):
        """
        Prepares an instruction for execution by adding it to the instructions queue.

        This method does not encode instructions into a binary format but rather queues
        them for execution in a format that matches the methods available in this class.

        Parameters:
            mnemonic (str): The instruction mnemonic (e.g., 'ADDI').
            regA (int), regB (int): Register indices for the operation.
            immediate (int): An immediate value for instructions that use it.
        """
        if mnemonic not in self.instructions:
            raise ValueError(f"Unknown instruction mnemonic: {mnemonic}")

        # Queue the instruction for later execution
        self.user_message(f"appending instruction {(mnemonic, regA, regB, immediate)} to queue...",
                          "encode_instruction")
        self.instructions_queue.append((mnemonic, regA, regB, immediate))

    def run_program(self):
        """
        Executes all instructions in the instructions queue.
        """
        start = True
        while self.instructions_queue:
            self.pc += 1
            self.user_message("EXECUTING NEXT INSTRUCTION...", "run_program")
            mnemonic, regA, regB, immediate = self.instructions_queue.pop(0)
            if mnemonic in self.instructions.keys():
                # Call the appropriate method from self.instructions
                self.instructions[mnemonic](regA, regB, immediate)
            else:
                raise ValueError(f"Execution of unknown instruction mnemonic: {mnemonic}")

        self.user_message("PROGRAM RUN SUCCESSFULLY.", "run_program")

    def user_message(self, message, fun):
        if self.verbose >= 2:
            print(f"RiSC-16 in \"{fun}\": ", message)