use std::{
    fs::File,
    io::{BufRead, BufReader},
};

use cached::proc_macro::cached;

/// Read in input ints line by line from disk
fn read_input_ints_from_disk(file_path: &str) -> anyhow::Result<Vec<i64>> {
    let input = File::open(file_path)?;
    let buffered = BufReader::new(input);
    buffered
        .lines()
        .map(|line| Ok(line?.parse::<i64>()?))
        .collect()
}

/// Get the required fuel for a module by dividing the mass by 3 and subtracting 2
fn get_required_fuel_for_mass(mass: i64) -> i64 {
    mass / 3 - 2
}

/// Get the required fuel for a module AND all its required fuel mass (recursive solve).
#[cached]
fn get_required_full_fuel_for_mass(mass: i64) -> i64 {
    let required_fuel_mass = mass / 3 - 2;
    // base case
    if required_fuel_mass <= 0 {
        return 0;
    }

    return required_fuel_mass + get_required_full_fuel_for_mass(required_fuel_mass);
}

/// Compute the total required fuel mass for the rocket
fn part_1() -> anyhow::Result<()> {
    let module_masses = read_input_ints_from_disk("data/input.txt")?;
    let fuel_masses = module_masses.into_iter().map(get_required_fuel_for_mass);
    println!("Part 1:\n-------");
    println!("Required fuel mass: {}\n", fuel_masses.sum::<i64>());
    Ok(())
}

/// Compute the total required fuel mass for the rocket, but this time accounting
/// for the required fuel to carry the required fuel (recursive!)
fn part_2() -> anyhow::Result<()> {
    let module_masses = read_input_ints_from_disk("data/input.txt")?;
    let fuel_masses = module_masses
        .into_iter()
        .map(get_required_full_fuel_for_mass);
    println!("Part 2:\n-------");
    println!("Required fuel mass: {}\n", fuel_masses.sum::<i64>());
    Ok(())
}

/// Main runner for day 01
fn main() -> anyhow::Result<()> {
    part_1()?;
    part_2()?;
    Ok(())
}
