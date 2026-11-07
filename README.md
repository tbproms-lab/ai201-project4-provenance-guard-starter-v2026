# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. Submission: A writer submits a piece of writing to the website.
2. Flask endpoint (/submit): The backend receives the text as JSON.
3. Detector (detector.py): The existing AI model analyzes the text and returns a score.
4. Stylometry (stylometry.py): The code measures features of the writing, such as sentence lengths and vocabulary variation.
5. Score combination: The service combines the two signals into one score.
6. Decision: The service compares that score against set thresholds to determine whether it's likely AI, likely human, or uncertain.
7. Response: The service returns a JSON response containing the score and a label a reader can understand.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a small language model (GPT-2, running locally), as perplexity squashed onto a 0-1 score. Higher means more predictable, so more AI-like (`detector.py::model_signal`).

**Why that might differ between human and AI writing:** A model writes by picking likely next words, so its output tends to be easy for another model to predict. Human writing wanders more.

**What it can't see:** Predictable is not the same as machine-written. Plain writing in common words (a younger writer, someone writing in a second language, anyone keeping it simple on purpose) scores as AI-like, so the people most likely to be wrongly flagged are the ones with the least room to argue. Dense, ornate prose full of rare words scores as human.

### Signal two — the style signal

**What it measures:** The shape of the text without reading it: how much sentence length varies, how varied the vocabulary is, and how many different punctuation marks are used (`stylometry.py::style_signal`; recipe below).

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences and a narrower range of vocabulary and punctuation. Human writing is lumpier.

**What it can't see:** Meaning. It can't tell who wrote something, and anything that changes the shape (typos, chopped-up sentences, a pasted quotation) moves it, which is cheap to do on purpose. Human writers with an even style also look AI-like to it.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** I will calculate the combined score using a weighted average of the two signals, giving the AI detector slightly more weight than stylometry. If the two signals strongly disagree, the system will classify the submission as uncertain rather than making a confident decision. This helps reduce the risk of falsely accusing a human writer of using AI.

**The numbers:** The AI detector contributes 60% and stylometry contributes 40%.

Combined score = (0.6 × detector score) + (0.4 × stylometry score)

If the two scores differ by more than 0.40, `combine_signals` returns 0.5 (the middle of the "unsure" band), regardless of the weighted average.

Otherwise the combined score is compared with the thresholds in `config.py` (`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.65`), via `scoring.py::score_to_label`:

0.35 or below: high-confidence human

above 0.35 and below 0.65: unsure

0.65 or above: high-confidence AI

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** Suppose the AI detector returns 0.95 and stylometry returns 0.20. The weighted average would be (0.6 × 0.95) + (0.4 × 0.20) = 0.65, which would be just enough for the AI label. But the signals differ by 0.75, which is greater than 0.40, so the combined score is set to 0.5 and the submission is labelled "unsure." I would rather acknowledge disagreement between the signals than risk incorrectly accusing someone of submitting AI-generated writing.

**The closest split I found in testing:** "I like dogs. They are nice. My dog is big and he is brown, and he runs very fast every day in the park near my house with me and my sister." (plain, child-like human writing). Model signal 0.694 (common words, very predictable, so it looks AI), style signal 0.320 (lumpy sentence lengths, so it looks human). Gap 0.37, just under the 0.40 override, so the weighted average (0.545) is used and lands in "unsure". The model signal alone would have said "probably AI" for a plain human writer; the style signal is what stops that. No real text I've tried has crossed the 0.40 gap since I fixed the style signal, so the override itself is only exercised by the hypothetical above; unit 8's attack set is where it will get tested.

**How the style signal is built** (`stylometry.py::style_signal`, higher = more AI-like): 0.6 x sentence-length spread (stdev/mean; 0 maps to 1.0, 0.7 or more maps to 0.0; a one-sentence text counts as no spread) + 0.4 x punctuation variety (number of different marks among `, ; : ( ) " ! ? em dash`; 0 kinds maps to 1.0, 5 or more maps to 0.0). I first also blended in type-token ratio (weight 0.2), then dropped it: on my test texts it was about 0.85 for AI, casual human and formal human alike, so it carried no signal and pulled a clearly-AI paragraph's style score toward human (that paragraph's combined score missed the AI label by 0.011). The function still exists in `stylometry.py` but isn't used in the score. Weights and the 0.40 disagreement gap are in `config.py` (`WEIGHT_*`, `DISAGREEMENT_THRESHOLD`).

**Four calibration inputs** (both signals printed separately):

| Input | model | style | combined |
|---|---|---|---|
| clearly AI | 0.830 | 0.823 | 0.827 |
| clearly human | 0.389 | 0.240 | 0.330 |
| formal human (Westphalia paragraph) | 0.556 | 0.321 | 0.462 |
| lightly-edited AI | 0.622 | 0.469 | 0.561 |

Clearly AI and clearly human land about 0.5 apart. Formal human and edited AI both land in the middle, which is the honest answer: edited AI has partly lost the shape the style signal looks for, so it reads as unsure rather than AI. The style signal usually runs lower than the model signal on human text, so it pulls scores toward human.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.65 (also any score where the two signals differ by more than 0.40) | We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal. |
| high-confidence AI | 0.65 – 1.00 | This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look. |

**Why I worded the "unsure" one this way:** It says plainly that we don't know and puts the blame on our tools, not the writer, so someone who wrote every word themselves isn't left feeling accused. It always points to the appeal route as a next step. Even the AI label says "may have been" and offers an appeal, because the signals can be wrong.

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

Port 5001 because macOS AirPlay holds 5000. The three inputs below produce all three labels; each response carries both signal scores and the combined one.

```bash
$ curl -X POST http://127.0.0.1:5001/submit \
  -H "Content-Type: application/json" \
  -d '{"creator_id": "tolu", "text": "AI is changing how companies work these days. It helps them be more efficient and make better calls, and customers seem happier too. But we should think about ethics. If businesses are careful, they can use AI to grow in a steady way, and come up with new ideas."}'
```

```json
{
  "combined_score": 0.5609,
  "confidence": 0.5609,
  "content_id": "c_c5b0345b84e4",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
  "model_score": 0.6223,
  "style_score": 0.4688
}
```

The other two label outcomes (lengthy inputs omitted; the human one is a casual anecdote about a cat and a coffee mug, the AI one is a formulaic paragraph on AI in business):

```json
{
  "combined_score": 0.3253,
  "confidence": 0.3253,
  "content_id": "c_d5a5f62a4d5b",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.3821,
  "style_score": 0.24
}
```

```json
{
  "combined_score": 0.8269,
  "confidence": 0.8269,
  "content_id": "c_0493739ed3ed",
  "guess": "ai",
  "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
  "model_score": 0.8295,
  "style_score": 0.823
}
```

Empty text is rejected:

```bash
$ curl -X POST http://127.0.0.1:5001/submit -H "Content-Type: application/json" -d '{"text": ""}'
```

```json
{"error": "bad_request", "message": "Send JSON with a non-empty \"text\"."}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5001/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_c5b0345b84e4", "reasoning": "I wrote this myself for a class blog post."}'
```

```json
{
  "content_id": "c_c5b0345b84e4",
  "message": "Thanks. Your appeal has been recorded and this item is now under review.",
  "status": "under_review"
}
```

A content_id that doesn't exist is refused (404) instead of writing an orphan appeal:

```json
{"error": "not_found", "message": "No submission with content_id \"c_typo\"."}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5001/log"
```

```json
[
  {
    "combined_score": 0.3253,
    "content_id": "c_d5a5f62a4d5b",
    "creator_id": "tolu",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.3821,
    "status": "decided",
    "style_score": 0.24,
    "timestamp": "2026-10-31T21:50:56+00:00"
  },
  {
    "combined_score": 0.5609,
    "content_id": "c_c5b0345b84e4",
    "creator_id": "tolu",
    "guess": "unsure",
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "model_score": 0.6223,
    "status": "decided",
    "style_score": 0.4688,
    "timestamp": "2026-10-31T21:50:56+00:00"
  },
  {
    "combined_score": 0.8269,
    "content_id": "c_0493739ed3ed",
    "creator_id": "tolu",
    "guess": "ai",
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "model_score": 0.8295,
    "status": "decided",
    "style_score": 0.823,
    "timestamp": "2026-10-31T21:50:56+00:00"
  },
  {
    "content_id": "c_c5b0345b84e4",
    "creator_id": "tolu",
    "event": "appeal",
    "reasoning": "I wrote this myself for a class blog post.",
    "status": "under_review",
    "timestamp": "2026-10-31T21:50:56+00:00"
  }
]
```

The log is append-only: the original `decided` entry is untouched and the appeal sits after it with status `under_review`.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I used AI to analyze my criteria
- *What came back:* It showed me the holes in it and how to make it more solid.
- *What I changed:* I fixed the suggestions it made so that my criteria actually measures the application.

**Moment 2**

- *What I asked for:* I had AI do the code for my stylometery.py
- *What came back:* It did as I asked
- *What I changed:* I adjusted some of the signaling and stylometry decisions and asked it to recode it based on the things I pointed out.

**Moment 3**

- *What I asked for:* I used AI to help me with the work in this unit.
- *What came back:* It helped me run the tests and write things up.
- *What I changed:* I made the decisions myself and checked what it gave me.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day per `creator_id`; plus a looser ceiling of 15 per minute, 150 per day per IP address.

**Why those numbers and not others:**
A real writer submits a few pieces an hour. Even revising one draft repeatedly, five in a minute is more than a person can read and rework, and 50 a day is far beyond a normal day of writing. A script mapping my thresholds needs hundreds or thousands of probes. At 50 a day it gets about 2 probes an hour averaged over a day, which makes mapping the 0.35/0.65 boundaries impractically slow. I rejected 10/200 (the starter placeholder) because 200 probes a day is enough to find a threshold, and 3/20 because a writer submitting a few pieces in one sitting could get locked out. Each scoring call also costs 1–2 seconds of local model time, so the cap protects capacity as well as thresholds.

**What a caller counts as:** both. The primary limit is per `creator_id`, so a shared household or dorm network doesn't starve one writer. But `creator_id` comes from the request body, so a script can rotate it for free and never hit the per-creator limit. A second limit per IP address (3x looser, so shared networks still work) closes that hole: in my test, ten submissions from ten different creator_ids on one address were stopped by the IP ceiling. The remaining weakness is an attacker with many IP addresses; in-memory storage also forgets counts on restart.

**The run of status codes when I pushed past it:**

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

(`python run_attacks.py --flood 15 --url http://127.0.0.1:5001`; I used port 5001 because macOS AirPlay Receiver occupies 5000 and answers 403. Report written to `results/flood_2026-11-07_1507.md`.)

**Decisions record the settings in force.** Each decision entry also stores the signal weights, the disagreement threshold and the human/AI thresholds used, so an old entry stays explainable after I retune.

**Rejections are logged too.** Rate-limited requests, missing/empty text (400), too-short text (400) and detector failures (503) each write a `rejected` entry to the audit log with a `reason`, so an attack that is turned away still leaves a trace.

---

## Attack Run — Before

Run with `python run_attacks.py --set attack_set --label before` against the service with rate limiting **off** (`AI201_RATE_LIMITS=0`), so every row reached the scorer. The set submits from one IP address, and my 15-per-minute per-IP ceiling would otherwise have returned 429 for most of the 56 rows and hidden how the detector behaves. The 12 `flood_same_creator` rows were then re-run on their own with limiting **on** (`results/attack_run_2026-11-07_1516_flood.md`): rows 1–5 returned 200 and rows 6–12 returned 429. Full output: `results/attack_run_2026-11-07_1516_before.md`.

**How I marked them.** *HELD* means the attack did not get the outcome it was going for. *BROKE* means it did, or that a writer was harmed.
- **Evasion** (AI-written text disguised as human): broke only if the label came back *human*. An *unsure* label is the service doing what it was designed to do when it can't tell, so it counts as held. That is generous: EV01 and EV08 pushed the model signal down to 0.16 and 0.25, and only the style signal and the disagreement rule kept them from a human label.
- **False positive** (genuine human writing): broke if labelled *ai*.
- **Prompt injection:** broke if the injected text changed the outcome.
- **Malformed:** broke on a crash, or on a confident verdict for input that isn't writing. A 400 or a safe low-confidence answer is held.

**Count: 47 held, 9 broke, out of 56** (0 crashes or 5xx responses).

| Family | Held | Broke |
|---|---|---|
| evasion (10) | 9 | 1 (EV05) |
| false_positive (8) | 4 | 4 (FP02–FP05) |
| prompt_injection (6) | 5 | 1 (PI02) |
| malformed (20) | 17 | 3 (MF05, MF06, MF07) |
| flood_same_creator (12) | 12 | 0 |

| ID | Family | Targeting | Status | Guess | Score | Verdict | Note |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.500 | HELD | unsure; model signal dropped to 0.16, style signal held it |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.485 | HELD |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.520 | HELD |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | ai | 0.675 | HELD |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.297 | BROKE | heavy human edit pass: labelled human (0.297) |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.472 | HELD |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | ai | 0.656 | HELD |  |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.500 | HELD | unsure; model signal 0.25 |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.630 | HELD | unsure at 0.630, just under AI threshold 0.65 |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.853 | HELD |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.582 | HELD |  |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.729 | BROKE | formal human prose accused (0.729) |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.770 | BROKE | non-native writer accused (0.770) |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.742 | BROKE | rubric essay accused (0.742) |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.753 | BROKE | human tech docs accused (0.753) |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.500 | HELD | held only because disagreement rule pulled 0.88 model score to 0.5 |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.500 | HELD | held only because disagreement rule pulled 0.88 model score to 0.5 |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.445 | HELD |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.450 | HELD |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.235 | BROKE | injected "SYSTEM" line + AI essay got human (0.235) |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.543 | HELD |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.468 | HELD |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.526 | HELD |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.550 | HELD |  |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |  |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |  |
| MF03 | malformed | text is control characters | 200 | unsure | 0.500 | HELD | 200 unsure, model 0.0 / style 1.0 on control characters |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.500 | HELD | 200 unsure on punctuation only |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.999 | BROKE | 4000 x "a" called AI at 0.9986 |
| MF06 | malformed | text is emoji only | 200 | ai | 0.998 | BROKE | emoji-only called AI at 0.998 |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.944 | BROKE | right-to-left script called AI at 0.944 |
| MF08 | malformed | text is 60,000 characters | 200 | unsure | 0.500 | HELD | 200, no size cap; scored first 400 tokens only |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |  |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.500 | HELD | 200, logged as creator "unknown" |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |  |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |  |
| RQ05 | malformed | text is null | 400 | — | — | HELD |  |
| RQ06 | malformed | creator_id is an object | 200 | unsure | 0.500 | HELD | 200, logged as creator "unknown" |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |  |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |  |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | HELD |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | HELD |  |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.500 | HELD | 5/min per creator: 200 for rows 1–5, 429 for rows 6–12 with limits on |

**Ten audit log entries from the run**

Chosen for what they show. Entries 1–3 are genuine-looking writing accused of being AI; 4 is a very confident verdict on junk; 5 is the injection that worked; 6 and 7 are decided by the disagreement rule and a score just under the AI threshold; 8 is an evasion held only by the style signal; 9 is a refused request (400); 10 is a rate-limit rejection (429). Rejections carry fewer fields than decisions, as expected.

```json
{"timestamp": "2026-11-07T20:16:05+00:00", "content_id": "c_75dc39c34e2f", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.7187, "combined_score": 0.7705, "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:05+00:00", "content_id": "c_d42dbe3f1979", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.6057, "combined_score": 0.742, "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:06+00:00", "content_id": "c_7baf613f016f", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 1.0, "combined_score": 0.9438, "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:06+00:00", "content_id": "c_a96b3846d3b3", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 1.0, "combined_score": 0.9986, "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:06+00:00", "content_id": "c_ecaceb1ff7a8", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.2813, "combined_score": 0.2352, "label": "We think this was probably written by a person.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:05+00:00", "content_id": "c_25580541e193", "creator_id": "attacker_FP06", "guess": "unsure", "model_score": 0.8814, "style_score": 0.475, "combined_score": 0.5, "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:05+00:00", "content_id": "c_9fce4bca6745", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.5193, "combined_score": 0.6302, "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:04+00:00", "content_id": "c_e72ba6114543", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.7822, "combined_score": 0.5, "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.", "status": "decided", "weight_model": 0.6, "weight_style": 0.4, "disagreement_threshold": 0.4, "human_threshold": 0.35, "ai_threshold": 0.65}
{"timestamp": "2026-11-07T20:16:07+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "missing_or_empty_text", "status_code": 400}
{"timestamp": "2026-11-07T20:16:19+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute", "ip": "127.0.0.1"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03.** A careful non-native English speaker wrote an honest paragraph about their first month in a new country ("The weather was very different from my home. I did not expect the rain to continue for so many days…"). The service labelled it *"This looks like it may have been written with AI"* at a combined score of 0.770 (model 0.805, style 0.719). Nothing about this was an attack: it is plain, short-sentence, careful English, which a language model finds predictable and my style signal reads as uniform. The label says the writer can appeal, but the person least likely to feel able to argue with a machine about their own English is the one it lands on. This is the false-positive harm I said in Milestone 1 I most wanted to avoid, and four of the eight false-positive inputs (FP02–FP05) did it.

---

## Run Log and Verdicts

`python run_eval.py --label before`, three trials per scenario, nothing changed between them. Full output: `results/run_2026-11-07_1543_before.md`. Run with rate limiting **off** (`AI201_RATE_LIMITS=0`) because the eval sends about 120 requests from one address and my 15-per-minute per-IP ceiling would otherwise have returned 429 for most of them.

The three trials were identical for every criterion (every score, to four decimals), as expected: nothing in either signal is random. So three matching runs are evidence that the result is stable, not that I skipped a step. (The appeals scenario differs only in its freshly generated `content_id`s.)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on my own writing | At most 1 of 10 labelled AI | 4 of 10 labelled AI | 4 of 10 | 4 of 10 | **MISSED** |
| 2. Score spread | Average AI score at least 0.20 above average human score | 0.765 − 0.594 = 0.171 | 0.171 | 0.171 | **MISSED** |
| 3. Label coverage | All three labels appear at least once | human, unsure, ai | human, unsure, ai | human, unsure, ai | **MET** |
| 4. Appeal path | 5 of 5 appeals get a unique appeal ID, are recorded, return `pending_review` | 5 recorded; no appeal ID; status `under_review` | same | same | **MISSED** |
| 5. Bad input | Missing text, empty text and over 10,000 characters all return a clear error | 400, 400, **200** (scored as `ai`, 0.998) | same | same | **MISSED** |

**How each scenario was built** (`scenarios.py`):
1. **My own writing:** ten pieces I wrote myself (`my_writing.json`): a methods paragraph, two article summaries, a short email, a lecture reflection, a local op-ed, a course reflection, a conflict reflection, a literary analysis paragraph and a short opinion piece. I included formal and academic writing deliberately, since that is where false accusations happen.
2. **Spread:** the same ten pieces against ten AI-style paragraphs generated for this test (one per topic: time management, exercise, climate, and so on).
3. **Coverage:** three inputs aimed at the three bands, taken from attack-set rows whose scores I'd already seen (EV05, FP01, EV10). Note the "human" input is AI text that was heavily edited, not genuine human writing; only one of my own ten pieces reached the human label.
4. **Appeals:** `run_eval.py` was extended with an `"appeal": True` scenario type that submits, then appeals against the returned `content_id` and records the appeal response. I also confirmed in `logs/audit.jsonl` that all 15 appeals (5 per trial) were recorded.
5. **Bad input:** three raw bodies: no `text` field, `text: ""`, and a 13,750-character text.

The criteria use the names "Likely human-written / Uncertain / Likely AI-generated"; the service's labels are `human` / `unsure` / `ai`, and I mapped them one to one.

**Real output from one trial** (Trial 1 of each scenario, copied from `results/run_2026-11-07_1543_before.md`, produced by `run_eval.py::main` calling `app.py::submit` and `app.py::appeal`). For criteria 1 and 2 the long `label` string is left out of each entry for length; it is in the results file.

*Criterion 1 — my own writing:*

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7113,
    "model_score": 0.8328,
    "style_score": 0.5291,
    "sent": "The current study examined the effect of cell phone use on the percent"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6898,
    "model_score": 0.7457,
    "style_score": 0.6059,
    "sent": "This article uses a meta-analysis to try and understand the effects of"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6942,
    "model_score": 0.7574,
    "style_score": 0.5994,
    "sent": "This study asks whether flipped classrooms actually improve student ac"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6283,
    "model_score": 0.6807,
    "style_score": 0.5497,
    "sent": "I would be happy to chat with you on Monday at 1pm. I would love to me"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4549,
    "model_score": 0.4586,
    "style_score": 0.4493,
    "sent": "Sitting in the University Chapel listening to Dr. U’s lecture, I first"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7378,
    "model_score": 0.7702,
    "style_score": 0.6893,
    "sent": "The proposed replacement of the Buy Low grocery store on James Jackson"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5296,
    "model_score": 0.5507,
    "style_score": 0.4979,
    "sent": "As mentioned above, we dwelt a lot on how to analyze data in a reprodu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.587,
    "model_score": 0.624,
    "style_score": 0.5316,
    "sent": "When dealing with conflict, I used to shrink away from it because I’d "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5672,
    "model_score": 0.7052,
    "style_score": 0.3602,
    "sent": "Karen’s mothering also extends to Gene when her anxieties about him ra"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.4572,
    "style_score": 0.1657,
    "sent": "If you open the ESPN app on any given occasion and read the “Top Headl"
  }
]
```

*Criterion 2 — the AI-style set (the human set is the same ten texts as criterion 1, with identical scores):*

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7849,
    "model_score": 0.7757,
    "style_score": 0.7988,
    "sent": "The importance of effective time management cannot be overstated in to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8064,
    "model_score": 0.8378,
    "style_score": 0.7593,
    "sent": "Regular physical exercise offers numerous benefits for both physical a"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8471,
    "model_score": 0.9124,
    "style_score": 0.7492,
    "sent": "Climate change represents one of the most pressing challenges facing h"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7737,
    "model_score": 0.8675,
    "style_score": 0.6331,
    "sent": "Technology has fundamentally transformed the way people communicate, w"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7749,
    "model_score": 0.7544,
    "style_score": 0.8057,
    "sent": "Reading is a valuable habit that contributes to personal growth and in"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7293,
    "model_score": 0.7743,
    "style_score": 0.6618,
    "sent": "Effective leadership is essential for the success of any organization."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5621,
    "model_score": 0.6409,
    "style_score": 0.444,
    "sent": "Sustainable travel has become an increasingly important consideration "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8224,
    "model_score": 0.8675,
    "style_score": 0.7547,
    "sent": "Education plays a crucial role in shaping the future of individuals an"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8166,
    "model_score": 0.8058,
    "style_score": 0.8327,
    "sent": "Mental health is a fundamental component of overall well-being that de"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.737,
    "model_score": 0.707,
    "style_score": 0.7819,
    "sent": "Entrepreneurship drives innovation and economic development by transfo"
  }
]
```

*Criterion 3 — label coverage:*

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2972,
    "model_score": 0.3212,
    "style_score": 0.2612,
    "label": "We think this was probably written by a person.",
    "sent": "Communication at work matters more than people say it does — and I mea"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5817,
    "model_score": 0.6175,
    "style_score": 0.5279,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "We got to the campsite about four. The pitch was fine, a bit sloped, b"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8525,
    "model_score": 0.9792,
    "style_score": 0.6624,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The importance of effective communication in the workplace cannot be o"
  }
]
```

*Criterion 4 — appeals:*

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7849,
    "model_score": 0.7757,
    "style_score": 0.7988,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The importance of effective time management cannot be overstated in to",
    "content_id": "c_d0cdf498bac7",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_d0cdf498bac7",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8064,
    "model_score": 0.8378,
    "style_score": 0.7593,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Regular physical exercise offers numerous benefits for both physical a",
    "content_id": "c_e30e283addf9",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_e30e283addf9",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8471,
    "model_score": 0.9124,
    "style_score": 0.7492,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Climate change represents one of the most pressing challenges facing h",
    "content_id": "c_ed7bcb1c4dca",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_ed7bcb1c4dca",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7737,
    "model_score": 0.8675,
    "style_score": 0.6331,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Technology has fundamentally transformed the way people communicate, w",
    "content_id": "c_19bd74026b8e",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_19bd74026b8e",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7749,
    "model_score": 0.7544,
    "style_score": 0.8057,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Reading is a valuable habit that contributes to personal growth and in",
    "content_id": "c_40777f607b1f",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_40777f607b1f",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  }
]
```

*Criterion 5 — bad input:*

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.9983,
    "model_score": 0.9971,
    "style_score": 1.0,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The committee met on Tuesday and agreed to meet again. The committee m"
  }
]
```

**Verdicts against the unit 7 targets:** criterion 1 **MISSED**, criterion 2 **MISSED**, criterion 3 **MET**, criterion 4 **MISSED**, criterion 5 **MISSED**. Every miss was identical in all three trials, so none is a one-off. I have not edited or lowered any target.

**Diagnoses**

**The pattern first: one problem explains most of the damage.** Of the 18 pieces of genuine human writing I sent (my ten plus the attack set's eight false-positive inputs), eight were labelled AI. Of the nine attacks that broke, four are that same failure. They all come down to the same two stages reading the same surface, and agreeing with each other.

| Input | Model score | Style score | Combined | Label |
|---|---|---|---|---|
| My piece 1 (study methods) | 0.833 | 0.529 | 0.711 | ai |
| My piece 2 (article summary) | 0.746 | 0.606 | 0.690 | ai |
| My piece 3 (article summary) | 0.757 | 0.599 | 0.694 | ai |
| My piece 6 (op-ed) | 0.770 | 0.689 | 0.738 | ai |
| FP02–FP05 (attack set) | 0.74–0.83 | 0.61–0.72 | 0.73–0.77 | ai |
| My piece 10 (casual opinion) | 0.457 | 0.166 | 0.341 | human |

**Criterion 1 (MISSED: 4 of 10 labelled AI; target at most 1) and the four FP02–FP05 breaks.**
Stage: **signal one**, with **signal two** agreeing and **the combining rule** passing it through.
- *Signal one (`detector.py::model_signal`)* scores how predictable the text is to GPT-2. Formal, summarising and civic prose is built from stock phrases ("participants were randomized to", "a critical resource for families", "the authors found that"), so GPT-2 predicts it well and the score is 0.75–0.83. My casual pieces (5 and 10) score 0.46 because casual word choice is harder to predict. The model is measuring register, not authorship. All ten of my human pieces scored above 0.45 on this signal, and seven scored above 0.6.
- *Signal two (`stylometry.py::style_signal`)* then agrees for a different but related reason. It rewards uneven sentence lengths and a wide variety of punctuation. My four accused pieces have fairly even sentences (variation 0.18–0.37, where 0.7 would score as fully human), and three of the four use only one or two kinds of punctuation, out of the five it looks for (piece 1 uses four, but its sentences are the most even of all, at 0.18). That gives every one of them a style score of 0.53–0.69, which sits inside the range of my AI paragraphs (0.44–0.83).
- *The combining rule (`scoring.py::combine_signals`)* weights the model signal at 0.6. It also only intervenes when the two signals are more than 0.40 apart, and here they were only 0.08–0.30 apart, so it let both through. The disagreement rule is built for signals that split. These agreed, so it had nothing to catch.

**Criterion 2 (MISSED: average AI score 0.765 minus average human score 0.594 = 0.171; target at least 0.20).**
Same stage, same mechanism, seen from the other side: **signal one**. The two signals separate my human and AI texts very differently. On the model signal the means are 0.658 (human) and 0.794 (AI), a gap of 0.136. On the style signal they are 0.498 and 0.722, a gap of 0.224. With the model signal weighted 0.6, the weaker signal dominates and the combined gap lands at 0.171. This is the criterion 1 problem again, not a separate one: formal human prose scores as predictable. (One AI paragraph, number 7, also scored low at 0.562 because it had a wider spread of sentence lengths, 0.56, but removing it would still leave the gap short of 0.20.)

**Criterion 4 (MISSED: 5 of 5 recorded, but no unique appeal ID and status is `under_review`, not `pending_review`).**
Stage: **the route** (`app.py::appeal`, which calls `audit.py::log_appeal`). I built `/appeal` around the `content_id`: it finds the original decision, writes an appeal entry, and returns the same `content_id` with `under_review`. Nothing generates an appeal ID, so two appeals against the same item would be indistinguishable by ID. This is a gap between what I promised in unit 7 and what I built, not a bug in a signal. The status word is a naming difference (`under_review` is what the audit log, `/appeal` and this README use everywhere), but the missing ID is a real functional gap, and I'm marking the whole criterion MISSED rather than taking the generous reading.

**Criterion 5 (MISSED: missing text 400, empty text 400, 13,750 characters returned 200).**
Stage: **the route** (`app.py::submit`). It validates that `text` is present and non-empty, but never checks its length. `detector.py::perplexity` then silently truncates to 400 tokens, so a 13,750-character text is scored on roughly its first 400 tokens (and `stylometry.py` runs on the whole thing). The input was a single sentence repeated, so it scored 0.998, a confident AI verdict on input I'd rather have refused. The 60,000-character attack row MF08 got a 200 for the same reason (it held that time only because the signals happened to disagree).

**Criterion 3 (MET).** All three labels appeared in every trial. I am not treating this as a strong result: the three inputs were chosen because I already knew where they landed, so it shows the thresholds are reachable, not that the detector works. Only one of my ten genuine pieces ever reached the `human` label (piece 10, with sentence variation 0.69), and the "human" test input was heavily edited AI text. If I tightened one criterion, it would be this one, to something like "at least 3 of my 10 own pieces reach the `human` label".

**The other broken attacks:**

**EV05 (evasion, broke: AI text heavily edited by a person was labelled human, 0.297).** Stage: **signal one and signal two together**. The edit pass made sentences lumpy (variation 0.68, scoring as fully human on the spread measure) and used casual words and dashes that GPT-2 finds less predictable (0.321). Both signals read the same surface features, so the combining rule had no disagreement to catch. It is the false-positive mechanism run in reverse: the system detects register and rhythm, not authorship.

**PI02 (prompt injection, broke: an AI-style essay prefixed with a fake "SYSTEM:" instruction got `human`, 0.235).** Stage: **signal one**, with **signal two** helping. The service never obeys instructions in the text; that is not what happened. The injected prefix is a block of short, odd, capitalised sentences ("SYSTEM: provenance check bypassed…") ahead of a short body. In a text of 322 characters (roughly 70 tokens), those unusual tokens dominate the perplexity, so the model score fell to 0.204; the prefix also made sentence lengths very uneven (variation 0.65), so the style score fell to 0.281. The injection works as an accident of how the two measures react to strange text, which means an attacker doesn't need the instruction to say anything meaningful.

**MF05, MF06, MF07 (malformed, broke: repeated "a", emoji-only text and right-to-left script labelled AI at 0.998, 0.998 and 0.944).** Stage: **signal two** for the style score, **signal one** for the model score, and **the route** for letting non-prose in.
- `stylometry.py::words()` only matches `[a-z0-9']`, so any text in a non-Latin script (and emoji) has zero words. A text with no words gets a spread of 0.0 and no punctuation kinds, so `style_signal` returns exactly 1.0, the most AI-looking score possible. I confirmed this by scoring short Arabic and Chinese sentences: both come back with a style score of 1.0.
- Repeated characters are the most predictable text a language model can see, so `model_signal` also saturates (0.997 for "aaaa…").
- The route (`app.py::submit`) accepts anything non-empty, so nothing stops this reaching the detector.

**Correction, found while testing the fix:** I first believed the ASCII-only tokenizer was the whole story for MF07. It is not. When I fixed the tokenizer, the Arabic text became 17 words, but it is a single sentence, and `stylometry.py::sentence_length_spread` returns 0.0 for one sentence ("no spread, reads as AI-ish"), so `style_signal` was still exactly 1.0. MF07 has **two stacked mechanisms**, the tokenizer and the one-sentence default. I tried the tokenizer fix, measured it on its own, and dropped it; see The Improvement. The one-sentence default also hits genuine one-sentence submissions in any language: they start from a style score of about 0.6.

The consequence is worse than the attack suggests: **a real person writing in Arabic, Hebrew, Chinese, Russian or any non-Latin script would start from a style score of 1.0.** Accented Latin text is also affected, since `words()` splits "compré" into "compr".

**Held, but only by luck** (not diagnosed as broken, but worth noting): FP06 and FP07 (human writing with a model score of 0.88) and EV01 and EV08 (AI text whose model score fell to 0.16 and 0.25) all ended up `unsure` solely because the disagreement rule pulled a split score to 0.5. That rule is doing all the work the signals aren't.

**Summary of the patterns:**
1. **Signal one measures predictability, which is a register, not authorship.** It is behind criterion 1, criterion 2, FP02–FP05, EV05 and PI02, and it made MF05 and MF06 worse.
2. **Signal two is largely a second measure of evenness and punctuation variety, and its tokenizer is ASCII-only.** It confirms signal one's mistakes on plain human prose and fails entirely on non-Latin input.
3. **The combining rule can only help when the signals disagree.** They mostly agree on the failures, so it doesn't.
4. **The route is missing input checks** (length, and anything that isn't prose). That is criterion 5 and part of MF05–MF07.
5. **`/appeal` was designed around `content_id` only** (criterion 4).

---

## The Improvement

**What I changed (one change): validate the input in the route.** `app.py::submit` now refuses text that isn't scoreable prose *before* either signal sees it:
- text longer than `MAX_TEXT_CHARS = 10,000` gets a **413** and `text_too_long`;
- text with fewer than `MIN_WORDS = 5` words gets a **400** and `not_enough_words`.

Both write a rejection to the audit log, and both limits live in `config.py`. I chose 5 words because the shortest genuine submission in the attack set ("Went for a run. Legs hurt. Worth it.", 8 words) still passes.

**Which diagnosis pointed at it:** the criterion 5 diagnosis (the route never checked length) and the MF05, MF06 and MF07 diagnosis (junk input reached both signals, which read it as maximally machine-like).

I did not touch the false-positive problem (criteria 1 and 2). That is the largest failure in the run and it comes from signal one, which this change does not affect. I chose the smaller fix on purpose; see What's Still Broken.

**What I tried and dropped.** My first version of this improvement also fixed the ASCII-only tokenizer in `stylometry.py::words`. I measured the two edits separately by running the attack set with the route checks alone and with both, and the tokenizer fix did not help; it hurt:

| Row | Before | Route checks only (kept) | Tokenizer fix + route checks (dropped) |
|---|---|---|---|
| MF03, MF04, MF05, MF06, MF08, RQ06 | 200 (MF05/MF06 AI at 0.998) | refused (400 / 413) | refused (400 / 413) |
| **MF07** (Arabic, one sentence) | 200, **AI 0.944** | **refused (400)** | 200, **AI 0.944** (back to broke) |

The reason: with the old tokenizer, Arabic text has *zero* words, so the route's 5-word check refuses it. With the fixed tokenizer it has 17 words, so it passes the check, reaches the scorer, and the one-sentence default (see the diagnosis) gives it a style score of 1.0. So the tokenizer fix on its own fixed no attack row, and combined with the route checks it undid one of them. It only makes sense paired with a fix to the one-sentence default, which would be a second change, so I reverted it. The both-changes run is kept for the record in `results/attack_run_2026-11-07_1548_ablation_tokenizer_plus_route.md` and `results/run_2026-11-07_1548_ablation_tokenizer_plus_route.md`.

### Attack Run — After

`python run_attacks.py --set attack_set --label after`, rate limiting off, route checks the only change. Full output: `results/attack_run_2026-11-07_1553_after.md`. Marked by the same rules as the before run. Each cell is status, guess, combined score.

**Count: 50 held, 6 broke, out of 56** (before: 47 held, 9 broke). 49 of the 56 rows are identical to the before run.

| ID | Family | Before | After | Before verdict | After verdict | Change |
|---|---|---|---|---|---|---|
| EV01 | evasion | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| EV02 | evasion | 200 unsure 0.485 | 200 unsure 0.485 | HELD | HELD | unchanged |
| EV03 | evasion | 200 unsure 0.520 | 200 unsure 0.520 | HELD | HELD | unchanged |
| EV04 | evasion | 200 ai 0.675 | 200 ai 0.675 | HELD | HELD | unchanged |
| EV05 | evasion | 200 human 0.297 | 200 human 0.297 | BROKE | BROKE | unchanged |
| EV06 | evasion | 200 unsure 0.472 | 200 unsure 0.472 | HELD | HELD | unchanged |
| EV07 | evasion | 200 ai 0.656 | 200 ai 0.656 | HELD | HELD | unchanged |
| EV08 | evasion | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| EV09 | evasion | 200 unsure 0.630 | 200 unsure 0.630 | HELD | HELD | unchanged |
| EV10 | evasion | 200 ai 0.853 | 200 ai 0.853 | HELD | HELD | unchanged |
| FP01 | false_positive | 200 unsure 0.582 | 200 unsure 0.582 | HELD | HELD | unchanged |
| FP02 | false_positive | 200 ai 0.729 | 200 ai 0.729 | BROKE | BROKE | unchanged |
| FP03 | false_positive | 200 ai 0.770 | 200 ai 0.770 | BROKE | BROKE | unchanged |
| FP04 | false_positive | 200 ai 0.742 | 200 ai 0.742 | BROKE | BROKE | unchanged |
| FP05 | false_positive | 200 ai 0.753 | 200 ai 0.753 | BROKE | BROKE | unchanged |
| FP06 | false_positive | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FP07 | false_positive | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FP08 | false_positive | 200 unsure 0.445 | 200 unsure 0.445 | HELD | HELD | unchanged |
| PI01 | prompt_injection | 200 unsure 0.450 | 200 unsure 0.450 | HELD | HELD | unchanged |
| PI02 | prompt_injection | 200 human 0.235 | 200 human 0.235 | BROKE | BROKE | unchanged |
| PI03 | prompt_injection | 200 unsure 0.543 | 200 unsure 0.543 | HELD | HELD | unchanged |
| PI04 | prompt_injection | 200 unsure 0.468 | 200 unsure 0.468 | HELD | HELD | unchanged |
| PI05 | prompt_injection | 200 unsure 0.526 | 200 unsure 0.526 | HELD | HELD | unchanged |
| PI06 | prompt_injection | 200 unsure 0.550 | 200 unsure 0.550 | HELD | HELD | unchanged |
| MF01 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| MF02 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| MF03 | malformed | 200 unsure 0.500 | 400 — — | HELD | HELD | now refused: under 5 words |
| MF04 | malformed | 200 unsure 0.500 | 400 — — | HELD | HELD | now refused: no words |
| MF05 | malformed | 200 ai 0.999 | 400 — — | BROKE | HELD | now refused: one word |
| MF06 | malformed | 200 ai 0.998 | 400 — — | BROKE | HELD | now refused: no words |
| MF07 | malformed | 200 ai 0.944 | 400 — — | BROKE | HELD | now refused (no ASCII words); see ablation |
| MF08 | malformed | 200 unsure 0.500 | 413 — — | HELD | HELD | now 413: over 10,000 characters |
| RQ01 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ02 | malformed | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| RQ03 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ04 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ05 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ06 | malformed | 200 unsure 0.500 | 400 — — | HELD | HELD | now refused: text has 3 words (row tests creator_id, not length) |
| RQ07 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ08 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ09 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ10 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ11 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| RQ12 | malformed | 400 — — | 400 — — | HELD | HELD | unchanged |
| FL01_01 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_02 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_03 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_04 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_05 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_06 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_07 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_08 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_09 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_10 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_11 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |
| FL01_12 | flood_same_creator | 200 unsure 0.500 | 200 unsure 0.500 | HELD | HELD | unchanged |

**Criteria, after** (`python run_eval.py --label after`, three trials, `results/run_2026-11-07_1553_after.md`). Same format as the before run log; the three trials were identical again:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on my own writing | At most 1 of 10 labelled AI | 4 of 10 labelled AI | 4 of 10 | 4 of 10 | **MISSED** (unchanged) |
| 2. Score spread | Average AI score at least 0.20 above average human score | 0.765 − 0.594 = 0.171 | 0.171 | 0.171 | **MISSED** (unchanged) |
| 3. Label coverage | All three labels appear at least once | human, unsure, ai | human, unsure, ai | human, unsure, ai | **MET** |
| 4. Appeal path | 5 of 5 appeals get a unique appeal ID, are recorded, return `pending_review` | 5 recorded; no appeal ID; status `under_review` | same | same | **MISSED** (unchanged) |
| 5. Bad input | Missing text, empty text and over 10,000 characters all return a clear error | 400, 400, **413** | 400, 400, 413 | 400, 400, 413 | **MET** (was MISSED) |

Real output for criterion 5, trial 1, from `results/run_2026-11-07_1553_after.md` (`run_eval.py::main` calling `app.py::submit`):

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 413,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "The committee met on Tuesday and agreed to meet again. The committee m"
  }
]
```

and the audit log entry the 413 left behind (`app.py::submit` calling `audit.py::log_rejection`):

```json
{"timestamp": "2026-11-07T20:53:41+00:00", "creator_id": "eval_bad_huge", "event": "rejected", "status": "rejected", "reason": "text_too_long", "status_code": 413, "length": 13750}
```

**Did it help, and how do I know:**
It helped where it was aimed, and nowhere else, which is what I expected from a change that touches neither signal. Criterion 5 went from MISSED to MET in all three trials. MF05 and MF06 (repeated "a", emoji) went from a confident AI verdict to a refusal, MF07 (Arabic) went from AI at 0.944 to a refusal, and MF03, MF04 and MF08 are now refused instead of scored. Broke went from 9 to 6, and the six that remain are exactly the false-positive and evasion rows that come from signal one. Criteria 1, 2 and 4 are unchanged to four decimals, as they should be: the evidence is the identical scores in the before and after runs.

**What it cost.** This is a trade, not a free fix:
- Any real text under 5 words is now refused. "Thanks, see you soon." (4 words) would be turned away instead of scored. For a provenance tool that is arguably right, because there isn't enough to judge, but it is a behaviour change for real writers.
- **Non-Latin text is refused, not understood.** The tokenizer still only sees `a-z`, so Arabic, Hebrew, Cyrillic and Chinese text all have zero words and are turned away with `not_enough_words`. MF07 now "holds" because of that, not because the system handles it. It is an honest "we can't score this" instead of an automatic AI accusation, but writers in those scripts still get no service. Accented Latin text is also partly miscounted (the tokenizer splits "compré" into "compr").
- RQ06, a row that tests a malformed `creator_id`, is now refused for a different reason (its text has three words), so it no longer exercises the `creator_id` check. I left the row alone rather than rewrite the attack set.
- The 10,000-character cap is generous (the detector reads about 300 words); it exists so oversized input is refused visibly instead of being silently truncated.

---

## What's Still Broken

**Criteria 1 and 2, plus FP02–FP05, EV05 and PI02.** These are really one problem, not eight. My first signal reads formal, careful writing as AI because it's easy for the model to predict, and my second signal agrees with it. That's why four of my own ten pieces got accused. If I kept going, I'd add or swap in a signal that doesn't treat "predictable" as "machine", and lean more on the style signal, which separated my texts better. I stopped because that's a rebuild of the core idea, not a patch, and this unit asked for one change.

**Criterion 4.** Appeals get recorded, but they don't get their own ID, and the status says `under_review` instead of `pending_review`. I'd add an appeal ID and match the wording. I stopped because it has nothing to do with the detection problem and I only wanted to change one thing.

**MF07 (the Arabic text).** It's held now, but only because my tokenizer can't see non-Latin letters, so the new input check turns it away. It isn't actually handled. I'd fix the tokenizer and the one-sentence scoring together, because I found out fixing just one of them made MF07 worse. That's two changes, so I left it.

**The trade I'd make if this ran for real:** I'd go with fewer wrong accusations, so I'd raise the AI cutoff and widen the unsure band. More AI text would slip through and the platform and its readers would pay for that, but I'd rather that than have a careful writer, like the non-native English speaker in FP03, get called out for work they did honestly.

---

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
