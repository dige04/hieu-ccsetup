# Study Skill

Teach, test, and generate exam-ready materials from course content.

## Trigger

`/study [subject] [--mode]`

## Arguments

- `subject`: Folder name in `/Users/hieudinh/Documents/02-Areas/`
- `--mode`: One of `--learn`, `--mcq`, `--code`, `--oral` (optional, prompts if missing)

## Examples

```
/study distributed-systems --learn
/study computer-vision --mcq
/study nlp --code
/study bioinformatics --oral
/study r-programming
```

## Base Paths

- Materials: `/Users/hieudinh/Documents/02-Areas/[subject]/`
- Summaries output: `/Users/hieudinh/Documents/02-Areas/[subject]/summaries/`
- Flashcards output: `/Users/hieudinh/Documents/02-Areas/[subject]/cards/`

---

## Workflow

### Step 1: Load Context

Read all `.md`, `.txt`, `.pdf`, `.ipynb`, `.py`, `.r` files in subject folder recursively.

Build mental map of:
- Topics covered and their sequence
- Terminology and notation used
- Depth level and complexity
- If `past-exam*` files exist, use them to calibrate difficulty and identify high-value topics

Always reference specific source files: "As covered in week3-attention.md..."

### Step 2: Select Mode

If mode not provided, ask:

```
Study mode for [subject]?
- learn  → Guided teaching + summary notes
- mcq    → Multiple choice practice
- code   → Handwritten code recall
- oral   → Professor simulation
```

### Step 3: Execute Selected Mode

---

## MODE: --learn

Guided learning that produces comprehensive exam-ready summary notes.

### Learn Step 1: Scan & Present Structure

```
[subject]/ - X files scanned

Topics found:
1. [Topic name] (source files)
2. [Topic name] (source files)
3. ...

Which topic? [1-N or "all"]:
```

### Learn Step 2: Teach with Structure

For each topic, present:

```markdown
## [Topic Name]

### Why It Matters (Exam Relevance)
- Frequency in past exams
- Typical question format
- Point value patterns

### Core Concepts (Memorize These)
Numbered list of essential concepts, 2-3 lines each max.
Use THEIR terminology from lectures.

### Mental Model
Simple analogy or ASCII diagram to cement understanding.

### Quick Reference Table
| Key comparisons in table format |

### Common Exam Patterns
- Typical question phrasings
- Expected answer structure
- Points allocation hints

### Mnemonics (If Applicable)
Memory aids for complex sequences or lists.

[continue / deeper / questions / save]
```

**User commands:**
- `continue` → Next subtopic
- `deeper` → Expand current topic with more detail
- `questions` → User asks for clarification
- `save` → Generate summary file for this topic

### Learn Step 3: Generate Summary File

When user says `save` or completes a topic, output:

```markdown
# [Topic] - Exam Summary

> Generated: [YYYY-MM-DD]
> Sources: [list of files used]

## 1-Minute Overview
Ultra-condensed version for last-minute review. Max 5 bullet points.

## Key Concepts
[Structured breakdown from teaching session]

## Formulas / Code Snippets / Syntax
[Exact notation to memorize, if applicable]

## Comparison Tables
[Side-by-side comparisons for related concepts]

## Exam Patterns
[How this appears in past exams, expected formats]

## Common Mistakes
[What to avoid, frequent errors]

## Quick Self-Test

**Q1:** [Question]

**Q2:** [Question]

**Q3:** [Question]

<details>
<summary>Answers</summary>

1. [Answer]
2. [Answer]
3. [Answer]

</details>
```

Output path: `[subject]/summaries/[topic-slug]-summary.md`

**"all" option:** Generate separate summary file per topic, not one massive file.

---

## MODE: --mcq

Multiple choice practice based on their materials.

### MCQ Format

Generate 5 questions per session:

```
**Q1/5: [Topic from their notes]**

[Context from their lecture material]

A) [Plausible wrong - common misconception]
B) [Plausible wrong - partially correct]
C) [Correct answer]
D) [Plausible wrong - related concept confusion]

Your answer:
```

### MCQ Feedback

**If wrong:**
- Explain why incorrect
- Reference specific lecture/material
- Clarify the misconception

**If correct:**
- "Why is [wrong answer] incorrect?" (verify understanding, not just luck)

### MCQ Session End

```
Score: X/5
Weak areas: [topics to review with specific file references]

Generate flashcards for missed concepts? [Y/n]
```

### MCQ Card Output (Obsidian SR Format)

```markdown
#flashcard #[subject] #[topic]

Q: [Question from session]
A: [Concise answer, max 2-3 lines]

---
```

Output instruction: "Copy to: [subject]/cards/[topic].md"

---

## MODE: --code

Handwritten code practice for exam preparation.

### Code Challenge Format

```
**Handwritten Code Challenge**

Topic: [From their assignments/lectures]
Language: [Python/R/etc. based on their materials]
Time: ~5 minutes (imagine paper, no autocomplete)

Task:
[Specific function/algorithm from their course]

Requirements:
- [Key element 1]
- [Key element 2]
- [Edge case to handle]

Write your code:
```

### Code Review Checklist

After user submits:

```
Review (as exam grader):

[ ] Imports correct and complete?
[ ] Function signature matches convention?
[ ] Variable names clear?
[ ] Core logic correct?
[ ] Edge cases handled?
[ ] Syntax errors? (brackets, colons, indentation)
[ ] Would run first try on paper?

Feedback:
- [What would lose marks]
- [What's good]
- [Suggested fix]
```

### Code Card Output

Generate flashcards for syntax/patterns that need memorization:

```markdown
#flashcard #[subject] #code

Q: Write the signature for [function] in [language]
A: `def function_name(param: Type) -> ReturnType:`

---
```

---

## MODE: --oral

Simulate oral examination with professor persona.

### Oral Format

```
**Oral Exam Simulation**

Topic: [Randomly selected from their materials]

Professor: "Explain [concept from their notes]."
```

### Oral Drill Pattern

After user explains:

1. **Probe deeper:** "Why not [alternative approach]?"
2. **Edge case:** "What happens if [failure scenario]?"
3. **Connect:** "How does this relate to [other topic from their materials]?"
4. **Challenge:** "A student says [common misconception]. How do you respond?"

Continue 3-4 levels deep until user says `stop` or demonstrates mastery.

### Oral Session End

```
Oral Exam Feedback:

Strengths:
- [What was explained well]

Gaps:
- [Where explanation was weak]
- [Follow-ups that caused hesitation]

Review suggestions:
- [Specific files/topics to revisit]
```

No file output for oral mode (live feedback only).

---

## Constraints

1. **ONLY use content from their materials folder** - never generic textbook knowledge
2. **Match their terminology** - use exact terms from their lectures
3. **Reference sources** - "As covered in week3-cap.md..."
4. **Calibrate to their exams** - if past exams exist, match that difficulty
5. **Language/libraries from their code** - check assignments for what they actually use
6. **If topic NOT in materials:** "This wasn't in your course files. Want general explanation or skip?"

## Output Rules

- **--learn mode:** Full markdown summary files (user copies to summaries/)
- **--mcq mode:** Flashcards as text (user copies to cards/)
- **--code mode:** Flashcards as text (user copies to cards/)
- **--oral mode:** No file output, live feedback only

All outputs are TEXT for manual copy (Option A approach - no direct file writes).
