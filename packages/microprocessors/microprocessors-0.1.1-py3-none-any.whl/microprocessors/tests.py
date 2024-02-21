import unittest
from microprocessors.processors import RiSC16

class TestRiSC16(unittest.TestCase):

    def test_addi_instruction(self):
        """Test loading a value into a register using the ADDI instruction."""
        print("\nSTART TEST 1")
        risc = RiSC16()
        # Use ADDI to simulate loading an immediate value into R1.
        risc.addi(1, 0, 10)  # Equivalent to LI R1, 10 if LI were available.
        self.assertEqual(risc.registers[1], 10, "ADDI failed to load 10 into R1")

    def test_lui_addi_combo(self):
        """Test loading a larger value into a register using a combination of LUI and ADDI."""
        print("\nSTART TEST 2")
        risc = RiSC16()
        # First, set the upper bits with LUI, assuming it sets the top half of the register.
        risc.lui(1, 1)  # Hypothetically sets the upper 16 bits of R1 to 1.
        # Then, use ADDI to set the lower bits.
        risc.addi(1, 1, 2)  # Assuming this adds 2 to the lower bits of R1.
        # The exact expected value depends on the implementation of LUI and ADDI.
        # This assertion needs adjustment based on the specific behavior of those instructions.
        expected_value = (1 << 6) + 2  # Adjust based on your LUI and ADDI implementation.
        self.assertEqual(risc.registers[1], expected_value, "Combination of LUI and ADDI failed to set expected value")

    def test_program_execution_halt(self):
        """Test program execution and halting condition."""
        print("\nSTART TEST 3")
        risc = RiSC16()
        # Simulate a program that sets R7 to halt the execution.
        risc.addi(7, 0, 1)  # Directly using ADDI to set R7 as a halt flag.
        risc.run()
        self.assertTrue(risc._halt, "The program did not halt as expected")
        self.assertEqual(risc.registers[7], 1, "R7 was not set correctly to indicate halt")


    def test_full_instruction_set(self):
        print("\nSTART TEST 4")
        risc = RiSC16(verbose=2)

        # Properly queue instructions
        risc.encode_instruction('ADDI', 1, 0, 5)  # R1 = 5
        risc.encode_instruction('LUI', 2, None, 1)      # R2 = 1 << (16 - immediate_bits)
        risc.encode_instruction('ADD', 3, 1, 2)   # R3 = R1 + R2
        risc.encode_instruction('NAND', 4, 1, 2)  # R4 = ~(R1 & R2)
        risc.encode_instruction('SW', 3, 0, 10)   # Memory[10] = R3
        risc.encode_instruction('LW', 5, 0, 10)   # R5 = Memory[10]
        risc.encode_instruction('BEQ', 1, 2, 2)   # if R1 == R2, skip next 2 instructions
        risc.encode_instruction('ADDI', 6, 0, 1)  # R6 = 1 (skipped if R1 == R2)
        risc.encode_instruction('JALR', 7, 0)     # R7 = PC + 1; PC = R0

        # Run all and visalize register at final state
        risc.run_program()
        risc.visualize_state()

        # Assertions to verify outcomes after executing the instructions
        self.assertEqual(risc.registers[1], 5, "ADDI failed to properly load 5 into R1")
        self.assertNotEqual(risc.registers[3], 0, "ADD failed to correctly add R1 and R2")
        self.assertNotEqual(risc.registers[4], 0, "NAND failed to correctly NAND R1 and R2")
        self.assertEqual(risc.registers[5], risc.registers[3], "LW/SW failed to load/store correctly")


    def test_beq_instruction(self):
        print("\nSTART TEST 5")
        risc = RiSC16(verbose=2)
        # Set R1 and R2 to the same value and test BEQ
        risc.encode_instruction('ADDI', 1, 0, 5)  # R1 = 5
        risc.encode_instruction('ADDI', 2, 0, 5)  # R2 = 5
        risc.encode_instruction('BEQ', 1, 2, 2)   # PC should jump by 2 if R1 == R2
        risc.run_program()

        # PC should be 3 (3 instructions executed, PC incremented after each fetch)
        self.assertEqual(risc.pc, 5, "BEQ failed to correctly modify PC when conditions are met")

    def test_jalr_instruction(self):
        print("\nSTART TEST 6")
        risc = RiSC16(verbose=2)
        # Setup for JALR: jump to address in R1 (which will be set to 0 for simplicity)
        risc.encode_instruction('ADDI', 1, 0, 0)  # R1 = 0 (jump target)
        risc.encode_instruction('JALR', 7, 1)     # R7 = PC + 1 (return address), jump to R1
        risc.run_program()

        # After JALR, R7 should hold the return address (PC before jump + 1) and PC should be the value in R1
        self.assertEqual(risc.registers[7], 2, "JALR failed to store return address in R7")
        self.assertEqual(risc.pc, 0, "JALR failed to jump to address in R1")




if __name__ == '__main__':
    unittest.main()
