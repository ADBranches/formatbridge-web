# CSE 212 - Week 03 Code Assignment Guide
## Sets and Maps Project Implementation Roadmap

---

## 1. Project Location

You are working in the existing course template repository:

```bash
cse212-ww-student-template/week03/code
```

This project **does use the provided course template**. Do not create a new project. Work inside the existing `week03/code` folder.

---

## 2. Assignment Goal

The Week 03 assignment focuses on **Sets and Maps/Dictionaries**.

You have five problems:

1. `FindPairs` - use sets
2. `SummarizeDegrees` - use dictionary and file reading
3. `IsAnagram` - use dictionary character counts
4. `Maze` - use dictionary-backed navigation
5. `EarthquakeDailySummary` - deserialize JSON into objects

You need at least **four of the five problems** completed for full credit. Completing all five may earn extra credit.

---

## 3. Files That Need Adjustment

### Must Modify

```bash
SetsAndMaps.cs
Maze.cs
FeatureCollection.cs
```

### Do Not Modify

```bash
SetsAndMaps_Tests.cs
code.csproj
census.txt
```

`SetsAndMaps_Tests.cs` is the grading/test file. Use it for understanding expected behavior, but do not edit it.

---

## 4. Development Cycle

Follow this cycle for each problem:

```bash
cd week03/code
dotnet test code.csproj
# edit one function
dotnet test code.csproj
# fix errors
dotnet test code.csproj
```

Recommended order:

1. Problem 1 - `FindPairs`
2. Problem 3 - `IsAnagram`
3. Problem 4 - `Maze`
4. Problem 2 - `SummarizeDegrees`
5. Problem 5 - `EarthquakeDailySummary`

---

# Problem 1 - FindPairs

## File to modify

```bash
SetsAndMaps.cs
```

## Method

```csharp
public static string[] FindPairs(string[] words)
```

## Requirement

Find two-character words whose reverse also exists.

Example:

```text
["am", "at", "ma", "if", "fi"]
```

Expected pairs:

```text
"ma & am"
"fi & if"
```

The tests canonicalize ordering, so `"am & ma"` and `"ma & am"` are treated as equivalent.

## Implementation Plan

Use:

```csharp
HashSet<string>
```

Steps:

1. Put all words into a `HashSet<string>`.
2. Create a result list.
3. Create another set to track words already paired.
4. For each word:
   - Reverse the two characters.
   - Skip if the word is the same as its reverse, such as `"aa"`.
   - Check if the reversed word exists.
   - Check that neither word has already been used.
   - Add the pair to the result list.
5. Return `result.ToArray()`.

## Performance Requirement

Must be **O(n)**.

Avoid nested loops.

---

# Problem 2 - SummarizeDegrees

## File to modify

```bash
SetsAndMaps.cs
```

## Method

```csharp
public static Dictionary<string, int> SummarizeDegrees(string filename)
```

## Requirement

Read `census.txt` and count the number of people with each degree.

The file has:

- No header row
- Degree information in the 4th column

In C#, the 4th column is index `3`.

## Implementation Plan

Inside the existing loop:

```csharp
foreach (var line in File.ReadLines(filename))
```

Do this:

1. Split the line by comma.
2. Get `fields[3]`.
3. Trim whitespace.
4. If degree already exists in the dictionary, increment it.
5. Otherwise, add it with value `1`.

## Important Expected Counts

The test expects results such as:

```text
Bachelors: 5355
HS-grad: 10501
Masters: 1723
Doctorate: 413
```

If these do not match, check that you used `fields[3]` and did not skip any line.

---

# Problem 3 - IsAnagram

## File to modify

```bash
SetsAndMaps.cs
```

## Method

```csharp
public static bool IsAnagram(string word1, string word2)
```

## Requirement

Return `true` if both inputs contain the same characters with the same frequencies.

Rules:

- Ignore spaces
- Ignore case
- Must use a dictionary

Examples:

```text
CAT / ACT -> true
DOG / GOOD -> false
A Decimal Point / Im a Dot in Place -> true
```

## Implementation Plan

Use:

```csharp
Dictionary<char, int>
```

Steps:

1. Create a dictionary for character counts.
2. Loop through `word1`:
   - Ignore spaces.
   - Convert characters to lowercase.
   - Increment character count.
3. Loop through `word2`:
   - Ignore spaces.
   - Convert characters to lowercase.
   - If character does not exist, return `false`.
   - Decrement character count.
4. At the end, every value in the dictionary should be `0`.
5. If all counts are zero, return `true`; otherwise, return `false`.

## Performance Requirement

Must be **O(n)**.

Avoid sorting because sorting is usually **O(n log n)**.

---

# Problem 4 - Maze

## File to modify

```bash
Maze.cs
```

## Methods

```csharp
public void MoveLeft()
public void MoveRight()
public void MoveUp()
public void MoveDown()
```

## Maze Structure

The maze map is:

```csharp
Dictionary<ValueTuple<int, int>, bool[]> _mazeMap
```

Each coordinate maps to movement permissions:

```text
(x, y) : [left, right, up, down]
```

Direction indexes:

```text
left  = 0
right = 1
up    = 2
down  = 3
```

## Current Position

The maze starts at:

```csharp
_currX = 1;
_currY = 1;
```

## Required Error Message

If movement is blocked, throw exactly:

```csharp
throw new InvalidOperationException("Can't go that way!");
```

The message must match exactly.

## Implementation Plan

For every move:

1. Get current movement options:

```csharp
var moves = _mazeMap[(_currX, _currY)];
```

2. Check the correct direction index.
3. If blocked, throw `InvalidOperationException`.
4. If allowed, update `_currX` or `_currY`.

Movement updates:

```text
MoveLeft  -> _currX--
MoveRight -> _currX++
MoveUp    -> _currY--
MoveDown  -> _currY++
```

Note: The test sequence confirms that `MoveDown()` increases `y` in this project.

---

# Problem 5 - EarthquakeDailySummary

## Files to modify

```bash
FeatureCollection.cs
SetsAndMaps.cs
```

## Method

```csharp
public static string[] EarthquakeDailySummary()
```

## Requirement

Read USGS earthquake JSON and return strings formatted like:

```text
Place - Mag Magnitude
```

Example:

```text
1km NE of Pahala, Hawaii - Mag 2.36
```

## Step 1 - Define JSON Classes

In `FeatureCollection.cs`, define classes matching the JSON structure.

Required model structure:

```text
FeatureCollection
  -> Features
      -> Feature
          -> Properties
              -> Place
              -> Mag
```

Suggested properties:

```csharp
public class FeatureCollection
{
    public List<Feature> Features { get; set; } = new();
}

public class Feature
{
    public Properties Properties { get; set; } = new();
}

public class Properties
{
    public string Place { get; set; } = "";
    public double? Mag { get; set; }
}
```

## Step 2 - Build Results

In `SetsAndMaps.cs`, after deserialization:

1. Create `List<string>`.
2. Loop through `featureCollection.Features`.
3. Read:
   - `feature.Properties.Place`
   - `feature.Properties.Mag`
4. Add formatted string:

```csharp
$"{place} - Mag {mag}"
```

5. Return `result.ToArray()`.

## Defensive Checks

Since live JSON can occasionally contain null values, it is safer to check:

- `featureCollection != null`
- `featureCollection.Features != null`
- `feature.Properties != null`

---

# Final Testing

Run:

```bash
dotnet test code.csproj
```

If tests fail, use detailed output:

```bash
dotnet test code.csproj --logger "console;verbosity=detailed"
```

---

# Git Submission

After all changes are done:

```bash
git status
git add week03/code/SetsAndMaps.cs week03/code/Maze.cs week03/code/FeatureCollection.cs
git commit -m "Complete week03 sets and maps assignment"
git push
```

Then submit your GitHub repository link to Canvas.

---

# Final Checklist

- [ ] `FindPairs` implemented using `HashSet`
- [ ] `SummarizeDegrees` implemented using `Dictionary<string, int>`
- [ ] `IsAnagram` implemented using `Dictionary<char, int>`
- [ ] `Maze` movement methods implemented
- [ ] `FeatureCollection.cs` JSON model classes added
- [ ] `EarthquakeDailySummary` returns formatted strings
- [ ] `dotnet test code.csproj` runs successfully
- [ ] Changes committed
- [ ] Changes pushed to GitHub

---

# Notes

Do not modify:

```bash
SetsAndMaps_Tests.cs
```

The tests define expected behavior. Your job is to adjust only the implementation files.
