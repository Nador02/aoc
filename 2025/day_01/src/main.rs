use anyhow::{Context, anyhow};
use std::{
    fs::File,
    io::{BufRead, BufReader},
};

/// Read in rotations
fn read_rotations_from_disk(file_path: &str) -> anyhow::Result<Vec<i64>> {
    let input = File::open(file_path)?;
    let buffered = BufReader::new(input);
    buffered
        .lines()
        .map(|line| {
            let line = line.context("failed to grab line from input file")?;
            let direction = line
                .chars()
                .next()
                .ok_or(anyhow!("failed to extract direction from line: \"{line}\""))?;
            let distance = line[1..].parse::<i64>()?;
            match direction {
                'L' => Ok(-distance),
                'R' => Ok(distance),
                bad_direction => Err(anyhow!("unsupported direction: \"{bad_direction}\"")),
            }
        })
        .collect()
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    // Read in the rotations from out inputs
    let rotations = read_rotations_from_disk("data/input.txt")?;

    // Now iterate through each tracking our position and counting how many times
    // we land on a position of zero
    const INITIAL_POSITION: i64 = 50;
    let (_, num_times_at_zero) =
        rotations
            .into_iter()
            .fold((INITIAL_POSITION, 0), |acc, rotation| {
                let new_position_raw = acc.0 + rotation;

                let new_position = if new_position_raw >= 0 || new_position_raw % 100 == 0 {
                    // Positive (or cleanly divisible by 100) raw position means we can just modulo
                    //
                    // NOTE: we need to do the cleanly divisible by 100 here cause otherwise if
                    // we have like -200 it will yield 100, which is not a valid position, it should be 0!
                    new_position_raw % 100
                } else {
                    // Negative raw position means we need to add 100 cause
                    // we are effectively counting backwards
                    100 + (new_position_raw % 100)
                };

                (
                    new_position,
                    // If we are on 0 for our new position, increment the counter
                    acc.1 + if new_position == 0 { 1 } else { 0 },
                )
            });

    // Output our result
    println!(
        "Part 1: After going through all the rotations, we landed on zero: {num_times_at_zero} times!"
    );
    Ok(())
}

/// Part 2
fn part_2() -> anyhow::Result<()> {
    // Read in the rotations from out inputs
    let rotations = read_rotations_from_disk("data/input.txt")?;

    // Now iterate through each tracking our position and counting how many times
    // we pass or land on zero
    const INITIAL_POSITION: i64 = 50;
    let (_, num_times_passed_and_on_zero) =
        rotations
            .into_iter()
            .fold((INITIAL_POSITION, 0), |acc, rotation| {
                let new_position_raw = acc.0 + rotation;

                let new_position = if new_position_raw >= 0 || new_position_raw % 100 == 0 {
                    // Positive (or cleanly divisible by 100) raw position means we can just modulo
                    //
                    // NOTE: we need to do the cleanly divisible by 100 here cause otherwise if
                    // we have like -200 it will yield 100, which is not a valid position, it should be 0!
                    new_position_raw % 100
                } else {
                    // Negative raw position means we need to add 100 cause
                    // we are effectively counting backwards
                    100 + (new_position_raw % 100)
                };

                // Count the # of times we passed or landed on 0 in this rotation
                let new_num_times_on_and_past_zero = acc.1
                    // If our raw position before truncating is negative, we must have 
                    // passed zero once UNLESS we started on zero (so most likely +1)
                    + (new_position_raw < 0 && acc.0 != 0) as i64
                    // If our number is greater than 100 we are doing a full rotation so add that in floored
                    // (+ N rotations)
                    + (new_position_raw / 100).abs()
                    // And if we end on 0 exactly (landing on it) count that as +1
                    + (new_position_raw == 0) as i64;

                (new_position, new_num_times_on_and_past_zero)
            });

    // Output our result
    println!(
        "Part 2: After going through all the rotations, we landed and passed zero: {num_times_passed_and_on_zero} times!"
    );
    Ok(())
}

/// Main runner for day 01
fn main() -> anyhow::Result<()> {
    part_1()?;
    part_2()?;
    Ok(())
}
