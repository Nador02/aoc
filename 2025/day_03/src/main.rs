use std::{
    fs::File,
    io::{BufRead, BufReader},
};

struct BatteryBank(String);

impl BatteryBank {
    /// Max joltage including 2 batteries in the bank
    fn get_max_joltage(&self) -> anyhow::Result<u32> {
        let batteries = self.0.chars();
        let mut max_joltage = (0, 0);
        for (idx, battery) in batteries.enumerate() {
            // Cast our battery char as a digit
            let battery_value = battery
                .to_digit(10)
                .unwrap_or_else(|| panic!("failed to cast battery: {battery} as digit"));

            // If our battery is greater than our value in the tens place
            // replace it and set the ones spot to zero
            //
            // NOTE: only do this if this is NOT the last number, otherwise it won't work
            // as there is no digit to fill into the ones place
            if battery_value > max_joltage.0 && idx != self.0.len() - 1 {
                max_joltage = (battery_value, 0)
            // Otherwise, if this is greater than our current max one digit, replace only that
            } else if battery_value > max_joltage.1 {
                max_joltage.1 = battery_value
            }
        }

        Ok(max_joltage.0 * 10 + max_joltage.1)
    }

    /// Max joltage including 12 batteries (safety override) in the bank
    fn get_max_joltage_w_safety_override(&self) -> anyhow::Result<u64> {
        // Unpack our batteries into chars and start with our "ideal" max
        // joltage batteries as the first 12
        let batteries = self.0.chars();
        let mut ideal_batteries: Vec<char> = batteries.clone().take(12).collect();

        // March through and check if it makes sense to sub in a new battery each
        // time by checking from the front to the back on if dropping a battery out
        // increases total value: `(curr battery < curr battery + 1)`
        for new_battery in batteries.skip(12) {
            for (idx, ideal_battery) in ideal_batteries.iter().enumerate() {
                // Edge case for the end when we compare with the new battery
                let compare_battery = if idx < ideal_batteries.len() - 1 {
                    ideal_batteries[idx + 1]
                } else {
                    new_battery
                };

                // Extract values of each
                let ideal_battery_value = ideal_battery.to_digit(10).unwrap();
                let compare_battery_value = compare_battery.to_digit(10).unwrap();

                // Compare and if it makes sense to swap out, pull in the new
                // battery and pop off the less valuable one
                if compare_battery_value > ideal_battery_value {
                    ideal_batteries.remove(idx);
                    ideal_batteries.push(new_battery);
                    break;
                }
            }
        }

        // Go through and sum our batteries to get the max safety override joltage
        let max_unsafe_joltage =
            ideal_batteries
                .into_iter()
                .enumerate()
                .fold(0, |acc, (idx, battery)| {
                    let battery_value = battery.to_digit(10).unwrap();
                    acc + (battery_value as u64) * (10u64).pow((11 - idx) as u32)
                });

        Ok(max_unsafe_joltage)
    }
}

/// Read in battery banks from disk
fn read_battery_banks_from_disk(file_path: &str) -> anyhow::Result<Vec<BatteryBank>> {
    let input = File::open(file_path)?;
    let buffered = BufReader::new(input);
    buffered
        .lines()
        .map(|line| Ok(BatteryBank(line?)))
        .collect()
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    // Load in battery banks
    let battery_banks = read_battery_banks_from_disk("data/input.txt")?;

    // Compute the max joltage for each bank and sum together
    let total_output_joltage = battery_banks
        .into_iter()
        .try_fold(0, |acc, battery_bank| -> anyhow::Result<u32> {
            Ok(acc + battery_bank.get_max_joltage()?)
        })?;

    // Output result
    println!("[Part 1] Total Output Joltage: {total_output_joltage} jolts");
    Ok(())
}

/// Part 2
fn part_2() -> anyhow::Result<()> {
    // Load in battery banks
    let battery_banks = read_battery_banks_from_disk("data/input.txt")?;

    // Compute the max safety override joltage for each bank and sum together
    let total_output_joltage =
        battery_banks
            .into_iter()
            .try_fold(0, |acc, battery_bank| -> anyhow::Result<u64> {
                Ok(acc + battery_bank.get_max_joltage_w_safety_override()?)
            })?;

    // Output result
    println!("[Part 2] Total Output Joltage (w/ Safety Override): {total_output_joltage} jolts");
    Ok(())
}

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    part_2()?;
    Ok(())
}
