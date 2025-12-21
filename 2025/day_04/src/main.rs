use itertools::Itertools;
use std::{
    collections::HashSet, fmt::Display, fs::File, io::{BufRead, BufReader}
};

#[derive(PartialEq, Eq, Hash)]
struct Point {
    i: usize,
    j: usize
}

impl Point {
    pub fn new(i: usize, j: usize) -> Self {
        Self {
            i,
            j
        }
    }
}

impl Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Point(i = {}, j = {})", self.i, self.j)
    }
}

struct PaperRollsDiagram {
    grid: Vec<char>,
    width: usize,
    height: usize,
}

impl PaperRollsDiagram {
    /// Load a paper roll diagram from disk
    pub fn from_disk(file_path: &str) -> anyhow::Result<Self> {
        // Load in our file buffer
        let input = File::open(file_path)?;
        let buffered = BufReader::new(input);
        
        // Load in rows and from that determine our 
        let rows: Vec<String> = buffered
            .lines()
            .map(|line| line)
            .try_collect()?;
        let width = rows[0].len();
        let height = rows.len();

        Ok(Self {
            grid: rows
                .into_iter()
                .map(|row| row.chars().collect::<Vec<char>>())
                .flatten()
                .collect(),
            width,
            height
        })
    }

    pub fn get_paper_roll(&self, point: Point) -> char {
        return self.grid[self.width*point.i + point.j]
    }

    pub fn get_all_paper_roll_points(&self) -> HashSet<Point> {
        let mut paper_roll_points = HashSet::new();
        for i in 0..self.height {
            for j in 0..self.width {
                if self.get_paper_roll(Point::new(i,j)) == '@' {
                    paper_roll_points.insert(Point::new(i,j));
                }
            }
        }

        paper_roll_points
    }
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    let paper_rolls_diagram = PaperRollsDiagram::from_disk("data/example.txt")?;
    for point in paper_rolls_diagram.get_all_paper_roll_points() {
        println!("{}", point);
    }
    Ok(())
}

/// Part 2
fn part_2() -> anyhow::Result<()> {
    todo!("Part 2!");
}

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    // part_2()?;
    Ok(())
}
