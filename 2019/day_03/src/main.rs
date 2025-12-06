use anyhow::{Context, anyhow};
use itertools::Itertools;
use std::fs;

const CIRCUIT_ORIGIN_POSITION: CircuitPosition = CircuitPosition { x: 0, y: 0 };

#[derive(Clone, Copy)]
pub struct CircuitPosition {
    x: usize,
    y: usize,
}

pub enum Direction {
    Right,
    Left,
    Down,
    Up,
}

impl TryFrom<char> for Direction {
    type Error = anyhow::Error;

    fn try_from(direction: char) -> Result<Self, Self::Error> {
        Ok(match direction {
            'R' => Self::Right,
            'L' => Self::Left,
            'U' => Self::Up,
            'D' => Self::Down,
            _ => Err(anyhow!(
                "Unsupported direction character: \'{direction}\' found!"
            ))?,
        })
    }
}

pub struct Segment {
    direction: Direction,
    length: usize,
}

impl TryFrom<&str> for Segment {
    type Error = anyhow::Error;

    fn try_from(segment: &str) -> Result<Self, Self::Error> {
        let direction =
            Direction::try_from(segment.chars().next().expect("Empty segment string?"))?;
        Ok(Self {
            direction,
            length: segment[1..].trim().parse().with_context(|| {
                format!(
                    "Failed to parse length from segment string: \"{}\"",
                    segment[1..].to_owned()
                )
            })?,
        })
    }
}

impl Segment {
    pub fn get_points_for_segment(&self, starting_position: CircuitPosition) -> anyhow::Result<Vec<CircuitPosition>> {
        Ok(match self.direction {
            Direction::Right => (starting_position.x..(starting_position.x + self.length)).into_iter().map(|x| CircuitPosition{
                x,
                y: starting_position.y,
            }).collect(),
            Direction::Left => (starting_position.x..(starting_position.x - self.length)).rev().into_iter().map(|x| CircuitPosition{
                x,
                y: starting_position.y,
            }).collect(),
            Direction::Up => (starting_position.y..(starting_position.y + self.length)).into_iter().map(|y| CircuitPosition{
                x: starting_position.x,
                y,
            }).collect(),
            Direction::Down => (starting_position.y..(starting_position.y - self.length)).rev().into_iter().map(|y| CircuitPosition{
                x: starting_position.x,
                y,
            }).collect(),
        })
    }
}

pub struct Wire {
    path: Vec<Segment>,
}

impl Wire {
    pub fn get_points_for_wire_path(&self) -> anyhow::Result<Vec<CircuitPosition>> {
        let mut current_position = CIRCUIT_ORIGIN_POSITION;
        Ok(self.path
            .iter()
            .flat_map(|segment| {
                let segment_points = segment.get_points_for_segment(current_position).unwrap();
                current_position = segment_points.last().copied().expect("Uh no points for this segment?");
                segment_points
            })
            .collect())
    }
}

impl TryFrom<&str> for Wire {
    type Error = anyhow::Error;

    fn try_from(wire_path: &str) -> Result<Self, Self::Error> {
        let segment_strings: Vec<&str> = wire_path.split(",").collect();
        Ok(Self {
            path: segment_strings
                .into_iter()
                .map(|segment_str| Segment::try_from(segment_str))
                .try_collect()?,
        })
    }
}

pub fn read_input(file_path: &str) -> anyhow::Result<(Wire, Wire)> {
    let input_string = fs::read_to_string(file_path)?;
    let wires: Vec<Wire> = input_string
        .split("\n")
        .map(|wire_path_str| Wire::try_from(wire_path_str))
        .try_collect()?;
    Ok(wires
        .into_iter()
        .collect_tuple()
        .expect("Unable to collect tuple from iterator of wires!"))
}

/// Part 1 Stuff
fn part_1() -> anyhow::Result<()> {
    let (wire1, wire2) = read_input("data/input.txt")?;

    Ok(())
}

/// Part 2 Stuff
fn part_2() -> anyhow::Result<()> {
    todo!()
}

/// Main runner for Day 03
fn main() -> anyhow::Result<()> {
    println!("Part 1:\n-------\n");
    part_1()?;
    // println!("\n\nPart 2:\n-------\n");
    // part_2()?;
    Ok(())
}
