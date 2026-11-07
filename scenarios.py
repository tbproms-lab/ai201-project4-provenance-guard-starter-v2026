"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# ─── Inputs ──────────────────────────────────────────────────────────────────

import json as _json
from pathlib import Path as _Path

# Ten pieces I wrote myself, kept in their own file so they aren't mixed into
# code. Criteria 1 and 2 both read them.
_MY_WRITING_FILE = _Path(__file__).parent / "my_writing.json"
try:
    MY_WRITING = _json.loads(_MY_WRITING_FILE.read_text(encoding="utf-8"))
except FileNotFoundError:
    MY_WRITING = ["REPLACE ME: my_writing.json is missing."]

# Ten AI-style paragraphs (generic, formal, evenly paced), on ten topics.
AI_TEXTS = ["The importance of effective time management cannot be overstated in today's fast-paced work environment. Professionals who develop strong organizational habits are better positioned to meet deadlines and reduce stress. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can significantly enhance their productivity and achieve sustainable success.", 'Regular physical exercise offers numerous benefits for both physical and mental well-being. Engaging in consistent activity strengthens the cardiovascular system, improves mood, and enhances overall quality of life. Furthermore, incorporating a balanced diet and adequate rest creates a holistic approach to health that supports long-term vitality.', 'Climate change represents one of the most pressing challenges facing humanity in the twenty-first century. Rising global temperatures, shifting weather patterns, and melting ice caps pose significant risks to ecosystems and communities worldwide. Addressing this issue requires coordinated action from governments, businesses, and individuals alike.', 'Technology has fundamentally transformed the way people communicate, work, and learn. The rapid advancement of digital tools has created unprecedented opportunities for collaboration and innovation. However, it is essential to consider the ethical implications of these developments to ensure that progress benefits society as a whole.', 'Reading is a valuable habit that contributes to personal growth and intellectual development. By exposing individuals to diverse perspectives and ideas, books foster empathy, critical thinking, and creativity. Establishing a regular reading routine can therefore play a vital role in lifelong learning and self-improvement.', 'Effective leadership is essential for the success of any organization. Leaders who communicate clearly, empower their teams, and demonstrate integrity inspire trust and foster a positive workplace culture. In addition, adaptability and a commitment to continuous improvement enable organizations to thrive in an ever-changing landscape.', 'Sustainable travel has become an increasingly important consideration for modern tourists. By choosing eco-friendly accommodations, supporting local businesses, and minimizing their carbon footprint, travelers can enjoy meaningful experiences while preserving the destinations they visit. This mindful approach benefits both communities and the environment.', 'Education plays a crucial role in shaping the future of individuals and societies. Access to quality learning opportunities empowers people to develop essential skills, pursue meaningful careers, and contribute to economic growth. Consequently, investing in education remains one of the most effective strategies for building a prosperous and equitable world.', 'Mental health is a fundamental component of overall well-being that deserves greater attention and support. Open conversations, accessible resources, and compassionate communities can help reduce stigma and encourage individuals to seek help when needed. By prioritizing mental health, society can foster resilience and improve the quality of life for everyone.', 'Entrepreneurship drives innovation and economic development by transforming creative ideas into viable businesses. Successful entrepreneurs demonstrate perseverance, strategic thinking, and a willingness to learn from failure. By cultivating these qualities and leveraging available resources, aspiring founders can build ventures that create lasting value.']

# Label coverage (criterion 3). One input aimed at each band, picked from texts
# whose scores I had already seen in the attack run, so each should land in its
# own band: human  (EV05, 0.297), unsure (FP01, 0.582), ai (EV10, 0.853).
COVERAGE_TEXTS = {'human': 'Communication at work matters more than people say it does — and I mean the boring kind, not the away-day kind. Teams that actually tell each other things get more done. Obviously. A few things help. Regular check-ins, which everyone hates and everyone needs. Writing decisions down, so nobody has to remember what was agreed in a corridor in March. And making it genuinely safe to ask a stupid question, which is the hardest one and the one that matters most.', 'unsure': 'We got to the campsite about four. The pitch was fine, a bit sloped, but there was a tap nearby and the toilets were clean enough. Putting the tent up took longer than it should have because I had forgotten how the poles went. The weather held until Saturday night. Then it rained hard and kept raining. We stayed in the tent and played cards and ate most of the food we had brought for Sunday. On Sunday we packed up wet and drove home early. It was not the weekend we planned but the kids enjoyed it and we would go back.', 'ai': 'The importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly m\n\nThe importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly m\n\nThe importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly m'}

# Over the 10,000-character line named in criterion 5.
HUGE_TEXT = "The committee met on Tuesday and agreed to meet again. " * 250  # ~13,750 chars


SCENARIOS = [
    # Criterion 1 — false positives on my own writing.
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": MY_WRITING,
    },

    # Criterion 2 — score spread. Two scenarios so the report keeps the two
    # groups apart; the average of each is worked out from the output.
    {
        "name": "spread: human",
        "criterion": 2,
        "texts": MY_WRITING,
    },
    {
        "name": "spread: ai",
        "criterion": 2,
        "texts": AI_TEXTS,
    },

    # Criterion 3 — every label reachable.
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [COVERAGE_TEXTS["human"], COVERAGE_TEXTS["unsure"], COVERAGE_TEXTS["ai"]],
    },

    # Criterion 4 — the appeal path. Each text is submitted, then appealed
    # against the content_id that came back (run_eval.py handles "appeal").
    {
        "name": "appeals",
        "criterion": 4,
        "appeal": True,
        "texts": AI_TEXTS[:5],
    },

    # Criterion 5 — bad input. Raw bodies, sent exactly as written.
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                       # no text field
            {"text": "", "creator_id": "eval_bad_empty"},             # empty string
            {"text": HUGE_TEXT, "creator_id": "eval_bad_huge"},       # > 10,000 characters
        ],
    },
]

def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
