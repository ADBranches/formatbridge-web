# CSE 212 Week 04 Code: Linked Lists — Exclusive Development Timeline & Patching Guide

## Project Location

Work inside this existing course template folder:

```bash
/home/trovas/Downloads/projects/byupw/block3_2026/CSE212/cse212-ww-student-template/week04/code
```

Expected files:

```bash
code.csproj
LinkedList.cs
LinkedList_Tests.cs
Node.cs
```

This assignment uses the provided `week04/code` folder. Do not create a new project, and do not rename/delete files, classes, or method signatures.

---

## Assignment Objective

The assignment is **W04 Code: Linked Lists**. Its purpose is to demonstrate your ability to use linked lists.

You need to implement five linked-list operations:

1. `InsertTail`
2. `RemoveTail`
3. `Remove`
4. `Replace`
5. `Reverse`

The course instructions state that full credit requires successfully completing **any four of the five problems**, while completing all five may qualify for extra credit.

---

## Rubric Targets

| Requirement | Points |
|---|---:|
| Base solution: at least one solved problem | 60 |
| Problem 1: Insert Tail | 10 |
| Problem 2: Remove Tail | 10 |
| Problem 3: Remove | 10 |
| Problem 4: Replace | 10 |
| Problem 5: Reversed Iterator | 10 |

Total possible rubric points shown: **110**.

Goal: implement and pass tests for **all five** to maximize the score.

---

## Files To Modify

### Modify

```bash
LinkedList.cs
```

Most or all code changes should happen here.

### Usually Do Not Modify

```bash
Node.cs
code.csproj
LinkedList_Tests.cs
```

Use `LinkedList_Tests.cs` only for understanding expected behavior. Do not edit test files unless explicitly instructed by the course.

---

## Development Rule

Patch one method at a time, then run only that method's tests.

Preferred loop:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CSE212/cse212-ww-student-template/week04/code

dotnet test code.csproj --filter InsertTail
# patch InsertTail
# retest InsertTail

dotnet test code.csproj --filter RemoveTail
# patch RemoveTail
# retest RemoveTail
```

Do not run the full suite until the individual method tests are passing.

---

## Stage 0 — Inspect The Starting Code

Run:

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/CSE212/cse212-ww-student-template/week04/code

sed -n '1,260p' LinkedList.cs
sed -n '1,220p' Node.cs
sed -n '1,320p' LinkedList_Tests.cs
```

Also check method names in tests:

```bash
grep -n "TestMethod\|public void\|InsertTail\|RemoveTail\|Remove\|Replace\|Reverse" LinkedList_Tests.cs
```

Run baseline tests:

```bash
dotnet test code.csproj
```

Expected: some tests fail because methods are not implemented yet.

---

## Stage 1 — Problem 1: InsertTail

### File

```bash
LinkedList.cs
```

### Requirement

Implement `InsertTail` to add a new `Node` at the end of the linked list.

### Concepts

A doubly linked list usually tracks:

```csharp
_head
_tail
```

Each node may have:

```csharp
Data
Next
Prev
```

Confirm exact property names in `Node.cs` before patching.

### Expected Logic

If the list is empty:

```text
head = new node
tail = new node
```

If the list is not empty:

```text
newNode.Prev = tail
tail.Next = newNode
tail = newNode
```

### Test Only InsertTail

```bash
dotnet test code.csproj --filter InsertTail
```

Proceed only after InsertTail passes.

---

## Stage 2 — Problem 2: RemoveTail

### File

```bash
LinkedList.cs
```

### Requirement

Implement `RemoveTail` to remove the last node.

### Expected Logic

If the list is empty:

```text
throw or do nothing depending on existing RemoveHead behavior/tests
```

Use existing `RemoveHead` behavior as the pattern.

If the list has one node:

```text
head = null
tail = null
```

If the list has multiple nodes:

```text
tail = tail.Prev
tail.Next = null
```

### Test Only RemoveTail

```bash
dotnet test code.csproj --filter RemoveTail
```

Proceed only after RemoveTail passes.

---

## Stage 3 — Problem 3: Remove

### File

```bash
LinkedList.cs
```

### Requirement

Implement `Remove` to search from the head and remove the **first node** whose value matches the target value.

Important: stop after removing the first match.

### Expected Logic

1. Start at `_head`.
2. Walk node by node.
3. If matching node is found:
   - If node is the head, reuse `RemoveHead()` if appropriate.
   - Else if node is the tail, reuse `RemoveTail()` if appropriate.
   - Else bypass node:

```text
current.Prev.Next = current.Next
current.Next.Prev = current.Prev
```

4. Stop immediately after removing one node.

### Edge Cases

- Empty list
- Target is at head
- Target is at tail
- Target is in the middle
- Target appears multiple times: only first match removed
- Target does not exist: list unchanged

### Test Only Remove

```bash
dotnet test code.csproj --filter Remove
```

If the filter also catches `RemoveTail`, use the exact test names from `grep` output.

---

## Stage 4 — Problem 4: Replace

### File

```bash
LinkedList.cs
```

### Requirement

Implement `Replace` to replace **all nodes** whose value equals `oldValue` with `newValue`.

Unlike `Remove`, this must continue through the whole list.

### Expected Logic

1. Start at `_head`.
2. While current node is not null:
   - If current value equals `oldValue`, set it to `newValue`.
   - Move to next node.
3. Do not stop after the first replacement.

### Edge Cases

- Empty list
- No matching values
- One matching value
- Multiple matching values
- All values matching

### Test Only Replace

```bash
dotnet test code.csproj --filter Replace
```

Proceed only after Replace passes.

---

## Stage 5 — Problem 5: Reverse Iterator

### File

```bash
LinkedList.cs
```

### Requirement

Implement `Reverse` so this works:

```csharp
foreach (var item in myLinkedList.Reverse())
{
    Debug.WriteLine(item);
}
```

### Expected Logic

Pattern after existing `GetEnumerator`, but start from tail instead of head.

Forward iterator usually does:

```text
current = head
while current != null:
    yield return current.Data
    current = current.Next
```

Reverse iterator should do:

```text
current = tail
while current != null:
    yield return current.Data
    current = current.Prev
```

### Test Only Reverse

```bash
dotnet test code.csproj --filter Reverse
```

Proceed only after Reverse passes.

---

## Stage 6 — Run Full Test Suite

After all individual tests pass:

```bash
dotnet test code.csproj
```

Target result:

```text
failed: 0
succeeded: all
Build succeeded
```

---

## Stage 7 — Clean Up Before Commit

Check for unfinished TODOs:

```bash
grep -n "TODO\|FILL IN CODE\|return \[\]\|return false" LinkedList.cs Node.cs
```

Check Git status:

```bash
git status
```

Only expected modified file is usually:

```bash
week04/code/LinkedList.cs
```

If backup files exist, remove them:

```bash
rm -f *.bak
```

---

## Stage 8 — Commit And Push

From inside `week04/code`, run:

```bash
git add LinkedList.cs

git commit -m "Complete week04 linked lists assignment"

git push
```

Then confirm:

```bash
git status
```

Expected:

```text
nothing to commit, working tree clean
```

---

## Stage 9 — Submit To Canvas

Submit your GitHub repository link, not a ZIP file and not a screenshot.

Example:

```text
https://github.com/YOUR-USERNAME/cse212-ww-student-template
```

Use:

```bash
git remote -v
```

to identify the repo URL.

---

## Exclusive Patching Plan Summary

Follow exactly this timeline:

```text
1. Inspect LinkedList.cs, Node.cs, LinkedList_Tests.cs
2. Run baseline tests
3. Patch InsertTail
4. Test InsertTail only
5. Patch RemoveTail
6. Test RemoveTail only
7. Patch Remove
8. Test Remove only
9. Patch Replace
10. Test Replace only
11. Patch Reverse
12. Test Reverse only
13. Run full dotnet test
14. Clean TODO/backups
15. git add LinkedList.cs
16. git commit
17. git push
18. Submit GitHub URL to Canvas
```

---

## Important Notes

- Do not rename files.
- Do not rename classes.
- Do not change method signatures.
- Do not edit files marked `DO NOT MODIFY THIS FILE`.
- Use `Debug.WriteLine()` instead of `Console.WriteLine()` if debugging tests.
- Use existing implemented methods such as `InsertHead` and `RemoveHead` as patterns.
- Always run a specific test before moving to the next method.

---

## Ready For The Next Step

After creating this guide, the next practical step is to paste the contents of:

```bash
sed -n '1,260p' LinkedList.cs
sed -n '1,220p' Node.cs
sed -n '1,320p' LinkedList_Tests.cs
```

Then patching can begin safely with exact terminal commands.
