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
fn is_num_repeating_twice(num: i64) -> anyhow::Result<bool> {
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

/// Part 1
fn part_1() -> anyhow::Result<()> {
    // Load in our product ID ranges
    let ranges = read_product_id_ranges("data/input.txt")?;

    // Sum together all the product IDs that are non-repeating in our ranges
    let mut invalid_id_sum = 0;
    for range in ranges {
        for product_id in range {
            let is_product_id_invalid = is_num_repeating_twice(product_id).with_context(|| {
                format!("failed to check if product ID: {product_id} is repeating")
            })?;

            if is_product_id_invalid {
                invalid_id_sum += product_id;
            }
        }
    }

    // Output the result
    println!(
        "Part 1: Adding up all the invalid product IDs yields: {}",
        invalid_id_sum
    );

    Ok(())
}

// /// Part 2
// fn part_2() -> anyhow::Result<()> {
//     todo!("Part 2!");
// }

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    // part_2()?;
    Ok(())
}
