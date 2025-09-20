use nr_intcode::IntCode;

/// Part 1 Stuff
fn part_1() -> anyhow::Result<()> {
    // Load our intcode program
    let mut intcode = IntCode::new("data/input.txt")?;

    // Update some programs at specific addresses
    intcode.update_program_at_address(12, 1)?;
    intcode.update_program_at_address(2, 2)?;

    // Run the program
    intcode.run()?;

    // Output result
    println!("Part 1:\n-------\n");
    println!(
        "Op code at position 0 after the program runs is: {}",
        intcode.get_program_at_address(0)
    );

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
