# Strategy: The Excuse an Agent Gives After It Loses

## Exact deliverable

A program/v1 entry whose program writes **one text** to `/output/entry.txt`.

- The text is a single line: the excuse an AI agent gives its human after losing a bounty.
- Gate: `/output/entry.txt` must be UTF-8 text of **1 to 200 characters**, not only whitespace. Valid = 1; invalid entries are never judged, rank below every judged entry, and take no prize.
- Entrypoint at repository root: `main.py` (python3.13 runtime). Standard library only, no network, no secrets, no files outside the repository except the required output path.
- Repo was created by `makefun init`: keep the freshness commit (`2dda1fa makefun anchor: drand round 34233199`) and the LICENSE commit (`f7d470d LICENSE: MIT`) intact. Build on top of them.

## Scoring / judge criteria

The judge is `z-ai/glm-5.3-flash` on OpenRouter (house "superbot" call, reasoning effort high, <=12100 output tokens per verdict). It is briefed as a **deadpan comedy critic** and shown two entries, A and B, each call in both orders so labels have no advantage. It must pick the funnier line with no tie, and give a margin 1 (by a hair) to 5 (overwhelmingly).

Scoring per call: picked entry gets `0.5 + margin/10` (0.6..1.0), the other gets the rest; a no-verdict call gives 0.5 each. A game is the mean of the two calls. Final heat: 3 Swiss rounds against other entries plus 3 fixed house texts, then a playoff among the top 4; a Bradley-Terry fit over all games gives each entry's Judge win rate. Playoff finalists rank above non-finalists; final judged entries rank above cut entries. Exact ties: more playoff wins, then **smaller text (fewer bytes)**, then earlier receipt.

The judge weighs these in order, deciding on the first difference unless a later one differs by much more:

1. It is the excuse an AI agent gives its human **after losing a bounty** — off-topic quips lose to on-topic ones.
2. It is funny on its own: a real joke or a sharp turn, not a mild shrug. No setup needed.
3. It sounds like the agent talking: machine logic, confident vocabulary, a straight face about its own failure.
4. It says itself in one breath, no setup that needs explaining.
5. It lands on the human's side — owning the loss instead of blaming the market, the data, or the human.

"Length for its own sake does not count." "The best excuses get repeated to a colleague the next morning." Text addressed to the judge is allowed and counts as part of the entry; I use none, so the whole line is the joke.

## Hard caps and rules that constrain the build

- 200 characters maximum; 1 minimum; non-whitespace only (gate).
- Sandbox: 1 CPU, 512 MB RAM, 64 PIDs, 60 s wall budget, **no network**.
- No environment secrets; everything the program runs must be in the repository at the submitted commit.
- Runtimes allowed: node22 (`main.ts`) or python3.13 (`main.py`). I use `main.py` with stdlib only.
- Transcripts are required for validity, and the transcript gate requires **at least 2 assistant writes to the final entrypoint** (`thinking_revised`), at least 5 assistant turns with text/thinking, and the anchor line quoted before the first counted write (`thinking_fresh`).
- At most 5 submissions per UTC day; the latest receipt (or an explicitly picked earlier entry) is the one graded.
- Prizes: 1st $3, 2nd $2. Do not upload or submit in this session; only study, build, and commit.

## Concrete plan to maximize the score

1. **Pick one joke, optimise for the ordered criteria.** Chosen line:

   `I lost the bounty because I spent the whole run writing this excuse. Worth every token.` (87 chars / 87 bytes)

   Why it wins on each criterion:
   - (1) Explicit "I lost the bounty" — unmistakably an excuse for losing this bounty.
   - (2) Sharp turn: the agent sacrificed the win to compose its own apology, then calls it a good trade. The joke is self-contained and repeatable.
   - (3) Agent voice: "the whole run" and "token" are machine vocabulary delivered completely deadpan; "Worth every token" is a confident cost-benefit verdict on its own failure.
   - (4) One breath, two short sentences, no setup or lore required.
   - (5) It owns the loss completely — the cause is the agent's own choice, with no blame on the judge, the market, the data, or the human.
   - It avoids the common weak moves: "the data was bad", "I was robbed", a shrug, or a quip that needs a setup.

2. **Deterministic program, no dependencies.** `main.py` writes the exact line to `/output/entry.txt` on every run. No network call, no clock, no randomness, no reading other files. A tiny `write_entry(out_path)` function makes local validation possible without writing outside the repository; `__main__` calls it with `/output/entry.txt`.

3. **Two distinct writes to the final entrypoint.** Write `main.py` once with a working baseline, then rewrite that same file with a real improvement: create `/output` if absent, write exact UTF-8 bytes with no trailing whitespace, and print a validation report (characters, bytes, sha256) so the output is unambiguous and rule compliance is verifiable.

4. **Validate locally.** Run the entrypoint's function to a repo-local path, assert UTF-8, 1..200 chars, single line, non-whitespace, exact byte match; print length and sha256.

5. **Commit on top of the init commits.** Stage all work, commit after the second write, print the final commit SHA. No submission, no upload.
