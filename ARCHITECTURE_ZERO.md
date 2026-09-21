# Tarjoman Architecture Zero

**Revision:** TARJOMAN-A0-PROD-2  
**Date:** 2026-09-21  
**Fork:** Amirezamky9/tarjoman  
**Upstream baseline:** `58e97b802aa3efb318135a5923231c0a08550c4a`  
**Architecture branch:** `arch/production-zero`  
**Status:** READY_FOR_OWNER_FREEZE  
**Supersedes:** TARJOMAN-A0-PROD-1

> This document is the normative engineering baseline for turning Tarjoman from a promising translation/quality toolkit into a production-grade, Persian-first content transformation engine. Once the owner freezes this revision, implementation changes that contradict a locked decision require an ADR.

## 0. Precedence and change control

When two project documents disagree, use this order:

1. `ARCHITECTURE_ZERO.md`
2. accepted ADRs under `docs/adr/`
3. `ROADMAP.md`
4. current contracts/tests
5. `research/`
6. README / historical skillpacks / examples

Research documents are evidence, not normative requirements. Existing README claims that conflict with code or this architecture must be corrected during implementation.

No architecture decision is changed silently. A change must:
- identify the affected decision ID,
- explain the reason and alternatives,
- include migration impact,
- update tests/evals,
- land as an ADR before implementation.

## 1. Product definition

Tarjoman is a **Persian-first localization and knowledge transformation engine**.

Its primary job is not merely “translate a sentence”. It takes text, documents, subtitles, or speech and produces **reliable, natural, reviewable Persian artifacts** while preserving structure, terminology, provenance, and quality evidence.

### 1.1 Primary product surfaces

1. **Translation** — high-quality English → Persian first; architecture supports other source languages and Persian ↔ English adapters.
2. **Persian review/polish** — normalize, lint, improve register, terminology, style, and typography without translating.
3. **Long-form projects** — books, papers, manuals, repositories of documents; resumable with translation memory and terminology consistency.
4. **Document localization** — preserve non-translatable structure and, where the format adapter supports it, formatting.
5. **Audio knowledge** — Persian/multilingual audio or video → timestamped transcript → cleaned Persian → lecture notes / meeting minutes / summary / action items.
6. **Agent-native operation** — deterministic CLI/Python/API plus MCP tools; optional A2A surface for remote-agent collaboration.
7. **Speech output (TTS)** — Persian text/artifacts → pronunciation-aware speech, optional voice cloning, audiobook/podcast/accessibility outputs, always behind model/license/safety policy.

### 1.2 What Tarjoman is not

- Not a new foundation model.
- Not tied to one LLM vendor.
- Not a mandatory cloud service.
- Not a full CAT desktop clone in v1.
- Not a video editor.
- Not an OCR research project; OCR/document parsing is delegated to adapters.
- Not a certification authority for legal/medical translations. High-risk profiles can require human review.

## 2. Architecture principles

### P1 — Lightweight core, heavy features as extras
The base package must not require Torch, Whisper, COMET, LibreOffice, FFmpeg, a web framework, or a database server. Heavy capabilities are optional extras/adapters.

### P2 — Provider-neutral by contract
No business logic imports an OpenAI/Anthropic/Ollama SDK directly. Translation/reflection/summarization call a typed Model Harness.

### P3 — Source content is data
Documents, transcripts, web text, and user-supplied glossaries are untrusted data. They cannot modify system policy or authorize tool actions.

### P4 — Deterministic structure, probabilistic language
Parsing, placeholders, document structure, terminology constraints, run state, caching, and validation are deterministic. LLMs are used only for language tasks where generative behavior is beneficial.

### P5 — Quality is externally measured
A generator must not award itself a production quality score. Rule checks, independent metrics, golden corpora, and human MQM review are separate from generation.

### P6 — Persian is first-class
RTL, ZWNJ, Persian/Arabic Unicode normalization, Persian punctuation, register, mixed Persian-English terms, and Persian typography are core contracts, not UI polish.

### P7 — Every output is traceable
A production artifact records source hash, project/profile versions, provider/model, prompt version, glossary/style versions, timings, token/cost data when available, and quality findings.

### P8 — Resumable and idempotent
Long translation/audio jobs survive interruption. Re-running a completed deterministic stage should not duplicate work.

### P9 — Safe auto-fix
Mechanical Unicode/spacing fixes may be automatic. Semantic rewrites must never be blindly regex-substituted when meaning can change.

### P10 — Interfaces share one core
CLI, Python SDK, FastAPI, MCP, and A2A are adapters over the same application services. They must not reimplement the pipeline.

## 3. High-level architecture

~~~text
 Inputs
 ├─ text / markdown / HTML
 ├─ DOCX / EPUB / subtitles / structured files
 ├─ PDF via parser adapter
 └─ audio / video via ASR adapter
          │
          ▼
  Ingestion + Canonical IR
  - stable segment IDs
  - structure/protected spans
  - language/domain metadata
          │
          ▼
  Project Context Builder
  - style profile
  - glossary / termbase
  - translation memory
  - entities / names / voice ledger
  - document summary / neighboring context
          │
          ▼
  Translation Orchestrator
  - chunk/batch planner
  - model harness
  - candidate / reflection strategy
  - retries / rate limits / cache
          │
          ▼
  Persian Quality Engine
  - deterministic normalization
  - constraint checks
  - terminology checks
  - safe lint + semantic review requests
          │
          ▼
  Independent Evaluation
  - exact invariants
  - chrF/SacreBLEU optional
  - COMET/XCOMET/DocCOMET optional
  - human MQM review sets
          │
          ▼
  Artifact Composer / Exporter
  - text / MD / HTML / Typst
  - bilingual review
  - DOCX/EPUB/subtitle adapters
  - transcript / notes / minutes
          │
          ▼
 Interfaces
 CLI | Python SDK | REST/jobs | MCP | optional A2A
~~~

## 4. Canonical intermediate representation (IR)

All input formats normalize into one canonical representation before translation.

Minimum contracts:

### `ProjectSpec`
- project_id
- source_language
- target_language
- domain_profile_id
- style_profile_id
- privacy_policy
- glossary_version
- translation_memory_scope
- provider_policy
- created_at / updated_at

### `Artifact`
- artifact_id
- project_id
- kind: text | document | subtitle | transcript | notes | minutes
- source_uri or logical source name
- source_hash
- parser_name + parser_version
- metadata
- segments[]

### `Segment`
- stable segment_id
- source_text
- source_span / location
- translatable bool
- protected_spans[]
- structural_context
- preceding/following context references
- translation
- review status
- findings[]
- provenance

### `ProtectedSpan`
- span_id
- type: code | url | email | math | placeholder | citation | tag | timestamp | speaker | other
- original_text
- integrity_policy: exact | normalized | mapped

### `RunRecord`
- run_id
- project_id
- operation
- status: queued | running | waiting_review | completed | failed | cancelled
- stage checkpoints
- config hash
- provider/model
- prompt hashes
- started_at / finished_at
- usage / cost / latency metadata
- error class + retry metadata

Stable IDs and source hashes are mandatory so caching, review, and resume are trustworthy.

## 5. Pipeline and state machine

The existing “5-pass” concept is retained as a product idea but redefined as an explicit, measurable workflow:

1. **Ingest / protect**  
   Parse structure, protect non-translatable spans, create stable segments.

2. **Analyze / plan**  
   Detect/confirm language and domain; build document summary, terminology candidates, entity/name ledger, style policy, and chunk plan.

3. **Generate**  
   Produce translation candidates using the configured backend and project context.

4. **Review / revise**  
   Independent critic or rule-driven review produces typed findings. A revision pass may correct semantic/style issues.

5. **Polish / validate / evaluate**  
   Apply safe Persian normalization, enforce hard constraints, restore protected spans, run independent metrics, and create final artifacts.

A project may skip stages explicitly (for example `polish-only`), but no hidden stage skipping is allowed.

## 6. Model Harness

### 6.1 Required interface

Application code calls capabilities, not vendors:

~~~python
class ModelProvider(Protocol):
    async def generate(self, request: ModelRequest) -> ModelResponse: ...
    def capabilities(self) -> ProviderCapabilities: ...
~~~

`ModelRequest` includes:
- task_type: translate | critique | revise | summarize | extract_terms | formalize
- source/target language
- messages / structured context
- required output schema
- temperature / seed when supported
- timeout
- privacy class

`ModelResponse` includes:
- text / structured payload
- provider + model
- usage
- finish reason
- latency
- request ID
- warnings

### 6.2 Built-in provider order

**P0 implementation priority**
1. `OpenAICompatibleProvider` — covers OpenRouter, 9router-style gateways, Ollama OpenAI compatibility, LM Studio, vLLM, and many hosted providers.
2. `AnthropicProvider` — optional direct adapter where native features are needed.
3. `CallableProvider` — test/custom integration.
4. `EchoProvider` — test-only; never a production default.

**Later optional adapters**
- local NMT / LibreTranslate-compatible service,
- Hugging Face / CTranslate2 NMT,
- specialized enterprise providers.

### 6.3 Fail-fast rule

`tarjoman translate` must never silently echo source text. If no real backend/model is configured, it exits with a clear configuration error unless the user explicitly selects `--backend echo` for testing.

### 6.4 Harness responsibilities

- timeout + bounded retry with exponential backoff,
- provider rate-limit handling,
- concurrency semaphore,
- cancellation,
- circuit-breaker behavior for repeatedly failing providers,
- usage/cost accounting,
- structured-output validation,
- capability validation before a run,
- provider fallback only when policy explicitly allows it,
- no secrets in logs.

## 7. Context, terminology, and translation memory

### 7.1 Translation memory

Replace JSON-only cache as the production source of truth with **SQLite WAL** in a per-user application data directory.

Core tables:
- projects
- artifacts
- segments
- segment_versions
- translation_memory
- glossary_terms
- style_profiles
- entity_ledger
- run_records
- quality_findings
- migrations/schema_meta

SQLite is sufficient for a lightweight local/server product and requires no separate service.

### 7.2 Cache key

A translation cache key must include at least:

- normalized source text hash,
- source/target languages,
- domain/style profile versions,
- glossary hard-constraint hash,
- relevant context hash,
- provider + model,
- prompt version,
- translation strategy version.

This prevents stale translations after terminology/style/model changes.

### 7.3 Professional interoperability

Support import/export progressively:
- TMX 1.4b for translation memory,
- TBX for termbases,
- XLIFF 2.x for localization interchange.

Do not implement all standards in Phase 1, but the data model must not block them.

### 7.4 Terminology policy

Terms have:
- source term,
- approved target,
- domain,
- status: suggested | approved | forbidden,
- case/inflection policy,
- notes/source,
- version.

“Approved” terms are hard constraints. “Suggested” terms are context hints.

### 7.5 Long-form context

For books/manuals:
- document-level summary,
- neighboring segments,
- project glossary,
- named entities,
- character voice/register ledger where applicable,
- retrieved TM matches.

Context is bounded by a token budget and recorded in provenance.

## 8. Persian Quality Engine

Split **normalization**, **linting**, and **semantic revision**.

### 8.1 Auto-fix safe layer
Allowed automatic operations:
- Arabic/Persian Kaf/Yeh normalization,
- ZWNJ normalization under tested rules,
- punctuation spacing,
- quote balancing suggestions,
- duplicate whitespace,
- digit policy by profile,
- Unicode direction/isolate hygiene,
- safe protected-token restoration.

### 8.2 Diagnostic layer
Flag, do not blindly rewrite:
- suspicious calques,
- passive constructions,
- awkward dialogue attribution,
- terminology inconsistencies,
- untranslated fragments,
- style/register mismatch,
- ambiguous number/unit handling.

Current regex anti-calque rules are retained initially as **detectors**. Semantic substitution moves to a revision engine or explicitly reviewed rule.

### 8.3 Persian NLP adapters

Optional adapters may use Hazm, DadmaTools, Parsivar, or other libraries behind Tarjoman-owned interfaces. No single external NLP library becomes a core architectural dependency.

### 8.4 Profiles

Profiles are versioned data, not hardcoded branches:
- literary
- scientific
- philosophy
- legal
- technical
- medical
- media
- financial
- classical
- transcreation
- meeting
- lecture_notes
- subtitle
- general

Each profile defines:
- register/style,
- digit policy,
- terminology sources,
- hard/soft QA rules,
- context strategy,
- human-review requirement,
- output templates.

## 9. Evaluation architecture

### 9.1 Four independent layers

1. **Invariant tests** — placeholders, numbers, units, URLs, code, math, tags, timestamps, speakers.
2. **Text metrics** — chrF++ / SacreBLEU where a reference exists.
3. **Neural MT evaluation** — optional COMET/XCOMET; DocCOMET for document context where appropriate.
4. **Human MQM** — release-gate samples reviewed with minor/major/critical errors.

No single scalar score is allowed to hide critical findings.

### 9.2 Golden corpus

Create a versioned `evals/golden/` corpus with:
- all existing 10 domains,
- short and long context,
- idioms,
- mixed Persian/English technical terms,
- numbers/dates/currency/units,
- code/math/URLs/HTML,
- dialogue,
- tables/list structures,
- subtitles,
- meeting/lecture transcript samples,
- adversarial prompt-injection text,
- known calque traps,
- human reference translations where licensing permits.

### 9.3 Release quality gates

For a release candidate:
- 100% protected-span round trip on invariant suite.
- 100% preservation of required numbers/units/identifiers.
- 100% hard-glossary compliance on deterministic test set.
- zero silent source echo in real translation mode.
- no new critical MQM finding in golden regression set.
- metric non-regression against frozen baseline; statistically compare systems when sample size permits.
- human review on a representative release sample before claiming “publication-grade”.

The current internal `100 - penalty` score may remain as a lint severity indicator but is renamed so it is not confused with translation quality.

## 10. Document and structured-file architecture

Every format is an adapter implementing:

~~~python
class IngestAdapter(Protocol):
    def detect(self, path: Path) -> bool: ...
    def ingest(self, path: Path) -> Artifact: ...

class ExportAdapter(Protocol):
    def export(self, artifact: Artifact, destination: Path) -> None: ...
~~~

### 10.1 Format rollout

**Phase 1:** TXT, Markdown, HTML/plain structured text  
**Phase 2:** SRT, VTT, ASS; JSON path-selected values  
**Phase 3:** DOCX and EPUB with formatting preservation  
**Phase 4:** PPTX/XLSX  
**PDF:** parser-driven extraction/reflow first; exact layout preservation is a separate capability and must not be falsely promised.

Inline tags/formatting are represented as protected/structural spans. Only translatable text reaches an LLM.

## 11. Audio and meeting/lecture module

Audio is an optional extra; it must not make the core install heavy.

### 11.1 ASR adapter

Initial recommended adapter:
- faster-whisper
- configurable model/device/compute type
- language auto-detect or explicit `fa`
- timestamps
- VAD option

Optional diarization adapter:
- WhisperX + a diarization backend, or another compatible local engine.
- Diarization is not required for single-speaker lecture mode.

### 11.2 Audio workflow

~~~text
audio/video
  → decode
  → ASR segments + timestamps
  → optional diarization / speaker labels
  → Persian normalization
  → optional spoken→written formalization
  → transcript artifact
  → template transform
      ├─ lecture notes
      ├─ meeting minutes
      ├─ executive summary
      ├─ decisions + action items
      └─ subtitle export
~~~

### 11.3 Lecture notes template

Outputs:
- title/metadata,
- structured outline,
- concepts/definitions,
- examples,
- key claims,
- formulas/technical terms preserved,
- questions raised,
- concise review section,
- timestamp links back to transcript where available.

### 11.4 Meeting template

Outputs:
- participants/speakers when known,
- agenda/topics,
- decisions,
- action items with owner/due date only when explicitly supported,
- open questions,
- risks/follow-ups,
- full timestamped transcript,
- formal Persian minutes option.

Never invent owners, due dates, or decisions absent from the transcript.

## 12. Interfaces

### 12.1 CLI
Must remain the primary lightweight interface.

Planned command groups:
- `tarjoman translate`
- `tarjoman review`
- `tarjoman lint`
- `tarjoman eval`
- `tarjoman project ...`
- `tarjoman glossary ...`
- `tarjoman tm ...`
- `tarjoman compose ...`
- `tarjoman transcribe ...` (audio extra)
- `tarjoman serve` (server extra)
- `tarjoman mcp` (MCP extra)

### 12.2 Python SDK
Typed application-service API; no CLI subprocess required for integrations.

### 12.3 REST / jobs
Optional FastAPI server:
- versioned `/v1` endpoints,
- async job API for long tasks,
- idempotency key support,
- status/progress/cancel,
- OpenAPI generated from Pydantic contracts,
- local bind by default; auth required when exposed beyond localhost.

### 12.4 MCP
Implement the current MCP specification through the official SDK when the phase begins.

Initial tools:
- tarjoman.translate
- tarjoman.review
- tarjoman.project.create
- tarjoman.project.status
- tarjoman.glossary.upsert
- tarjoman.eval
- tarjoman.transcribe
- tarjoman.notes.generate
- tarjoman.export

Tools return structured IDs/artifacts, not giant opaque prose blobs when a resource handle is more appropriate.

### 12.5 A2A
A2A is optional and layered above application services. Use it only when Tarjoman acts as an independent remote agent. MCP remains the simpler tool surface for most coding/assistant agents.

## 13. Security and privacy

### 13.1 Default posture
- local project storage,
- no telemetry by default,
- no source text in info logs,
- secrets only via environment/keyring/provider secret store,
- explicit policy for cloud provider use.

### 13.2 Provider privacy classes
A project can be:
- `local_only` — network model calls forbidden,
- `cloud_allowed` — approved providers may receive content,
- `restricted` — only explicitly allowlisted providers/models.

Policy is enforced in the Model Harness, not prompts.

### 13.3 Prompt injection
Input content is quoted/segmented as data. It cannot change system instructions. Tool interfaces have no arbitrary shell/filesystem access. Agent adapters expose only Tarjoman capabilities.

### 13.4 Sensitive output
Logs contain hashes/IDs and operational metadata. Debug content logging is opt-in and visibly marked unsafe for sensitive projects.

## 14. Reliability, performance, and observability

### 14.1 Resumability
Each long job checkpoints stage + segment state. Atomic artifact writes use temp-file + replace semantics.

### 14.2 Concurrency
- bounded async worker pool,
- per-provider semaphore,
- configurable max in-flight requests,
- backpressure rather than unbounded task creation,
- deterministic output ordering independent of completion order.

### 14.3 Retry rules
Retry only transient failures: rate limits, timeouts, selected 5xx/network errors. Validation/semantic failures go through a bounded correction path, not infinite retries.

### 14.4 Structured logs
Every log record can include:
- run_id / project_id / segment_id,
- stage,
- provider/model,
- latency,
- retry count,
- cache hit,
- quality finding counts.

### 14.5 Metrics
Optional server metrics:
- job latency,
- provider latency/error rate,
- tokens/cost,
- cache hit rate,
- quality finding rate,
- ASR real-time factor when audio enabled.

## 15. Packaging and technology

### 15.1 Primary language
Keep **Python** as the orchestration/core language. It already fits the codebase and AI/NLP ecosystem.

Rust/TypeScript are allowed only where they solve a concrete boundary problem (desktop/audio capture/UI), not as a rewrite goal.

### 15.2 Target Python
Production target: Python 3.11–3.13 initially. Reassess 3.10 compatibility before release rather than carrying it automatically.

### 15.3 Optional extras

Target packaging shape:

- `tarjoman` — core, CLI, deterministic Persian quality, SQLite state
- `tarjoman[llm]` — HTTP/provider adapters
- `tarjoman[docs]` — document adapters
- `tarjoman[asr]` — faster-whisper/audio-input tooling
- `tarjoman[tts]` — speech synthesis engines/G2P adapters
- `tarjoman[speech]` — convenience extra for ASR + TTS
- `tarjoman[eval]` — SacreBLEU/COMET/TTS-eval stack
- `tarjoman[server]` — FastAPI/Uvicorn
- `tarjoman[mcp]` — MCP server
- `tarjoman[all]` — convenience only

Heavy optional libraries must not leak into base imports.

## 16. Target repository layout

~~~text
tarjoman/
├─ ARCHITECTURE_ZERO.md
├─ ROADMAP.md
├─ research/
├─ docs/
│  └─ adr/
├─ src/tarjoman/
│  ├─ application/
│  ├─ core/
│  │  ├─ contracts/
│  │  ├─ pipeline/
│  │  └─ policies/
│  ├─ providers/
│  ├─ quality/
│  ├─ profiles/
│  ├─ memory/
│  ├─ ingest/
│  ├─ export/
│  ├─ audio/          # imported only with extra
│  ├─ evals/          # lightweight interfaces; heavy impl optional
│  ├─ interfaces/
│  │  ├─ cli/
│  │  ├─ api/
│  │  ├─ mcp/
│  │  └─ a2a/
│  └─ prompts/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ contract/
│  └─ security/
├─ evals/
│  ├─ golden/
│  └─ reports/
└─ .github/workflows/
~~~

Migration to `src/` layout happens once in Foundation Phase; avoid repeated reshuffles.

## 17. CI/CD and supply-chain requirements

Pull requests eventually run:
1. format/lint,
2. static type checks,
3. unit tests,
4. contract tests,
5. security/static checks,
6. package build,
7. offline deterministic benchmark,
8. golden eval smoke subset.

Scheduled/manual workflows run expensive provider/COMET/audio evaluations so pull requests do not require secrets or GPUs.

Releases:
- version from one source of truth,
- changelog/release notes,
- build sdist + wheel,
- install smoke test in clean env,
- optional Sigstore/package provenance,
- dependency vulnerability scan,
- SBOM for packaged server/desktop distributions.

`main` should be branch-protected after the first production CI gates exist.

## 18. Compatibility policy

- Semantic Versioning for public Python/CLI/API interfaces.
- Schema migrations are monotonic and tested from previous release fixtures.
- Prompt/profile versions are explicit and stored with runs.
- A project created by a released version must either migrate automatically or fail with a precise migration message; silent data loss is forbidden.

## 19. Locked decision ledger

| ID | Decision |
|---|---|
| D01 | Tarjoman becomes a Persian-first content transformation engine, not only a regex translation script. |
| D02 | Python remains the core language; no rewrite for fashion. |
| D03 | Base installation stays lightweight; heavy AI/audio/eval/server features are extras. |
| D04 | Canonical IR separates ingestion/export from translation logic. |
| D05 | Real model backend is mandatory for real translation; Echo is test-only. |
| D06 | OpenAI-compatible provider is first implementation priority; vendor adapters stay behind one harness. |
| D07 | SQLite WAL is the production local state/TM/termbase store. |
| D08 | Translation memory, glossary, style profiles, prompts, and provenance are versioned. |
| D09 | Regex anti-calque rules become diagnostics by default; unsafe semantic auto-rewrites are removed. |
| D10 | Quality evaluation is independent from generation and includes external metrics + human MQM. |
| D11 | File formats are adapters over one IR; structure is never entrusted blindly to an LLM. |
| D12 | PDF exact-layout preservation is not promised until a dedicated fidelity pipeline proves it. |
| D13 | Audio/meeting/lecture capability is an optional module over the same artifact pipeline. |
| D14 | CLI/Python are core; FastAPI and MCP are optional interfaces over shared services. |
| D15 | MCP is the primary agent-tool protocol; A2A is optional for remote-agent identity/collaboration. |
| D16 | Privacy policy is enforced in the Model Harness; source content is not logged by default. |
| D17 | Long jobs are resumable, idempotent, bounded-concurrency jobs. |
| D18 | Architecture changes after freeze require ADRs. |
| D19 | Module dependencies follow Core <- Application <- Infrastructure/Adapters <- Interfaces; reverse imports are forbidden. |
| D20 | SQLite stores transactional metadata; large/binary artifacts live in a content-addressed filesystem store, not DB BLOBs. |
| D21 | Configuration precedence is CLI > environment > project config > user config > defaults; secrets never live in project config. |
| D22 | v1 uses a SQLite-backed single-node persistent job engine; Redis/Celery/Kafka are forbidden unless an ADR proves need. |
| D23 | Prompts, profiles, rules, schemas, and strategy versions are immutable identifiers recorded in every run. |
| D24 | TTS is an optional provider-neutral speech-output module; it never becomes a mandatory base dependency. |
| D25 | Persian speech normalization, pronunciation lexicon, G2P, speech planning, synthesis, and audio post-processing are separate contracts. |
| D26 | `nimaone/persian_tts` / pocket-tts-farsi-v2 is research/non-commercial by default; it is never bundled into a commercial production profile without an explicit compatible license. |
| D27 | Every external model/voice/dataset must have a machine-readable ModelManifest and pass a license gate before production use or redistribution. |
| D28 | Voice cloning requires explicit capability enablement, reference-audio consent/ownership attestation, provenance, and retention controls. |
| D29 | TTS quality is independently evaluated for pronunciation/intelligibility, naturalness, speaker similarity when relevant, long-form stability, latency/RTF, memory, and failure rate. |
| D30 | Patterns from external repos may be independently reimplemented; code is not copied when repository/model licensing is absent, incompatible, or unclear. |
| D31 | Raw audio/transcript/source text is immutable evidence; cleaned/formalized/synthesized artifacts are versioned derivatives with lineage. |
| D32 | Optional plugins are registered explicitly; import-time plugin discovery and surprise network/model downloads are forbidden. |
| D33 | Architecture-conformance tests enforce dependency direction, optional-dependency isolation, no direct provider SDK in core, and no network in deterministic tests. |
| D34 | One implementation work package per PR by default; architecture-changing code is blocked until its ADR is accepted. |
| D35 | Provider/model fallback is explicit policy; silent fallback to a different model, cloud, language, or quality tier is forbidden. |

## 20. Definition of “production-ready v1”

Tarjoman v1 is not declared production-ready until all are true:

- real provider path works end-to-end and default CLI never echoes input,
- state is migrated from ad-hoc JSON to tested SQLite schema,
- critical constraints have deterministic tests,
- golden English→Persian corpus and regression reports exist,
- at least one external quality metric is integrated,
- human MQM review has been performed on release candidate samples,
- TXT/MD/HTML/SRT/VTT are reliable; DOCX available if its fidelity gate passes,
- long jobs resume after interruption,
- structured logs and provenance are complete,
- provider timeouts/retries/rate limits are bounded and tested,
- secrets are not logged or stored in project files,
- MCP tool surface passes contract tests,
- docs describe actual implemented flags/features only,
- CI gates main and a clean package install succeeds.

## 21. Deferred, not ambiguous

The following are intentionally deferred and therefore **must not block Foundation work**:

- Web UI framework: no UI is required for core v1.
- Desktop/Tauri app: later adapter.
- Exact PDF layout preservation: separate milestone.
- Default frontier cloud model: runtime config, not architecture.
- Default diarization model: adapter choice after license/quality bake-off.
- Multi-user database server/Postgres: only if SQLite measurements justify it.

The default action for a deferred item is **do not implement it early**.


---

## 22. Implementation architecture: layers and dependency law

This section turns the conceptual architecture into rules that coding agents can test.

### 22.1 Layers

~~~text
┌─────────────────────────────────────────────────────────┐
│ Interfaces: CLI / REST / MCP / A2A / future Web UI     │
└──────────────────────────────┬──────────────────────────┘
                               │ calls
┌──────────────────────────────▼──────────────────────────┐
│ Application: use-cases, jobs, orchestration, services  │
└──────────────────────────────┬──────────────────────────┘
                               │ depends on ports/contracts
┌──────────────────────────────▼──────────────────────────┐
│ Core: IR, policies, state machines, pure quality rules │
└──────────────────────────────▲──────────────────────────┘
                               │ implemented by
┌──────────────────────────────┴──────────────────────────┐
│ Infrastructure/Adapters: DB, providers, files, ASR/TTS │
└─────────────────────────────────────────────────────────┘
~~~

Dependency rule:
- `core` imports only stdlib + explicitly approved lightweight schema/runtime dependencies.
- `application` may import `core`, never concrete infrastructure.
- `infrastructure/adapters` implement ports defined by core/application.
- `interfaces` call application services and may compose adapters at startup.
- adapters do not call CLI/API/MCP code.
- one interface never imports another interface.
- provider SDKs, FastAPI, MCP SDK, Whisper, ONNX Runtime, COMET and document libraries are never imported by base-core modules.

CI must enforce this with import-boundary tests.

### 22.2 Package ownership

| Package | Owns | Must not own |
|---|---|---|
| `core.contracts` | stable IR/data contracts | network, DB sessions, provider clients |
| `core.policies` | privacy/license/retry/routing decisions | provider-specific code |
| `core.quality` | deterministic Persian normalization + typed findings | model calls |
| `application` | use cases and transaction boundaries | HTTP framework |
| `providers` | LLM provider adapters | business decisions |
| `storage` | SQLite repositories + blob store | UI behavior |
| `ingest/export` | file format transformations | translation strategy |
| `speech.asr` | ASR ports/adapters | meeting summaries |
| `speech.tts` | TTS ports/adapters | translation decisions |
| `interfaces.*` | input/output protocol mapping | duplicate core logic |

## 23. Configuration and secret contract

### 23.1 Precedence

Highest wins:

1. explicit CLI/API call arguments,
2. environment variables,
3. project `tarjoman.toml`,
4. user config under OS application-data directory,
5. packaged defaults.

No hidden current-working-directory config lookup beyond the explicit project file.

### 23.2 Secrets

API keys/tokens:
- environment variable or OS keyring/secret provider only,
- never written to project TOML, SQLite run payloads, logs, benchmark reports, or exported artifacts,
- redaction applies to exception text and provider HTTP traces.

### 23.3 Reproducibility snapshot

Each run stores a redacted resolved-config snapshot hash plus:
- provider/model,
- strategy ID,
- prompt/profile/rule versions,
- glossary/TM/context hashes,
- random seed where supported,
- package version and schema version.

## 24. Error taxonomy and failure semantics

Public errors are typed:

| Error | Retry? | User action |
|---|---:|---|
| `ConfigurationError` | no | fix config |
| `PolicyViolationError` | no | change policy/permission |
| `LicensePolicyError` | no | use approved model/voice |
| `CapabilityUnavailableError` | no | install extra or choose adapter |
| `ProviderRateLimitError` | bounded | wait/backoff |
| `ProviderTransientError` | bounded | retry/fallback if policy allows |
| `ProviderPermanentError` | no | fix request/provider |
| `StructuredOutputError` | one bounded repair path | model/schema issue |
| `ArtifactValidationError` | no | inspect source/parser |
| `MigrationError` | no automatic destructive repair | restore/upgrade |
| `JobCancelledError` | no | expected cancellation |
| `SpeechSynthesisQualityError` | bounded per configured policy | retry/alternate engine only if allowed |

Rules:
- no blanket `except Exception: pass` in production paths,
- no infinite retry,
- errors crossing CLI/API/MCP are mapped to stable machine codes,
- raw source content is excluded from normal error messages.

## 25. Storage architecture

### 25.1 Split metadata from binary artifacts

SQLite WAL stores metadata and text-sized records. Large files use an artifact store:

~~~text
<project-root>/.tarjoman/
  project.toml
  state.sqlite3
  artifacts/
    sha256/
      ab/
        <full-sha256>
  exports/
  locks/
~~~

Audio, video, PDFs, DOCX, generated WAV/MP3 and other large binaries are never stored as SQLite BLOBs in v1.

### 25.2 Artifact record

Every stored binary has:
- artifact_id,
- sha256,
- byte_size,
- MIME type,
- logical filename,
- producer + version,
- parent artifact IDs,
- created_at,
- retention/sensitivity policy.

Writes:
1. stream to temp file,
2. hash while writing,
3. fsync where supported,
4. atomic rename to content-addressed path,
5. commit DB metadata.

Partial artifacts are never presented as completed.

### 25.3 Database rules

- numbered SQL migrations,
- migration transaction where SQLite permits,
- `PRAGMA foreign_keys=ON`,
- WAL mode,
- explicit busy timeout,
- indexes justified by query plan/benchmarks,
- no destructive migration without backup/forward-migration plan,
- repository layer owns SQL,
- schema version checked before application work starts.

## 26. Persistent job engine

v1 uses a lightweight SQLite-backed job system.

### 26.1 Job states

`QUEUED → RUNNING → {WAITING_REVIEW | SUCCEEDED | FAILED | CANCELLED}`

A RUNNING job stores heartbeat/lease time. On restart, expired RUNNING leases return to a resumable state according to stage policy.

### 26.2 Stage checkpoint

Each stage records:
- input artifact/version hash,
- output artifact/version hash,
- stage implementation version,
- status,
- attempts,
- started/finished timestamps,
- last typed error.

### 26.3 Idempotency

A user-facing idempotency key plus operation/config/input hash prevents duplicate long jobs.

### 26.4 Concurrency

- bounded worker pool,
- per-provider semaphore,
- per-device speech semaphore,
- deterministic result ordering,
- no unbounded `gather()`,
- backpressure at queue admission.

Redis/Celery/Kafka are explicitly out of scope for v1 single-node mode.

## 27. Segment and review state machine

Translation segments use:

`PENDING → DRAFTED → REVIEW_REQUIRED → REVIEWED → APPROVED`

Optional direct path:
`DRAFTED → APPROVED` only when project policy allows and all hard gates pass.

Any source/glossary/style/profile change invalidates approval when its cache/provenance hash changes.

Human edits create a new segment version; they never overwrite history.

## 28. Prompt, rule, and profile registry

IDs are immutable, e.g.:
- `translate.fa.v1`
- `critique.fa.mqm.v2`
- `profile.technical.fa.v3`
- `rules.persian-normalize.v2`
- `strategy.reflect-1.v1`

Editing behavior creates a new version ID. Old project runs remain reproducible.

Prompt templates are code-reviewed assets, not user-writable arbitrary templates in production mode unless the project is explicitly in custom-prompt mode.

## 29. Plugin/capability registry

Optional components register an explicit capability descriptor:

~~~text
capability_id
package
version
operations
languages
formats
hardware requirements
network requirement
license status
commercial-use status
redistribution status
model manifests
~~~

Startup never imports every optional package “just in case”. A missing optional dependency produces `CapabilityUnavailableError` with the exact extra/install route.

## 30. Model and dataset compliance registry

Every model/voice/dataset has a `ModelManifest` or `DataManifest`.

Required fields:
- immutable ID + source URL/revision/hash,
- task/languages,
- code license,
- model-weight license,
- known training-data license/provenance statement,
- commercial_use: allowed | forbidden | unknown,
- redistribution: allowed | forbidden | unknown,
- attribution requirements,
- remote-code requirement,
- security review status,
- reviewed_at,
- reviewer/evidence links.

### 30.1 License gate

Production profiles permit only `commercial_use=allowed`.

`forbidden` and `unknown`:
- may run only in explicitly non-commercial/research profiles,
- may never be bundled into a commercial distribution,
- may never silently download in production.

A child model card claiming a permissive license does not override a restrictive base model. The full dependency/model lineage must be checked.

## 31. Speech-output (TTS) architecture

TTS is a first-class optional output subsystem, but it is not coupled to translation.

~~~text
Text/Artifact
  → SpeechTextNormalizer
  → PronunciationResolver
      ├─ project pronunciation lexicon
      ├─ named-entity overrides
      └─ G2P adapter
  → SpeechPlanner
      ├─ sentence/phrase boundaries
      ├─ pause plan
      ├─ chunk/token budget
      ├─ pace/style hints
      └─ language/code-switch spans
  → TtsEngine
      ├─ fixed/multi-speaker
      └─ optional voice-cloning reference
  → AudioQualityGate
  → AudioPostProcessor
  → AudioArtifact + provenance
~~~

### 31.1 TTS contracts

`TtsEngine`:

~~~python
class TtsEngine(Protocol):
    def capabilities(self) -> TtsCapabilities: ...
    async def synthesize(self, request: TtsRequest) -> TtsResult: ...
~~~

`TtsCapabilities` declares:
- languages,
- voice cloning yes/no,
- streaming yes/no,
- seed/determinism support,
- sample rates,
- max recommended text/chunk,
- GPU/CPU requirements,
- supported reference-audio duration,
- license manifest ID.

`TtsRequest` includes:
- normalized speech text or phoneme plan,
- language,
- voice profile,
- pace/style,
- seed,
- output format,
- privacy/license policy.

`TtsResult` includes:
- audio artifact,
- sample rate/channels/duration,
- engine/model/version,
- seed,
- pronunciation plan hash,
- quality-gate results,
- usage/latency/RTF,
- warnings.

### 31.2 Speech normalization is not publication normalization

Before TTS, text may require:
- number verbalization,
- currency/date/time reading,
- abbreviations/acronyms,
- URLs/emails policy,
- Latin technical-term pronunciation,
- punctuation-to-prosody mapping,
- optional Persian diacritics/phoneme hints.

The original written artifact is never modified by speech normalization.

### 31.3 Pronunciation lexicon

Project-level dictionary:

`surface form → normalized reading → optional phonemes → language tag → notes/status`

Priority:
1. explicit segment override,
2. approved project pronunciation lexicon,
3. named-entity dictionary,
4. G2P,
5. engine-native fallback.

Manual phoneme editing learned from `nimaone/persian_tts` becomes a durable pronunciation override, not a one-off UI hack.

### 31.4 Long-form speech planner

The planner, not the model, owns:
- sentence splitting,
- phrase packing,
- max token/phoneme budget,
- punctuation pauses,
- paragraph/chapter gaps,
- deterministic chunk order,
- retry boundaries.

Engine-specific constraints are capability data, not hardcoded global constants.

### 31.5 Voice profiles

A voice profile may be:
- built-in fixed voice,
- engine speaker ID,
- user reference audio,
- reusable derived speaker embedding if the engine/license permits.

Reference audio rules:
- content type/size/duration validation before full decode,
- mono/sample-rate conversion in controlled temp storage,
- explicit retention policy,
- original reference hash recorded,
- deletion removes derived cache/embedding where applicable.

## 32. TTS engines: adoption policy

### 32.1 `nimaone/persian_tts` / Pocket-TTS Farsi v2 ONNX

**What we adopt as engineering patterns**
- pure ONNX CPU path without Torch,
- explicit G2P stage,
- model package manifest,
- word/phrase-aware chunk planning,
- reference-voice caching,
- reproducible seed,
- bounded parallel chunk generation,
- bounded retry after acoustic-quality heuristics,
- loudness/silence stitching,
- manual pronunciation correction.

**What we do not adopt directly**
- no production bundling of the current Pocket Farsi v2 weights under CC-BY-NC-4.0,
- no code copy from the repository while its own repository license is not explicit,
- no unauthenticated demo-server design,
- no full-file upload read without byte limits,
- no global engine lock as final concurrency architecture,
- no in-memory-only result store as production artifact storage.

A future adapter can support a user-supplied Pocket ONNX package in `research/noncommercial` mode if license policy allows.

### 32.2 Commercial-capable candidates to benchmark

Candidates are not defaults until bake-off and license review:

- **MOSS-TTS v1.5** — model card lists Persian among 31 languages and Apache-2.0; strong long-form/voice-cloning features, but ~8.5B parameters / large weight footprint make it a heavy GPU/server profile, not a lightweight default.
- **Persian Piper/ONNX voices** — attractive fixed-voice CPU profile; each voice's exact model/data license and quality must be recorded before approval.
- **ManaTTS-derived Persian models** — some published weights report CC0; useful commercial-compatible baseline candidates if quality/fidelity pass.
- other new Persian models may enter only through the same manifest/bake-off process.

Models based on XTTS-v2/CPML or MMS CC-BY-NC remain non-commercial unless their legal status changes.

## 33. Voice-cloning safety and consent

Voice cloning is an opt-in capability, never the anonymous default.

Production requirements:
- feature disabled unless project/admin enables it,
- request records that user asserts authorization to use the reference voice,
- public unauthenticated endpoint cannot create persistent cloned voice profiles,
- retention/deletion policy for reference audio and derived embeddings,
- provenance flag `voice_cloned=true` in generated audio metadata/report,
- engine-provided watermarking is preserved when available,
- rate/size limits and abuse controls in server mode,
- logs never contain raw voice bytes.

Tarjoman does not claim biometric identity verification; it records provenance and enforces product policy.

## 34. TTS quality evaluation

A TTS release is evaluated independently from synthesis.

### 34.1 Persian pronunciation suite
Must cover:
- Ezafe,
- ambiguous unvowelled words,
- Arabic/Persian names,
- English technical terms in Persian,
- numbers/dates/currency,
- acronyms,
- ZWNJ compounds,
- punctuation/prosody,
- long unpunctuated sentences,
- domain terminology.

### 34.2 Metrics

Record at minimum:
- ASR-backtranscription WER/CER as an intelligibility signal,
- pronunciation error rate on curated lexicon cases,
- human MOS/naturalness sample,
- speaker similarity for clone engines,
- long-form repetition/runaway/truncation rate,
- duration/pace error,
- first-audio latency,
- RTF,
- peak RAM/VRAM,
- cold-start time,
- failure/retry rate.

UTMOS or another learned metric may be secondary evidence, not the sole release gate.

### 34.3 Determinism
Where seed is supported:
- same engine/model/voice/text/seed must reproduce within defined tolerance,
- engine changes require a new implementation/model version.

## 35. Speech artifact lineage

Examples:

~~~text
source_document
  └─ translated_fa_v4
      ├─ speech_plan_v2
      │   └─ wav_v1
      └─ audiobook_mp3_v1

meeting_audio_raw
  └─ transcript_raw
      └─ transcript_clean
          ├─ minutes_v3
          └─ spoken_summary_script
              └─ tts_audio_v2
~~~

Every derivative points to parent artifact IDs and configuration hashes.

## 36. Server/API security baseline

Any non-loopback server mode requires:
- authentication,
- request size limits at server/proxy and application layers,
- bounded multipart upload,
- MIME + decoder validation,
- temporary-file quotas,
- per-user/project authorization,
- rate limiting for expensive operations,
- job IDs rather than blocking long HTTP requests,
- no arbitrary user path parameters,
- download by authorized artifact ID,
- secure filename normalization,
- cancellation and cleanup.

Demo mode may be loopback-only and explicitly marked non-production.

## 37. Testing pyramid and conformance

### PR-gating deterministic suite
- unit tests,
- contract/schema tests,
- DB migration tests,
- artifact round-trip tests,
- provider fake-server tests,
- dependency-boundary tests,
- security tests,
- CLI/API/MCP equivalence tests,
- optional-dependency import tests.

### Scheduled/opt-in expensive suite
- real provider translation evals,
- COMET/XCOMET,
- ASR benchmarks,
- TTS acoustic benchmarks,
- GPU/server profiles,
- human review exports.

No secret-dependent test is required for a normal fork contributor PR.

## 38. Coding-agent implementation protocol

Every coding-agent task must name one roadmap Work Package ID.

Before editing, the agent must read:
1. `ARCHITECTURE_ZERO.md`,
2. accepted ADRs,
3. the work package in `ROADMAP.md`,
4. relevant research file(s),
5. current tests/contracts.

### 38.1 Required PR evidence

A work-package PR includes:
- scope and IDs,
- files changed,
- contracts/schema changed,
- migration impact,
- tests added/changed,
- commands/tests executed,
- benchmark/eval impact where relevant,
- documentation updated,
- known limitations,
- confirmation that no locked decision was changed.

### 38.2 Forbidden agent shortcuts

Without an accepted ADR, an agent must not:
- rewrite Python core in another language,
- add Redis/Celery/Kafka/Postgres,
- put provider SDK calls in core/application business rules,
- make Torch/Whisper/COMET/FastAPI mandatory base dependencies,
- change public schema silently,
- modify an old migration after release,
- log source text/secrets by default,
- silently fallback to cloud or another model,
- use a model whose manifest license is unknown/non-commercial in production profile,
- “fix” semantic Persian with unconditional regex replacements,
- let an LLM translate raw document markup/timecodes/identifiers without structural protection,
- store large binaries in SQLite,
- bypass job checkpoints for long operations,
- document flags/features that lack executable tests.

### 38.3 Ambiguity protocol

If implementation encounters a case not determined by architecture:
- if it is internal and does not affect public behavior/data/security/license, choose the simplest implementation and document it in the PR;
- if it affects API/schema/data migration/security/privacy/license/model behavior/caching/public semantics, stop that work package and propose an ADR.
No architecture-level guess is permitted.

## 39. Definition of Done for every work package

A package is DONE only when:
- acceptance criteria pass,
- tests cover success + at least one failure path,
- errors are typed,
- logs/provenance are adequate,
- optional dependency isolation is preserved,
- docs reflect actual behavior,
- no TODO/FIXME remains for an acceptance criterion,
- no architecture violation exists,
- migrations are tested if data changed,
- benchmark/eval baseline is updated when observable quality/performance changes.

“Code written” is not DONE.

## 40. Release profiles

Tarjoman can release capability profiles independently while sharing one versioned core:

### Core profile
Translation, Persian quality, project/TM/glossary, deterministic formats.

### ASR profile
Core + speech input/transcription/meeting/lecture derivatives.

### TTS profile
Core + pronunciation/G2P/TTS engines and speech-output evals.

### Agent/server profile
Core + persistent jobs + REST/MCP.

A broken optional speech engine blocks that profile, not an unrelated base-package security fix. Compatibility and schema remain coordinated by the same release version.
