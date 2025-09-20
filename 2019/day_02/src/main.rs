use std::fs;
use anyhow::anyhow;
use itertools::Itertools;

/// Read in op code input
fn read_input(file_path: &str) -> anyhow::Result<Vec<usize>> {
    let op_code_string = fs::read_to_string(file_path)?;
    op_code_string.split(",").map(|code| Ok(code.parse()?)).try_collect()
}

/// Part 1 Stuff
fn part_1() -> anyhow::Result<()> {
    // Read in the op codes
    let mut op_codes = read_input("data/input.txt")?;

    // Mutate for the 1202 program declaration
    op_codes[1] = 12;
    op_codes[2] = 2;

    // Run the op code
    for i in (0..op_codes.len()).step_by(4){
        // Other 3 values in this op code `(lhs_pos, rhs_pos, insert_pos)`
        let lhs_position = op_codes[i+1];
        let rhs_position = op_codes[i+2];
        let insert_position = op_codes[i+3];

        // Determine value and insert
        op_codes[insert_position] = match op_codes[i] {
            1 => Ok(op_codes[lhs_position] + op_codes[rhs_position]),
            2 => Ok(op_codes[lhs_position] * op_codes[rhs_position]),
            99 => break,
            bad_op_code => Err(anyhow!("Unsupported op code found: {bad_op_code}"))
        }?;
    }

    // Output result
    println!("Op code at position 0 after the program runs is: {}", op_codes[0]);

    Ok(())
}

/// Part 2 Stuff
fn part_2() -> anyhow::Result<()> {
    todo!()
}

/// Main runner for Day 01
fn main() -> anyhow::Result<()> {
    part_1()?;
    // part_2()?;
    Ok(())
}
