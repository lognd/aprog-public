# Study Guides

One file per curriculum topic (numbered to match docs/curriculum-map.md).
Each file inventories everything a student must know to complete that
topic's activities and assignments.

Three uses:
1. Audit -- every knowledge item is tagged [taught: this topic] or
   [assumed: row N]. An [assumed] item whose source row does not actually
   teach it is a curriculum gap.
2. Slides -- the "Know" bullets are written to lift directly onto slides.
3. Studying -- students read the checklist before starting the topic.

## File format (all guides follow this exactly)

```markdown
# Study Guide N: <Topic Name>

One-paragraph plain-language summary of what this topic is about.

## Know before you start

Knowledge this topic assumes from earlier rows. Each line names the item
and its source row:
- <item> [assumed: row K -- <topic name>]

## Taught here

The knowledge this topic's artifacts introduce and exercise. Grouped by
concept, one bullet per fact/skill, each starting with an imperative
"Know ..." / "Be able to ..." statement:
- Know <fact stated fully, self-contained, slide-ready>
- Be able to <skill, concrete>

## Per-artifact requirements

### <slug> (activity|assignment)
- Requires: <comma-separated knowledge items, each tagged [taught] or [assumed: row K]>
- Produces: <what completing it proves the student can do, one line>

## Study checklist

- [ ] <short imperative item a student can self-test>
```

Rules: ASCII only; no answers or passphrases from any activity may appear
in a guide; knowledge items must be derived from the artifacts' actual
content (READMEs, question banks, graders), not from the topic name.
