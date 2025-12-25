use std::{
    collections::HashSet,
    fmt::Display,
    fs::File,
    io::{BufRead, BufReader},
    ops::RangeInclusive,
};

use itertools::Itertools;

struct IngredientIDRanges(Vec<RangeInclusive<usize>>);

struct IngredientIDs(HashSet<usize>);

impl Display for IngredientIDs {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{}]", self.0.iter().join(","))
    }
}

impl Display for IngredientIDRanges {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "[{}]",
            self.0
                .iter()
                .map(|range| format!("({}, {})", range.start(), range.end()))
                .join(",")
        )
    }
}

impl IngredientIDs {
    pub fn new() -> Self {
        Self(HashSet::new())
    }

    pub fn insert(&mut self, ingredient_id: usize) {
        self.0.insert(ingredient_id);
    }
}

impl IngredientIDRanges {
    pub fn new() -> Self {
        Self(Vec::new())
    }

    pub fn push(&mut self, ingredient_id_range: RangeInclusive<usize>) {
        self.0.push(ingredient_id_range)
    }

    pub fn contains(&self, ingredient_id: &usize) -> bool {
        for range in &self.0 {
            if range.contains(ingredient_id) {
                return true;
            }
        }

        false
    }
}

/// Read in input
fn get_fresh_and_available_ingredient_ids_from_disk(
    file_path: &str,
) -> anyhow::Result<(IngredientIDRanges, IngredientIDs)> {
    let input = File::open(file_path)?;
    let buffered = BufReader::new(input);

    let mut fresh_ingredient_ids = IngredientIDRanges::new();
    let mut avaialable_ingredient_ids = IngredientIDs::new();
    let mut found_input_split = false;

    for line in buffered.lines() {
        // If we passed our input split, starting adding to available
        // ingredient IDs
        if found_input_split {
            avaialable_ingredient_ids.insert(line?.parse::<usize>()?);
        } else {
            // Check if this is where we should split
            let line_str = line?;
            if line_str.is_empty() {
                found_input_split = true;
                continue;
            }

            // Otherwise, continue adding ranges to our fresh ingredient IDs
            let (id_range_start, id_range_end) = line_str.split_once("-").unwrap();
            let id_range_start = id_range_start.parse::<usize>()?;
            let id_range_end = id_range_end.parse::<usize>()?;
            fresh_ingredient_ids.push(RangeInclusive::new(id_range_start, id_range_end));
        }
    }

    Ok((fresh_ingredient_ids, avaialable_ingredient_ids))
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    let (fresh_ingredient_ids, available_ingredient_ids) =
        get_fresh_and_available_ingredient_ids_from_disk("data/input.txt")?;
    let num_fresh_ingredients = available_ingredient_ids
        .0
        .iter()
        .filter(|&ingredient_id| fresh_ingredient_ids.contains(ingredient_id))
        .collect::<Vec<&usize>>()
        .len();
    println!("[Part 1]: Number of Fresh Ingredients Available: {num_fresh_ingredients}");
    Ok(())
}

/// Part 2
#[allow(dead_code)]
fn part_2() -> anyhow::Result<()> {
    todo!("Part 2!");
}

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    // part_2()?;
    Ok(())
}
