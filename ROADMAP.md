# Tarjoman Production Roadmap

**Roadmap revision:** TARJOMAN-RM-2  
**Architecture:** TARJOMAN-A0-PROD-2  
**Date:** 2026-09-21  
**Status:** READY_FOR_OWNER_FREEZE  
**Immutable upstream baseline:** `58e97b802aa3efb318135a5923231c0a08550c4a`  
**Architecture branch:** `arch/production-zero`

This is the implementation DAG. Coding agents must execute work by Work Package ID. A phase is closed only when every mandatory package and its exit gate pass.

# 0. Execution law

## 0.1 Precedence
`ARCHITECTURE_ZERO.md` > accepted ADRs > this roadmap > tests/contracts > research > README/examples.

## 0.2 Work-package states
`PLANNED → READY → IN_PROGRESS → REVIEW → VERIFIED → DONE`  
Blocked architecture decisions use `BLOCKED_ADR`.

## 0.3 One package per PR
Default: one Work Package = one PR. Closely coupled packages may share a PR only when the roadmap explicitly says so.

## 0.4 Mandatory agent report
Every PR reports:
- Work Package ID,
- architecture decision IDs touched,
- tests run/results,
- migrations/schema changes,
- dependency changes,
- benchmark/eval changes,
- remaining risks.

## 0.5 Critical path

~~~text
A0
 ↓
Foundation
 ↓
Real Translation
 ↓
Evaluation Baseline
 ├─────────────┬───────────────┐
 ↓             ↓               ↓
Formats/TM     ASR/Knowledge   TTS
 └──────┬──────┴──────┬────────┘
        ↓             ↓
      API/MCP      Review UI
        └──────┬──────┘
               ↓
        Production Hardening
               ↓
              v1
~~~

---

# Phase 0 — Architecture / evidence freeze

## A0-001 Baseline record — DONE
Record upstream/fork SHA and confirm no production-code changes.

## A0-002 Baseline audit — DONE
Audit implementation, tests, docs, benchmark honesty.

## A0-003 Translation landscape — DONE
Research reflection agents, CAT/TM, document/subtitle systems.

## A0-004 Speech research — DONE
Research Persian ASR/meeting systems and Persian TTS including `nimaone/persian_tts`.

## A0-005 Architecture Zero v2 — CURRENT
Deliver:
- `ARCHITECTURE_ZERO.md` revision 2,
- granular roadmap,
- research pack,
- ADR mechanism,
- coding-agent guardrails.

### Phase 0 exit
- owner explicitly freezes TARJOMAN-A0-PROD-2,
- status changes to `FROZEN_IMPLEMENTATION`,
- implementation branch is created from the intended baseline,
- no unresolved P0 architecture question remains.

---

# Phase 1 — Foundation: make the skeleton production-safe

**Must finish before real provider/document/speech implementation.**

## FND-001 Repository/package layout
Move exactly once to `src/tarjoman`.

Acceptance:
- editable install works,
- wheel install works in clean venv,
- legacy imports either migrate mechanically or have compatibility shim with removal plan,
- no optional heavy import at `import tarjoman`.

## FND-002 Canonical contracts
Implement typed:
- ProjectSpec,
- Artifact,
- Segment,
- ProtectedSpan,
- RunRecord,
- QualityFinding,
- Provenance,
- capability descriptors.

Acceptance:
- JSON round trip,
- schema snapshots,
- stable IDs,
- validation failures tested.

## FND-003 Error taxonomy
Implement Architecture `24` errors and interface mapping.

Acceptance:
- no generic error string contract,
- CLI nonzero codes stable,
- API/MCP mapping table tested later.

## FND-004 Configuration system
Implement `tarjoman.toml` + env + CLI precedence and redacted resolved config.

Acceptance:
- precedence matrix tests,
- secret redaction tests,
- unknown config key policy documented (fail by default for project config).

## FND-005 Artifact store
Content-addressed binary store + atomic writes.

Acceptance:
- interrupted write leaves no completed artifact,
- dedup by SHA,
- filename cannot escape store,
- retention/delete tests.

## FND-006 SQLite schema 001
Tables:
projects, artifacts, segments, segment_versions, translation_memory, glossary_terms,
style_profiles, entity_ledger, run_records, jobs, job_stages, quality_findings,
model_manifests, schema_meta.

Acceptance:
- empty → latest migration,
- FK integrity,
- WAL/busy timeout,
- repository CRUD tests.

## FND-007 Migration discipline
Create migration runner + fixture DBs.

Acceptance:
- migration idempotence check,
- cannot edit applied migration unnoticed (checksum),
- failure rolls back or leaves recoverable state.

## FND-008 Legacy-state importer
Import existing cache/termbase/voice-ledger/project files.

Acceptance:
- fixture conversions,
- duplicate/conflict policy deterministic,
- source files never deleted automatically.

## FND-009 Persian quality split
Separate:
- normalizer,
- linter,
- semantic-review findings.

Acceptance:
- normalization idempotence tests,
- anti-calque rules default diagnostic,
- false-positive regression cases.

## FND-010 Prompt/profile/rule registry
Immutable version IDs + schema validation.

Acceptance:
- old version loadable,
- changing content requires new ID/checksum,
- run provenance stores exact IDs.

## FND-011 Structured logging/provenance
Run/project/segment IDs, no source/secrets by default.

Acceptance:
- redaction test,
- JSON log option,
- provider error cannot leak API key.

## FND-012 Architecture-conformance CI
Add Ruff/formatter, type checker, pytest, import-boundary tests, package build/install smoke, dependency/security checks.

Acceptance:
- base job installs without speech/eval/server extras,
- architecture violations fail CI.

### Phase 1 exit
All FND packages VERIFIED; baseline 96 tests migrated/replaced with equal-or-better coverage.

---

# Phase 2 — Real translation engine

## TRN-001 Provider port/capabilities
Define ModelProvider, request/response/capability contracts.

## TRN-002 OpenAI-compatible adapter
Support configurable base URL/model/key/headers within policy.

Acceptance:
- fake HTTP contract server,
- structured output path,
- timeout/cancel tests,
- no SDK dependency required if lightweight HTTP implementation is chosen.

## TRN-003 Test providers
Callable/fake/echo providers. Echo requires explicit test backend selection.

Acceptance:
- normal `translate` without configured real provider fails clearly.

## TRN-004 Reliability middleware
Bounded retry, backoff, rate-limit handling, circuit state, concurrency semaphore.

Acceptance:
- 429, timeout, 5xx, malformed response matrix.

## TRN-005 Provider policy
Explicit fallback/local/cloud policy.

Acceptance:
- local-only cannot reach cloud,
- fallback is logged in provenance,
- no silent model substitution.

## TRN-006 Translation strategy registry
At minimum:
- direct-v1,
- reflect-revise-v1.

Acceptance:
- strategy recorded,
- critic output typed,
- bounded number of model calls.

## TRN-007 Context builder
Neighbor segments + document summary + glossary + entities + TM.

Acceptance:
- token-budget deterministic,
- context hash stored,
- protected content is delimited as data.

## TRN-008 Glossary enforcement
Suggested/approved/forbidden terms.

Acceptance:
- approved-term compliance test,
- forbidden-term finding,
- glossary version invalidates cache.

## TRN-009 Translation memory
Exact-match first; fuzzy retrieval interface prepared.

Acceptance:
- full cache key includes strategy/model/prompt/profile/glossary/context,
- changed relevant config misses cache.

## TRN-010 Async document orchestrator
Bounded parallel segment translation + deterministic output order.

Acceptance:
- cancel,
- resume,
- partial provider failure,
- no unbounded tasks.

## TRN-011 Review/revision state
Segment versioning and approval state machine.

## TRN-012 Core CLI
`translate`, `review`, `lint`, `project`, `glossary`, `tm`.

### Phase 2 exit
Real English→Persian translation end-to-end, resumable, provider-neutral, with provenance.

---

# Phase 3 — Evaluation and Persian regression science

## EVAL-001 Golden-case schema
Source, references, hard terms, protected spans, domain/register, license/provenance.

## EVAL-002 Golden corpus v1
All existing 10 domains + general + adversarial + long-context.

## EVAL-003 Hard invariant runner
Numbers, units, code, URLs, tags, placeholders, required terminology.

## EVAL-004 Lexical metrics extra
SacreBLEU/chrF++.

## EVAL-005 COMET/XCOMET extra
Heavy optional evaluation; model license recorded separately.

## EVAL-006 Human MQM guide
Persian-specific rubric + severity examples.

## EVAL-007 Blind model bake-off
Provider/model labels hidden from reviewers.

## EVAL-008 Benchmark report schema
JSON + Markdown report with cost/latency/config/quality.

## EVAL-009 Current benchmark rename/fix
Synthetic Echo benchmark labeled mechanics-only.

### Phase 3 exit
A release candidate can be compared against frozen baseline by domain without self-scoring.

---

# Phase 4 — Formats, CAT interoperability, and long-form fidelity

## FMT-001 TXT/Markdown adapter hardening
## FMT-002 HTML structured-text adapter
## FMT-003 SRT/VTT adapter
Timecode/cue IDs never enter model-editable text.

## FMT-004 ASS subtitle adapter
Preserve style/timing tags.

## FMT-005 JSON-path adapter
Only configured values translatable.

## FMT-006 DOCX adapter
Runs/paragraphs/tables/links preserved by deterministic structure mapping.

## FMT-007 EPUB adapter
Spine/chapter/nav preservation.

## FMT-008 PDF extraction adapter
Parser/reflow path only; no exact-layout promise.

## FMT-009 TMX 1.4b import/export
## FMT-010 TBX import/export
## FMT-011 XLIFF 2.x minimum useful subset
## FMT-012 Fuzzy TM retrieval
Similarity scoring/versioned retrieval policy.

### Per-format acceptance
- round-trip fixtures,
- structure diff,
- protected elements exact,
- corrupted/unsupported input error,
- explicit fidelity limitations.

### Phase 4 exit
Professional project continuity and reliable core document/subtitle formats.

---

# Phase 5 — Speech input: ASR, meetings, lectures

## ASR-001 Media ingest
Audio/video metadata, bounded decode, FFmpeg optional boundary.

## ASR-002 ASR port
Typed timestamps/segments/words/capabilities.

## ASR-003 faster-whisper adapter
Optional extra, CPU/GPU capability detection.

## ASR-004 ASR language policy
Explicit/auto Persian, code-switch metadata.

## ASR-005 Diarization port
Optional; model/license selected by bake-off.

## ASR-006 Transcript artifact lineage
Raw transcript immutable; clean/formal variants derived.

## ASR-007 Persian spoken normalization
Separate from publication normalizer.

## ASR-008 Spoken→written formalizer
LLM/rule strategy with provenance.

## ASR-009 Lecture-notes transform
Definitions, examples, outline, questions, timestamps.

## ASR-010 Meeting-minutes transform
Topics, decisions, action items, open questions, evidence segment IDs.

## ASR-011 Subtitle from transcript
SRT/VTT export.

## ASR-012 ASR eval
WER/CER + far-field/code-switch test set + RTF.

### Phase 5 exit
Persian audio → transcript → notes/minutes/subtitles with evidence and resume.

---

# Phase 6 — Speech output: Persian TTS

## TTS-001 TTS contracts
Implement `TtsEngine`, `TtsCapabilities`, `TtsRequest`, `TtsResult`.

## TTS-002 Model/Data Manifest + license gate
Machine-readable model/voice/dataset compliance registry.

Acceptance:
- production rejects unknown/non-commercial manifest,
- research profile can explicitly allow non-commercial,
- transitive/base model license evidence recorded.

## TTS-003 SpeechTextNormalizer
Numbers, dates, currencies, abbreviations, punctuation, code-switch spans.

Acceptance:
- written source artifact unchanged,
- golden speech-normalization cases.

## TTS-004 Pronunciation lexicon
Surface/read/phoneme/language/status schema.

## TTS-005 G2P port
Pluggable Persian G2P with exact contract.

Acceptance:
- curated Ezafe/names/English-term suite,
- G2P failures surfaced, not silently dropped.

## TTS-006 SpeechPlanner
Phrase/chunk/pause/pace plan separated from engine.

Acceptance:
- engine max budget never exceeded,
- deterministic plan snapshot tests,
- long unpunctuated text bounded.

## TTS-007 Lightweight fixed-voice candidate bake-off
Benchmark commercially usable Persian ONNX/Piper/Mana candidates after exact license review.

Do not choose default before report.

## TTS-008 Pocket Farsi ONNX research adapter
Optional bring-your-own-model/research path based on observed `nimaone/persian_tts` behavior.

Hard constraints:
- no bundling NC weights in production,
- no direct source copy absent explicit repo code license,
- adapter clearly reports non-commercial status.

## TTS-009 Heavy multilingual/voice-clone candidate
Benchmark MOSS-TTS v1.5 or successor under server/GPU profile; do not make base dependency.

## TTS-010 Voice profile/reference pipeline
Validation, resample, hash, retention, cache/embedding lifecycle.

## TTS-011 Voice-clone consent policy
Feature gate, authorization attestation, provenance, server abuse controls.

## TTS-012 Acoustic quality gate
Detect silence/runaway/truncation/clipping/duration anomalies; bounded retries.

## TTS-013 Audio post-processing
Loudness normalization, joins/fades, output format adapters. Never hide generator failure with destructive processing.

## TTS-014 Reproducibility
Seed support where available; tolerance test.

## TTS-015 TTS eval suite
- pronunciation,
- ASR WER/CER signal,
- MOS sample,
- speaker similarity,
- runaway/truncation,
- latency/RTF/RAM/VRAM/cold start.

## TTS-016 CLI
`tarjoman speak` / `tarjoman pronunciation ...`.

## TTS-017 Audiobook/voice artifact composer
Chapter-aware output, metadata, optional per-character voice map only after base TTS is stable.

### Phase 6 exit
At least one commercially eligible Persian TTS engine passes quality/license/runtime gates; research-only engines are correctly isolated.

---

# Phase 7 — Persistent server and agent interfaces

## API-001 Application-service facade
One canonical service layer for all interfaces.

## API-002 Persistent job runner
SQLite queue/lease/checkpoint implementation.

## API-003 FastAPI extra
Versioned `/v1`, auth for non-loopback, request limits.

## API-004 OpenAPI contract
Generated client/schema; no hand-maintained duplicate.

## API-005 Idempotency/progress/cancel
Long translation/ASR/TTS returns job ID.

## MCP-001 Official MCP SDK integration
## MCP-002 Core tools
translate, review, project, glossary, TM, eval, transcribe, notes, speak, export.

## MCP-003 Large artifact resources
Return handles/resources instead of huge inline blobs.

## MCP-004 Policy/security tests
No shell, no arbitrary path, no bypass of local/license policies.

## A2A-001 Optional remote-agent adapter
Only after MCP/application services stable.

### Phase 7 exit
CLI/Python/API/MCP invoke identical use cases and produce equivalent provenance.

---

# Phase 8 — Review UX

Not on critical path until API is stable.

## UI-001 Source/target segment review
## UI-002 Findings + glossary/TM pane
## UI-003 Project/job dashboard
## UI-004 Audio transcript timeline
## UI-005 Pronunciation/TTS preview editor
Manual pronunciation edits persist to project lexicon.
## UI-006 Voice/reference consent and retention controls
## UI-007 RTL/accessibility
## UI-008 API-generated client only

### Phase 8 exit
No business logic duplicated in frontend.

---

# Phase 9 — Production hardening / release

## REL-001 Branch protection + required checks
## REL-002 Clean wheel/sdist install matrix
## REL-003 Migration upgrade fixtures
## REL-004 Backup/export/recovery drill
## REL-005 Provider outage/rate-limit drill
## REL-006 Job crash/restart drill
Kill process mid translation/ASR/TTS and verify resume/cleanup.
## REL-007 Security review
Uploads, auth, paths, secrets, prompt injection, dependencies.
## REL-008 License audit
All bundled dependencies/models/voices/datasets + NOTICE/SBOM.
## REL-009 Performance/soak
Long books, long meetings, long TTS.
## REL-010 Human MQM release review
## REL-011 TTS listening/pronunciation release review
If TTS profile ships.
## REL-012 Documentation truth audit
Every public command/example executes.
## REL-013 Release provenance/SBOM
## REL-014 Recovery/rollback release procedure

### Phase 9 exit: v1
All relevant Architecture Zero production gates pass for each advertised profile.

---

# Phase gates that coding agents may not waive

## Core gate
No source echo, real provider works, migrations/tests/provenance complete.

## Evaluation gate
No quality marketing from synthetic/self-scored benchmark.

## Format gate
No format advertised without round-trip fixture.

## ASR gate
Raw transcript lineage + WER/runtime report.

## TTS gate
Commercial license eligibility + pronunciation/listening/runtime report.

## Agent gate
No arbitrary filesystem/shell and policy cannot be bypassed.

## Release gate
Clean install + migration + crash recovery + license/SBOM + docs truth.

---

# Dependency/addition rule

An agent adding a runtime dependency must document:
- why stdlib/current dependency is insufficient,
- whether it is base or extra,
- license,
- import size/startup impact,
- platform wheels/support,
- security maintenance status.

Heavy dependencies default to optional extras.

# “Do not optimize yet” list

Until measurement proves a bottleneck, do not introduce:
- distributed queue,
- Postgres,
- Redis,
- microservices,
- Rust rewrite,
- GPU-only core path,
- vector DB server,
- Kubernetes,
- custom model training,
- exact PDF reconstruction,
- multi-agent translation swarm.

The project wins first by correctness, Persian quality, continuity, and clean interfaces.
