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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
