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
    println!(
        "Op code at position 0 after the program runs is: {}",
        intcode.get_program_at_address(0)
    );

    Ok(())
}

/// Part 2 Stuff
fn part_2() -> anyhow::Result<()> {
    // Load our intcode program
    let intcode = IntCode::new("data/input.txt")?;

    // Go through all possible programs at addresses 1 and 2
    // checking each time if the total matches the desired value
    let mut objective_found = false;
    for noun in 0..99 {
        for verb in 0..99 {
            // Clone our intcode each time so we don't carry forward any previous
            // attempt's mutations
            let mut curr_intcode = intcode.clone();

            // Assign the values at address 1 and 2
            curr_intcode.update_program_at_address(noun, 1)?;
            curr_intcode.update_program_at_address(verb, 2)?;

            // Run the code and check if the value at index 0 is the desired one
            curr_intcode.run()?;
            let result = curr_intcode.get_program_at_address(0);
            if result == 19690720 {
                println!("Objective found!\nNoun: {noun}\nVerb: {verb}");
                println!("Result: {}", 100 * noun + verb);
                objective_found = true;
                break;
            }
        }

        if objective_found {
            break;
        }
    }

    // If we never found our objective, log it
    if !objective_found {
        println!("Aw man, we never found our objective value :(\n");
    }

    Ok(())
}

/// Main runner for Day 02
fn main() -> anyhow::Result<()> {
    println!("Part 1:\n-------\n");
    part_1()?;
    println!("\n\nPart 2:\n-------\n");
    part_2()?;
    Ok(())
}
