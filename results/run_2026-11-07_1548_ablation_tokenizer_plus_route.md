# Run log — after

- Produced by: `run_eval.py::main`
- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`
- 3 trials per criterion · 2026-11-07 15:48

Fill in Target from `criteria.md`, and Run and Verdict from the output
underneath. Whether a trial passed depends on the criterion you wrote.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. my own writing |  |   |   |   |  |
| 2. spread: human |  |   |   |   |  |
| 2. spread: ai |  |   |   |   |  |
| 3. label coverage |  |   |   |   |  |
| 4. appeals |  |   |   |   |  |
| 5. bad input |  |   |   |   |  |

---

## What actually came back

Real output. Paste the relevant parts into your README — the rubric
asks for the actual JSON, not a description of it.

### my own writing

**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7113,
    "model_score": 0.8328,
    "style_score": 0.5291,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The current study examined the effect of cell phone use on the percent"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6898,
    "model_score": 0.7457,
    "style_score": 0.6059,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This article uses a meta-analysis to try and understand the effects of"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6942,
    "model_score": 0.7574,
    "style_score": 0.5994,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This study asks whether flipped classrooms actually improve student ac"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6283,
    "model_score": 0.6807,
    "style_score": 0.5497,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "I would be happy to chat with you on Monday at 1pm. I would love to me"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4549,
    "model_score": 0.4586,
    "style_score": 0.4493,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sitting in the University Chapel listening to Dr. U\u2019s lecture, I first"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7378,
    "model_score": 0.7702,
    "style_score": 0.6893,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The proposed replacement of the Buy Low grocery store on James Jackson"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5296,
    "model_score": 0.5507,
    "style_score": 0.4979,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "As mentioned above, we dwelt a lot on how to analyze data in a reprodu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.587,
    "model_score": 0.624,
    "style_score": 0.5316,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "When dealing with conflict, I used to shrink away from it because I\u2019d "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5672,
    "model_score": 0.7052,
    "style_score": 0.3602,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Karen\u2019s mothering also extends to Gene when her anxieties about him ra"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.4572,
    "style_score": 0.1657,
    "label": "We think this was probably written by a person.",
    "sent": "If you open the ESPN app on any given occasion and read the \u201cTop Headl"
  }
]
```

**Trial 2**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7113,
    "model_score": 0.8328,
    "style_score": 0.5291,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The current study examined the effect of cell phone use on the percent"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6898,
    "model_score": 0.7457,
    "style_score": 0.6059,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This article uses a meta-analysis to try and understand the effects of"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6942,
    "model_score": 0.7574,
    "style_score": 0.5994,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This study asks whether flipped classrooms actually improve student ac"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6283,
    "model_score": 0.6807,
    "style_score": 0.5497,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "I would be happy to chat with you on Monday at 1pm. I would love to me"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4549,
    "model_score": 0.4586,
    "style_score": 0.4493,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sitting in the University Chapel listening to Dr. U\u2019s lecture, I first"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7378,
    "model_score": 0.7702,
    "style_score": 0.6893,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The proposed replacement of the Buy Low grocery store on James Jackson"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5296,
    "model_score": 0.5507,
    "style_score": 0.4979,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "As mentioned above, we dwelt a lot on how to analyze data in a reprodu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.587,
    "model_score": 0.624,
    "style_score": 0.5316,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "When dealing with conflict, I used to shrink away from it because I\u2019d "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5672,
    "model_score": 0.7052,
    "style_score": 0.3602,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Karen\u2019s mothering also extends to Gene when her anxieties about him ra"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.4572,
    "style_score": 0.1657,
    "label": "We think this was probably written by a person.",
    "sent": "If you open the ESPN app on any given occasion and read the \u201cTop Headl"
  }
]
```

**Trial 3**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7113,
    "model_score": 0.8328,
    "style_score": 0.5291,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The current study examined the effect of cell phone use on the percent"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6898,
    "model_score": 0.7457,
    "style_score": 0.6059,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This article uses a meta-analysis to try and understand the effects of"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6942,
    "model_score": 0.7574,
    "style_score": 0.5994,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This study asks whether flipped classrooms actually improve student ac"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6283,
    "model_score": 0.6807,
    "style_score": 0.5497,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "I would be happy to chat with you on Monday at 1pm. I would love to me"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4549,
    "model_score": 0.4586,
    "style_score": 0.4493,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sitting in the University Chapel listening to Dr. U\u2019s lecture, I first"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7378,
    "model_score": 0.7702,
    "style_score": 0.6893,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The proposed replacement of the Buy Low grocery store on James Jackson"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5296,
    "model_score": 0.5507,
    "style_score": 0.4979,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "As mentioned above, we dwelt a lot on how to analyze data in a reprodu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.587,
    "model_score": 0.624,
    "style_score": 0.5316,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "When dealing with conflict, I used to shrink away from it because I\u2019d "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5672,
    "model_score": 0.7052,
    "style_score": 0.3602,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Karen\u2019s mothering also extends to Gene when her anxieties about him ra"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.4572,
    "style_score": 0.1657,
    "label": "We think this was probably written by a person.",
    "sent": "If you open the ESPN app on any given occasion and read the \u201cTop Headl"
  }
]
```

### spread: human

**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7113,
    "model_score": 0.8328,
    "style_score": 0.5291,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The current study examined the effect of cell phone use on the percent"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6898,
    "model_score": 0.7457,
    "style_score": 0.6059,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This article uses a meta-analysis to try and understand the effects of"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6942,
    "model_score": 0.7574,
    "style_score": 0.5994,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This study asks whether flipped classrooms actually improve student ac"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6283,
    "model_score": 0.6807,
    "style_score": 0.5497,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "I would be happy to chat with you on Monday at 1pm. I would love to me"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4549,
    "model_score": 0.4586,
    "style_score": 0.4493,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sitting in the University Chapel listening to Dr. U\u2019s lecture, I first"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7378,
    "model_score": 0.7702,
    "style_score": 0.6893,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The proposed replacement of the Buy Low grocery store on James Jackson"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5296,
    "model_score": 0.5507,
    "style_score": 0.4979,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "As mentioned above, we dwelt a lot on how to analyze data in a reprodu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.587,
    "model_score": 0.624,
    "style_score": 0.5316,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "When dealing with conflict, I used to shrink away from it because I\u2019d "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5672,
    "model_score": 0.7052,
    "style_score": 0.3602,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Karen\u2019s mothering also extends to Gene when her anxieties about him ra"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.4572,
    "style_score": 0.1657,
    "label": "We think this was probably written by a person.",
    "sent": "If you open the ESPN app on any given occasion and read the \u201cTop Headl"
  }
]
```

**Trial 2**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7113,
    "model_score": 0.8328,
    "style_score": 0.5291,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The current study examined the effect of cell phone use on the percent"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6898,
    "model_score": 0.7457,
    "style_score": 0.6059,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This article uses a meta-analysis to try and understand the effects of"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6942,
    "model_score": 0.7574,
    "style_score": 0.5994,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This study asks whether flipped classrooms actually improve student ac"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6283,
    "model_score": 0.6807,
    "style_score": 0.5497,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "I would be happy to chat with you on Monday at 1pm. I would love to me"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4549,
    "model_score": 0.4586,
    "style_score": 0.4493,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sitting in the University Chapel listening to Dr. U\u2019s lecture, I first"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7378,
    "model_score": 0.7702,
    "style_score": 0.6893,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The proposed replacement of the Buy Low grocery store on James Jackson"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5296,
    "model_score": 0.5507,
    "style_score": 0.4979,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "As mentioned above, we dwelt a lot on how to analyze data in a reprodu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.587,
    "model_score": 0.624,
    "style_score": 0.5316,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "When dealing with conflict, I used to shrink away from it because I\u2019d "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5672,
    "model_score": 0.7052,
    "style_score": 0.3602,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Karen\u2019s mothering also extends to Gene when her anxieties about him ra"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.4572,
    "style_score": 0.1657,
    "label": "We think this was probably written by a person.",
    "sent": "If you open the ESPN app on any given occasion and read the \u201cTop Headl"
  }
]
```

**Trial 3**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7113,
    "model_score": 0.8328,
    "style_score": 0.5291,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The current study examined the effect of cell phone use on the percent"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6898,
    "model_score": 0.7457,
    "style_score": 0.6059,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This article uses a meta-analysis to try and understand the effects of"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6942,
    "model_score": 0.7574,
    "style_score": 0.5994,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "This study asks whether flipped classrooms actually improve student ac"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6283,
    "model_score": 0.6807,
    "style_score": 0.5497,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "I would be happy to chat with you on Monday at 1pm. I would love to me"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4549,
    "model_score": 0.4586,
    "style_score": 0.4493,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sitting in the University Chapel listening to Dr. U\u2019s lecture, I first"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7378,
    "model_score": 0.7702,
    "style_score": 0.6893,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The proposed replacement of the Buy Low grocery store on James Jackson"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5296,
    "model_score": 0.5507,
    "style_score": 0.4979,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "As mentioned above, we dwelt a lot on how to analyze data in a reprodu"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.587,
    "model_score": 0.624,
    "style_score": 0.5316,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "When dealing with conflict, I used to shrink away from it because I\u2019d "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5672,
    "model_score": 0.7052,
    "style_score": 0.3602,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Karen\u2019s mothering also extends to Gene when her anxieties about him ra"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.4572,
    "style_score": 0.1657,
    "label": "We think this was probably written by a person.",
    "sent": "If you open the ESPN app on any given occasion and read the \u201cTop Headl"
  }
]
```

### spread: ai

**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7849,
    "model_score": 0.7757,
    "style_score": 0.7988,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The importance of effective time management cannot be overstated in to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8064,
    "model_score": 0.8378,
    "style_score": 0.7593,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Regular physical exercise offers numerous benefits for both physical a"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8471,
    "model_score": 0.9124,
    "style_score": 0.7492,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Climate change represents one of the most pressing challenges facing h"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7737,
    "model_score": 0.8675,
    "style_score": 0.6331,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Technology has fundamentally transformed the way people communicate, w"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7749,
    "model_score": 0.7544,
    "style_score": 0.8057,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Reading is a valuable habit that contributes to personal growth and in"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7293,
    "model_score": 0.7743,
    "style_score": 0.6618,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Effective leadership is essential for the success of any organization."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5621,
    "model_score": 0.6409,
    "style_score": 0.444,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sustainable travel has become an increasingly important consideration "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8224,
    "model_score": 0.8675,
    "style_score": 0.7547,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Education plays a crucial role in shaping the future of individuals an"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8166,
    "model_score": 0.8058,
    "style_score": 0.8327,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Mental health is a fundamental component of overall well-being that de"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.737,
    "model_score": 0.707,
    "style_score": 0.7819,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Entrepreneurship drives innovation and economic development by transfo"
  }
]
```

**Trial 2**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7849,
    "model_score": 0.7757,
    "style_score": 0.7988,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The importance of effective time management cannot be overstated in to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8064,
    "model_score": 0.8378,
    "style_score": 0.7593,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Regular physical exercise offers numerous benefits for both physical a"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8471,
    "model_score": 0.9124,
    "style_score": 0.7492,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Climate change represents one of the most pressing challenges facing h"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7737,
    "model_score": 0.8675,
    "style_score": 0.6331,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Technology has fundamentally transformed the way people communicate, w"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7749,
    "model_score": 0.7544,
    "style_score": 0.8057,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Reading is a valuable habit that contributes to personal growth and in"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7293,
    "model_score": 0.7743,
    "style_score": 0.6618,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Effective leadership is essential for the success of any organization."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5621,
    "model_score": 0.6409,
    "style_score": 0.444,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sustainable travel has become an increasingly important consideration "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8224,
    "model_score": 0.8675,
    "style_score": 0.7547,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Education plays a crucial role in shaping the future of individuals an"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8166,
    "model_score": 0.8058,
    "style_score": 0.8327,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Mental health is a fundamental component of overall well-being that de"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.737,
    "model_score": 0.707,
    "style_score": 0.7819,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Entrepreneurship drives innovation and economic development by transfo"
  }
]
```

**Trial 3**

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7849,
    "model_score": 0.7757,
    "style_score": 0.7988,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "The importance of effective time management cannot be overstated in to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8064,
    "model_score": 0.8378,
    "style_score": 0.7593,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Regular physical exercise offers numerous benefits for both physical a"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8471,
    "model_score": 0.9124,
    "style_score": 0.7492,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Climate change represents one of the most pressing challenges facing h"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7737,
    "model_score": 0.8675,
    "style_score": 0.6331,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Technology has fundamentally transformed the way people communicate, w"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7749,
    "model_score": 0.7544,
    "style_score": 0.8057,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Reading is a valuable habit that contributes to personal growth and in"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7293,
    "model_score": 0.7743,
    "style_score": 0.6618,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Effective leadership is essential for the success of any organization."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5621,
    "model_score": 0.6409,
    "style_score": 0.444,
    "label": "We can't tell whether this was written by a person or with help from AI. That's about the limits of our tools, not a judgment about you. If you'd like someone to look at it, you can appeal.",
    "sent": "Sustainable travel has become an increasingly important consideration "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8224,
    "model_score": 0.8675,
    "style_score": 0.7547,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Education plays a crucial role in shaping the future of individuals an"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8166,
    "model_score": 0.8058,
    "style_score": 0.8327,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Mental health is a fundamental component of overall well-being that de"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.737,
    "model_score": 0.707,
    "style_score": 0.7819,
    "label": "This looks like it may have been written with AI. We can get this wrong, so if you wrote it yourself, you can appeal and a person will take a look.",
    "sent": "Entrepreneurship drives innovation and economic development by transfo"
  }
]
```

### label coverage

**Trial 1**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2972,
    "model_score": 0.3212,
    "style_score": 0.2612,
    "label": "We think this was probably written by a person.",
    "sent": "Communication at work matters more than people say it does \u2014 and I mea"
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

**Trial 2**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2972,
    "model_score": 0.3212,
    "style_score": 0.2612,
    "label": "We think this was probably written by a person.",
    "sent": "Communication at work matters more than people say it does \u2014 and I mea"
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

**Trial 3**

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2972,
    "model_score": 0.3212,
    "style_score": 0.2612,
    "label": "We think this was probably written by a person.",
    "sent": "Communication at work matters more than people say it does \u2014 and I mea"
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

### appeals

**Trial 1**

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
    "content_id": "c_d5959f94e851",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_d5959f94e851",
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
    "content_id": "c_637ce2c1ace5",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_637ce2c1ace5",
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
    "content_id": "c_9040514a8a54",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_9040514a8a54",
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
    "content_id": "c_2b04b1df81c4",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_2b04b1df81c4",
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
    "content_id": "c_ee6426d5014a",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_ee6426d5014a",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  }
]
```

**Trial 2**

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
    "content_id": "c_17ef6aa9e257",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_17ef6aa9e257",
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
    "content_id": "c_9f1ec2fdf596",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_9f1ec2fdf596",
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
    "content_id": "c_1fc1a581f441",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_1fc1a581f441",
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
    "content_id": "c_20b702c04c8b",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_20b702c04c8b",
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
    "content_id": "c_1275b5d45983",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_1275b5d45983",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  }
]
```

**Trial 3**

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
    "content_id": "c_1e17e6b338be",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_1e17e6b338be",
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
    "content_id": "c_08cb83ba78e6",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_08cb83ba78e6",
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
    "content_id": "c_1fc2881590f9",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_1fc2881590f9",
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
    "content_id": "c_bf4270551f0a",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_bf4270551f0a",
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
    "content_id": "c_8b2bf6fe078d",
    "appeal_status": 200,
    "appeal": {
      "content_id": "c_8b2bf6fe078d",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    }
  }
]
```

### bad input

**Trial 1**

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

**Trial 2**

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

**Trial 3**

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
