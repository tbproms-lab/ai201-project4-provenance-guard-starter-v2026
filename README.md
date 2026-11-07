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

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
