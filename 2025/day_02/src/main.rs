use anyhow::{Context, anyhow};
use std::{
    fs::File,
    io::{BufRead, BufReader},
    ops::RangeInclusive,
};

/// Read in input product ID ranges
fn read_product_id_ranges(file_path: &str) -> anyhow::Result<Vec<RangeInclusive<i64>>> {
    let input = File::open(file_path)?;
    let buffered = BufReader::new(input);

    let input_str = buffered
        .lines()
        .next()
        .transpose()?
        .ok_or(anyhow!("input product ID file is empty"))?;

    let range_strings: Vec<&str> = input_str.split(",").collect();

    range_strings
        .into_iter()
        .map(|range_str| {
            // Split along the dash for each of our ranges
            let range_vec: Vec<&str> = range_str.split("-").collect();

            // If for some reason this gives us a weird sized vector, just error out early
            if range_vec.len() != 2 {
                return Err(anyhow!(
                    "range string has more than two parts? \"{range_str}\""
                ));
            }

            // Otherwise parse each string as an int and create our inclusive range
            let start = range_vec[0]
                .to_owned()
                .parse::<i64>()
                .with_context(|| format!("failed to parse start of range: \"{}\"", range_vec[0]))?;
            let end = range_vec[1]
                .to_owned()
                .parse::<i64>()
                .with_context(|| format!("failed to parse end of range: \"{}\"", range_vec[1]))?;

            Ok(start..=end)
        })
        .collect()
}

/// Check if a number is repeating twice
///
/// # Examples
/// `123123` -> `true`
/// `99` -> `true`
/// `12345` -> `false`
/// `123123123` -> `false`
///
/// # Note
/// This two pointer solution worked but is somehow slower than my brute force
/// slice comparison approach? Not really sure why, can look into that later
/// cause its interesting I must have done some super bad performance Rust thing!
#[allow(dead_code)]
fn is_num_repeating_twice_two_pointers(num: i64) -> anyhow::Result<bool> {
    // This is dangerous but we can do it safely because
    // we are definitely only ASCII as these are ints -> strings
    let num_str = num.to_string();
    let num_chars = num_str.chars();

    // If the number has an odd length it cannot be repeating!
    if num_str.len() % 2 != 0 {
        return Ok(false);
    }

    // Otherwise march forward two pointers to check
    let mut back_iter = num_chars.clone();
    let mut front_iter = num_chars.skip(num_str.len() / 2).peekable();
    while front_iter.peek().is_some() {
        let back_curr = back_iter.next().ok_or(anyhow!(
            "back pointer out of bounds somehow for input num: \"{num}\""
        ))?;
        let front_curr = front_iter.next().ok_or(anyhow!(
            "front pointer out of bounds somehow for input num: \"{num}\""
        ))?;

        if back_curr != front_curr {
            return Ok(false);
        }
    }

    Ok(true)
}

/// Check if a number is repeating any N times
fn is_num_repeating_n_times(num: i64, num_repetitions: usize) -> anyhow::Result<bool> {
    // This is dangerous but we can do it safely because
    // we are definitely only ASCII as these are ints -> strings
    let num_str = num.to_string();

    // If the number is not evenly divisible by the number of repetitions we
    // can just skip over it before doing anything else
    if num_str.len() % num_repetitions != 0 || num_str.len() < num_repetitions {
        return Ok(false);
    }

    // Otherwise compare slices
    let pattern_length = num_str.len() / num_repetitions;
    let front_pattern = &num_str[..pattern_length];
    for repeated_pattern_front_index in 1..num_repetitions {
        let curr_pattern = &num_str[repeated_pattern_front_index * pattern_length
            ..repeated_pattern_front_index * pattern_length + pattern_length];
        let patterns_match = front_pattern
            .chars()
            .zip(curr_pattern.chars())
            .all(|(expected_char, found_char)| expected_char == found_char);

        if !patterns_match {
            return Ok(false);
        }
    }

    Ok(true)
}

/// Check if a number is repeating AT ALL (any valid N times)
fn is_num_repeating(num: i64) -> anyhow::Result<bool> {
    for num_repetitions in 2..=num.to_string().len() {
        if is_num_repeating_n_times(num, num_repetitions)? {
            return Ok(true);
        }
    }

    Ok(false)
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    // Load in our product ID ranges
    let ranges = read_product_id_ranges("data/input.txt")?;

    // Sum together all the product IDs that are non-repeating in our ranges
    let mut invalid_id_sum = 0;
    for range in ranges {
        for product_id in range {
            let is_product_id_invalid =
                is_num_repeating_n_times(product_id, 2).with_context(|| {
                    format!("failed to check if product ID: {product_id} is repeating")
                })?;

            if is_product_id_invalid {
                invalid_id_sum += product_id;
            }
        }
    }

    // Output the result
    println!(
        "Part 1: Adding up all the invalid product IDs (with double repetition) yields: {}",
        invalid_id_sum
    );

    Ok(())
}

/// Part 2
fn part_2() -> anyhow::Result<()> {
    // Load in our product ID ranges
    let ranges = read_product_id_ranges("data/input.txt")?;

    // Sum together all the product IDs that are non-repeating in our ranges
    let mut invalid_id_sum = 0;
    for range in ranges {
        for product_id in range {
            let is_product_id_invalid = is_num_repeating(product_id).with_context(|| {
                format!("failed to check if product ID: {product_id} is repeating")
            })?;

            if is_product_id_invalid {
                invalid_id_sum += product_id;
            }
        }
    }

    // Output the result
    println!(
        "Part 2: Adding up all the invalid product IDs (with ANY repetition) yields: {}",
        invalid_id_sum
    );

    Ok(())
}

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    part_2()?;
    Ok(())
}
