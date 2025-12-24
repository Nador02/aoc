use anyhow::anyhow;
use itertools::Itertools;
use std::{
    collections::HashSet,
    fmt::Display,
    fs::File,
    io::{BufRead, BufReader},
    ops::Add,
};

#[derive(PartialEq, Eq, Hash, Clone, Copy)]
struct Point {
    i: i32,
    j: i32,
}

impl Point {
    pub fn new(i: i32, j: i32) -> Self {
        Self { i, j }
    }

    pub fn get_neighboring_points(&self) -> HashSet<Point> {
        HashSet::from([
            *self + Point::new(-1, 0),
            *self + Point::new(-1, 1),
            *self + Point::new(0, 1),
            *self + Point::new(1, 1),
            *self + Point::new(1, 0),
            *self + Point::new(1, -1),
            *self + Point::new(0, -1),
            *self + Point::new(-1, -1),
        ])
    }
}

impl Add for Point {
    type Output = Point;

    fn add(self, rhs: Self) -> Self::Output {
        Self {
            i: self.i + rhs.i,
            j: self.j + rhs.j,
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
        let rows: Vec<String> = buffered.lines().try_collect()?;
        let width = rows[0].len();
        let height = rows.len();

        Ok(Self {
            grid: rows
                .into_iter()
                .flat_map(|row| row.chars().collect::<Vec<char>>())
                .collect(),
            width,
            height,
        })
    }

    pub fn point_to_index(&self, point: Point) -> usize {
        self.width * (point.i as usize) + (point.j as usize)
    }

    pub fn get_paper_roll(&self, point: Point) -> char {
        self.grid[self.point_to_index(point)]
    }

    pub fn into_removed_rolls_at_points(mut self, points: HashSet<Point>) -> anyhow::Result<Self> {
        for point in points {
            if self.get_paper_roll(point) != '@' {
                return Err(anyhow!(
                    "didn't find paper roll at point: {point} found \'{}\'",
                    self.get_paper_roll(point)
                ));
            }

            let idx = self.point_to_index(point);
            self.grid[idx] = '.';
        }

        Ok(self)
    }

    pub fn get_all_paper_roll_points(&self) -> HashSet<Point> {
        let mut paper_roll_points = HashSet::new();
        for i in 0..self.height {
            for j in 0..self.width {
                let i = i as i32;
                let j = j as i32;
                if self.get_paper_roll(Point::new(i, j)) == '@' {
                    paper_roll_points.insert(Point::new(i, j));
                }
            }
        }

        paper_roll_points
    }
}

/// Part 1
fn part_1() -> anyhow::Result<()> {
    let paper_rolls_diagram = PaperRollsDiagram::from_disk("data/input.txt")?;

    let paper_roll_points = paper_rolls_diagram.get_all_paper_roll_points();
    let mut num_forklift_accessible_rolls = 0;
    for point in &paper_roll_points {
        let neighboring_points = point.get_neighboring_points();
        let neighboring_paper_rolls: HashSet<Point> = neighboring_points
            .intersection(&paper_roll_points)
            .copied()
            .collect();

        if neighboring_paper_rolls.len() < 4 {
            num_forklift_accessible_rolls += 1;
        }
    }

    println!("[Part 1] Number of Forklift Accessible Rolls: {num_forklift_accessible_rolls}");
    Ok(())
}

/// Part 2
fn part_2() -> anyhow::Result<()> {
    let mut paper_rolls_diagram = PaperRollsDiagram::from_disk("data/input.txt")?;

    let mut num_forklift_accessible_rolls = 0;
    loop {
        let mut removable_rolls = HashSet::new();
        let paper_roll_points = paper_rolls_diagram.get_all_paper_roll_points();

        for point in &paper_roll_points {
            let neighboring_points = point.get_neighboring_points();
            let neighboring_paper_rolls: HashSet<Point> = neighboring_points
                .intersection(&paper_roll_points)
                .copied()
                .collect();

            if neighboring_paper_rolls.len() < 4 {
                num_forklift_accessible_rolls += 1;
                removable_rolls.insert(*point);
            }
        }

        if removable_rolls.is_empty() {
            break;
        }
        paper_rolls_diagram = paper_rolls_diagram.into_removed_rolls_at_points(removable_rolls)?;
    }

    println!("[Part 2] Total Number of Forklift Accessible Rolls: {num_forklift_accessible_rolls}");
    Ok(())
}

/// Main runner template
fn main() -> anyhow::Result<()> {
    part_1()?;
    part_2()?;
    Ok(())
}
