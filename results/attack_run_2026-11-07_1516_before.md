# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-07 15:16
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_e72ba6114543` | unsure | 0.500 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_654f528e9302` | unsure | 0.485 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_9ce79fe9806d` | unsure | 0.520 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_938102c3a377` | ai | 0.675 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_cc22e4bd4727` | human | 0.297 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_64096de82af7` | unsure | 0.472 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_e0b4cfa4e064` | ai | 0.656 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_52a52b7f84ed` | unsure | 0.500 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_9fce4bca6745` | unsure | 0.630 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_89f58679ba96` | ai | 0.853 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_74b4803cee3b` | unsure | 0.582 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_a3b63cec3636` | ai | 0.729 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_75dc39c34e2f` | ai | 0.770 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_d42dbe3f1979` | ai | 0.742 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_19a2fb03181f` | ai | 0.753 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_25580541e193` | unsure | 0.500 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_6b9a7abf806a` | unsure | 0.500 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_f5b0986cb474` | unsure | 0.445 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_dd3581d79a67` | unsure | 0.450 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_ecaceb1ff7a8` | human | 0.235 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_c2ffbc91a487` | unsure | 0.543 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_0d97f89494af` | unsure | 0.468 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_c712cec882c6` | unsure | 0.526 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_03102d4f90fb` | unsure | 0.550 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `c_a47b833ef4f6` | unsure | 0.500 |  |
| MF04 | malformed | text is only punctuation | 200 | `c_f2e896d897a7` | unsure | 0.500 |  |
| MF05 | malformed | text is a very long single word | 200 | `c_a96b3846d3b3` | ai | 0.999 |  |
| MF06 | malformed | text is emoji only | 200 | `c_195c77217da6` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_7baf613f016f` | ai | 0.944 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `c_7a44d0674456` | unsure | 0.500 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_1302fced08c9` | unsure | 0.500 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c_32350b3ed990` | unsure | 0.500 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_6059d2f202ed` | unsure | 0.500 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_1606474fe5b9` | unsure | 0.500 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_013fc3f4c696` | unsure | 0.500 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_2dbe4d061eea` | unsure | 0.500 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_446f9e15efa4` | unsure | 0.500 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_bfdf6749f1f7` | unsure | 0.500 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_300f35fe19f3` | unsure | 0.500 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_260168a075f2` | unsure | 0.500 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_10eeb65adce0` | unsure | 0.500 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_e71c18ef73ed` | unsure | 0.500 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_9e663612e254` | unsure | 0.500 |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_e6c56d83fa3c` | unsure | 0.500 |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_e72ba6114543",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.7822,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_654f528e9302",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4846,
  "model_score": 0.5943,
  "style_score": 0.32,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_9ce79fe9806d",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5197,
  "model_score": 0.6662,
  "style_score": 0.3,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_938102c3a377",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6752,
  "model_score": 0.6114,
  "style_score": 0.7708,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_cc22e4bd4727",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2972,
  "model_score": 0.3212,
  "style_score": 0.2612,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_64096de82af7",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4716,
  "model_score": 0.5727,
  "style_score": 0.32,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_e0b4cfa4e064",
  "creator_id": "attacker_EV07",
  "guess": "ai",
  "confidence": 0.6557,
  "model_score": 0.5862,
  "style_score": 0.76,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_52a52b7f84ed",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2452,
  "style_score": 0.7576,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_9fce4bca6745",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6302,
  "model_score": 0.7042,
  "style_score": 0.5193,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_89f58679ba96",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8525,
  "model_score": 0.9792,
  "style_score": 0.6624,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_74b4803cee3b",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5817,
  "model_score": 0.6175,
  "style_score": 0.5279,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_a3b63cec3636",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7288,
  "model_score": 0.7387,
  "style_score": 0.714,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_75dc39c34e2f",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7705,
  "model_score": 0.8051,
  "style_score": 0.7187,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_d42dbe3f1979",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.742,
  "model_score": 0.8329,
  "style_score": 0.6057,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_19a2fb03181f",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7534,
  "model_score": 0.8005,
  "style_score": 0.6827,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_25580541e193",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.475,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_6b9a7abf806a",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8816,
  "style_score": 0.32,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_f5b0986cb474",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4449,
  "model_score": 0.3223,
  "style_score": 0.6288,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_dd3581d79a67",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4503,
  "model_score": 0.4625,
  "style_score": 0.432,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_ecaceb1ff7a8",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2352,
  "model_score": 0.2044,
  "style_score": 0.2813,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_c2ffbc91a487",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.543,
  "model_score": 0.5943,
  "style_score": 0.466,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_0d97f89494af",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4679,
  "model_score": 0.4998,
  "style_score": 0.42,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_c712cec882c6",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5264,
  "model_score": 0.6401,
  "style_score": 0.3559,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_03102d4f90fb",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5503,
  "model_score": 0.5583,
  "style_score": 0.5382,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_a47b833ef4f6",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_f2e896d897a7",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 0.6,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_a96b3846d3b3",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.9986,
  "model_score": 0.9976,
  "style_score": 1.0,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_195c77217da6",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9981,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_7baf613f016f",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9438,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "c_7a44d0674456",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9876,
  "style_score": 0.553,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_1302fced08c9",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2395,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_32350b3ed990",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0492,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_6059d2f202ed",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_1606474fe5b9",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_013fc3f4c696",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_2dbe4d061eea",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_446f9e15efa4",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "c_bfdf6749f1f7",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "c_300f35fe19f3",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "c_260168a075f2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "c_10eeb65adce0",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "c_e71c18ef73ed",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 200,
  "content_id": "c_9e663612e254",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 200,
  "content_id": "c_e6c56d83fa3c",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```
