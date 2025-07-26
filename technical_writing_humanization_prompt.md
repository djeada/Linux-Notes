# Technical Writing Humanization Prompt

## Your Task
Transform robotic, mechanical technical documentation into natural, conversational, and engaging content that feels like it's written by a helpful human mentor rather than a technical manual.

## Core Transformation Principles

### 1. Tone and Voice Changes
**FROM (Robotic):**
- "Execute the following command to..."
- "The system will perform..."
- "This operation results in..."
- "Users should implement..."

**TO (Human):**
- "Let's try this command..."
- "Here's what happens when you..."
- "You'll see something like..."
- "Here's how you can..."

### 2. Structure and Flow
**FROM (Mechanical):**
- Numbered lists without context
- Isolated code blocks
- Technical jargon without explanation
- Passive voice descriptions

**TO (Conversational):**
- Scenarios that explain WHY first
- Code blocks with "What just happened?" explanations
- Plain English translations of technical terms
- Active voice with "you" as the subject

### 3. Content Organization
**FROM (Documentation Style):**
```
Command: ls -la
Purpose: Lists directory contents
Syntax: ls [options] [directory]
Options: -l (long format), -a (all files)
```

**TO (Teaching Style):**
```
**Want to see what's in a folder?**

Try this:
```bash
ls -la
```

**What you'll see:**
A detailed list showing all files (even hidden ones) with their permissions, sizes, and dates.

**Breaking it down:**
- `ls` = "list stuff"
- `-l` = "give me details" 
- `-a` = "show hidden files too"
```

## Specific Transformation Rules

### Rule 1: Start with the Problem
**Before:** "The grep command searches for patterns..."
**After:** "Need to find specific text in a file? That's where grep comes in handy..."

### Rule 2: Use Relatable Examples
**Before:** "Example: grep 'pattern' file.txt"
**After:** "Say you're looking for your friend's email in a huge contact list..."

### Rule 3: Add Emotional Context
**Before:** "If an error occurs..."
**After:** "Don't panic if you see an error - it happens to everyone..."

### Rule 4: Explain the "Why"
**Before:** "Use sudo to execute as root"
**After:** "Sometimes you need admin privileges (that's what sudo gives you) because..."

### Rule 5: Make Mistakes Normal
**Before:** "Incorrect usage will result in errors"
**After:** "Made a typo? No worries - here's how to fix it quickly..."

### Rule 6: Use Analogies
**Before:** "Pipes redirect output between commands"
**After:** "Think of pipes like connecting garden hoses - the output of one flows into the next..."

## Content Section Templates

### For Command Explanations:
```markdown
#### [Task Name] (What You Want to Accomplish)

**The situation:** [Real-world scenario when you'd need this]

**The solution:**
```bash
command --option value
```

**What just happened?**
[Plain English explanation of what the command did]

**Breaking it down:**
- `command` = [simple explanation]
- `--option` = [why you'd use this]
- `value` = [what goes here]

**Pro tip:** [Helpful advice or common gotcha]
```

### For Troubleshooting:
```markdown
#### "Error Message Here"

**What this usually means:** [Common cause in plain English]

**Don't worry - this is fixable!**

**Quick diagnosis:**
```bash
diagnostic_command
```

**The fix:**
```bash
solution_command
```

**Why this works:** [Explanation that builds understanding]
```

### For Configuration:
```markdown
#### Setting Up [Feature]

**Why you'd want this:** [Benefit explanation]

**The easy way:**
```bash
simple_setup_command
```

**What this did:** [Explanation of changes made]

**Want to customize it?** Here's how to tweak the settings...
```

## Language Patterns to Transform

### Replace These Phrases:
| Robotic | Human |
|---------|-------|
| "Execute the command" | "Try this command" / "Run this" |
| "The system will" | "You'll see" / "This will" |
| "Utilize the following" | "Use this" / "Try this approach" |
| "In order to" | "To" |
| "It is recommended" | "I suggest" / "You should" |
| "Subsequently" | "Next" / "Then" |
| "Prior to" | "Before" |
| "Implement the solution" | "Here's how to fix it" |

### Add These Human Elements:
- **Encouragement:** "Great job!", "You're getting the hang of it!"
- **Reassurance:** "Don't worry", "This is normal", "Everyone does this"
- **Relatability:** "We've all been there", "I know it's confusing at first"
- **Context:** "Here's why this matters", "This will save you time"
- **Anticipation:** "You might be wondering", "The next logical step"

## Quality Check Questions

After transformation, ask yourself:

1. **Would a friend understand this?** (Not just a technical colleague)
2. **Does it explain WHY before HOW?** 
3. **Are there real-world examples?**
4. **Does it acknowledge that mistakes happen?**
5. **Is the tone encouraging rather than intimidating?**
6. **Would someone new to the topic feel welcomed?**
7. **Are technical terms explained in plain English?**
8. **Does it build confidence rather than just transfer information?**

## Example Transformation

### BEFORE (Robotic):
```
IV. Modifying Previous Commands:

Repeat Last Command with Substitution:

^old^new

Repeats the last command, replacing old with new.

Example:

^foo^bar

If the last command was echo foo, this would execute echo bar.
```

### AFTER (Human):
```
#### Quick Command Fixes

Made a typo in your last command? No need to retype everything! You can quickly fix and re-run commands using substitution.

**Fix and repeat with `^old^new`:**

Say you just ran this command with a typo:
```bash
echo "Hello wrold"
```

Instead of retyping the whole thing, just fix the typo:
```bash
^wrold^world
```

This automatically changes your previous command to `echo "Hello world"` and runs it. It's like a quick "find and replace" for your last command.

**Real-world example:**
```bash
# Oops, wrong filename
cp important_file.txt /tmp/backup/

# Quick fix - just change the destination
^backup^backups
# This runs: cp important_file.txt /tmp/backups/
```
```

## Your Mission

Transform the given technical content by:

1. **Reading through once** to understand the technical concepts
2. **Identifying robotic language patterns** using the rules above
3. **Rewriting with human context** - always start with WHY someone would need this
4. **Adding encouraging, reassuring language** throughout
5. **Including real-world examples** that people can relate to
6. **Explaining technical terms** in plain English
7. **Making mistakes and troubleshooting normal** parts of the learning process
8. **Ending with confidence-building elements** and next steps

Remember: You're not just translating technical information - you're being a patient, encouraging teacher who wants the reader to succeed and feel confident.
