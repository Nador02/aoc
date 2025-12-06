use std::{
    fs::File,
    io::{BufRead, BufReader},
};

/// Read in input
/// NOTE: example here is just ints but can be whatever is needed
fn read_input_ints_from_disk(file_path: &str) -> anyhow::Result<Vec<i64>> {
    let input = File::open(file_path)?;
    let buffered = BufReader::new(input);
    buffered
        .lines()
        .map(|line| Ok(line?.parse::<i64>()?))
        .collect()
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    let _input = read_input_ints_from_disk("data/input.txt")?;
    todo!("Part 1!");
}

/// Part 2
fn part_2() -> anyhow::Result<()> {
    let _input = read_input_ints_from_disk("data/input.txt")?;
    todo!("Part 2!");
}

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    part_2()?;
    Ok(())
}
