use anyhow::anyhow;
use itertools::Itertools;
use std::fs;

/// Represents an IntCode Program
#[derive(Clone)]
pub struct IntCode {
    code: Vec<usize>,
}

impl IntCode {
    /// Create a new IntCode program based off a IntCode program file
    pub fn new(file_path: &str) -> anyhow::Result<Self> {
        let op_code_string = fs::read_to_string(file_path)?;
        Ok(Self {
            code: op_code_string
                .split(",")
                .map(|code| Ok::<usize, anyhow::Error>(code.parse()?))
                .try_collect()?,
        })
    }

    /// Get a program at the address
    pub fn get_program_at_address(self, address: usize) -> usize {
        self.code[address]
    }

    /// Update program at a specific address in the IntCode
    pub fn update_program_at_address(
        &mut self,
        new_program: usize,
        address: usize,
    ) -> anyhow::Result<()> {
        self.code[address] = new_program;
        Ok(())
    }

    /// Run the current IntCode program
    pub fn run(&mut self) -> anyhow::Result<()> {
        let mut instruction_pointer = 0;
        while instruction_pointer <= self.code.len() {
            // Other 3 values in this op code `(lhs_pos, rhs_pos, insert_pos)`
            let lhs_position = self.code[instruction_pointer + 1];
            let rhs_position = self.code[instruction_pointer + 2];
            let insert_position = self.code[instruction_pointer + 3];

            // Run instruction
            self.code[insert_position] = match self.code[instruction_pointer] {
                1 => {
                    instruction_pointer += 4;
                    Ok(self.code[lhs_position] + self.code[rhs_position])
                }
                2 => {
                    instruction_pointer += 4;
                    Ok(self.code[lhs_position] * self.code[rhs_position])
                }
                99 => break,
                bad_op_code => Err(anyhow!(
                    "Unsupported op code found for the current IntCode Compiler: {bad_op_code}"
                )),
            }?;
        }

        Ok(())
    }
}
