use std::{
    collections::HashSet, fs::File, io::{BufRead, BufReader}, process::id
};

struct IngredientIDs(HashSet<usize>);

impl IngredientIDs {
    pub fn new() -> Self {
        Self(HashSet::new())
    }

    pub fn insert(&mut self, ingredient_id: usize) {
        self.0.insert(ingredient_id);
    }
}

/// Read in input
fn get_fresh_and_available_ingredient_ids_from_disk(file_path: &str) -> anyhow::Result<(IngredientIDs, IngredientIDs)> {
    let input = File::open(file_path)?;
    let buffered = BufReader::new(input);

    let mut fresh_ingredient_ids = IngredientIDs::new();
    let mut avaialable_ingredient_ids = IngredientIDs::new();
    let mut found_input_split = false;

    for line in buffered.lines() {
        // If we passed our input split, starting adding to available
        // ingredient IDs
        if found_input_split {
            avaialable_ingredient_ids.insert(line?.parse::<usize>()?);
        } else {
            // Otherwise, continue adding ranges to our fresh ingredient IDs
            fresh_ingredient_ids.insert(line?.parse::<usize>()?);
        }
    }

    Ok((fresh_ingredient_ids, avaialable_ingredient_ids))
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    let (fresh_ingredient_ids, avaialble_ingredient_ids) = get_fresh_and_available_ingredient_ids_from_disk("data/input.txt")?;
    todo!("Part 1!");
}

/// Part 2
#[allow(dead_code)]
fn part_2() -> anyhow::Result<()> {
    todo!("Part 2!");
}

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    part_2()?;
    Ok(())
}
