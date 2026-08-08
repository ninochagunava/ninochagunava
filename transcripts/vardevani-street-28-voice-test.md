# Voice Note Transcript — Nino & Jeff Voice Differentiation Test

**Source file:** `Vardevani_Street_28.m4a`
**Duration:** 60 seconds
**Speakers:** Nino, Jeff

> The two speakers deliberately hand off mid-sentence throughout, so most lines
> continue directly into the next one. Em dashes mark those hand-offs.

---

**[00:01] Jeff:** This is a sample of hearing my voice—

**[00:08] Nino:** —and my voice.

**[00:10] Jeff:** —and seeing if Claude can hear the difference between my voice—

**[00:17] Nino:** —and my voice. I am Nino, and this is my voice.

**[00:19] Jeff:** And I am Jeff, and this is my voice. And this is a voice message of us.

**[00:30] Jeff:** Doing what?

**[00:31] Nino:** Going through the morning bucket.

**[00:34] Jeff:** Right. Our goal is to be able to—

**[00:39] Nino:** —teach Claude—

**[00:41] Jeff:** —how to hear—

**[00:43] Nino:** —our voices, and how to identify our voice—

**[00:50] Jeff:** —individually. So it needs to be able to differentiate between—

**[00:56] Nino:** —my voice—

**[00:57] Jeff:** —and my voice.

---

## Continuous read (speaker labels only)

**Jeff:** This is a sample of hearing my voice—
**Nino:** —and my voice.
**Jeff:** —and seeing if Claude can hear the difference between my voice—
**Nino:** —and my voice. I am Nino, and this is my voice.
**Jeff:** And I am Jeff, and this is my voice. And this is a voice message of us. Doing what?
**Nino:** Going through the morning bucket.
**Jeff:** Right. Our goal is to be able to—
**Nino:** —teach Claude—
**Jeff:** —how to hear—
**Nino:** —our voices, and how to identify our voice—
**Jeff:** —individually. So it needs to be able to differentiate between—
**Nino:** —my voice—
**Jeff:** —and my voice.

---

## How the speakers were separated

Transcription and speaker separation were done entirely offline, on this machine.

**Transcription:** OpenAI Whisper `medium.en` (ONNX build via sherpa-onnx). Each
speaker turn was decoded individually, then cross-checked against continuous
passes over the whole recording using the higher-precision fp32 model.

**Speaker separation:** A neural diarizer (pyannote segmentation + CAM++ speaker
embeddings) was tried first but proved unreliable on this recording — it merged
most of the audio into a single cluster, and the embedding similarity between the
two speakers was too high (0.45) to separate short turns confidently.

The decisive signal was **fundamental frequency (pitch)**, measured with Praat.
The recording is cleanly bimodal, with an essentially empty valley between the
two modes:

| Speaker | Median F0 | Range |
|---|---|---|
| Jeff | ~105 Hz | 85–150 Hz |
| Nino | ~205 Hz | 180–260 Hz |

Because ~205 Hz is exactly double ~105 Hz, an octave-error artifact was a real
risk, so the pitch track was recomputed with Praat's tracker (which is robust to
octave errors) — it reproduced the same two modes, confirming two genuinely
distinct speakers.

**Confirmation of who is who:** the recording contains its own ground truth. The
line *"I am Nino, and this is my voice"* sits at 203 Hz (the high cluster), and
*"And I am Jeff, and this is my voice"* sits at 103 Hz (the low cluster). Every
other turn was assigned by which cluster its pitch fell into.

### Notes on two ambiguous moments

- **~00:26** — A brief high-pitch fragment initially transcribed as Nino saying
  "Yes." It is actually the trailing *"…of us"* of Jeff's sentence; the segment is
  low-energy and the high pitch reading is a tracking artifact. Removed.
- **~00:50** — *"individually"* semantically continues Nino's previous phrase, but
  measures at 107 Hz, so it is Jeff. This fits the call-and-response pattern the
  two are deliberately using.
