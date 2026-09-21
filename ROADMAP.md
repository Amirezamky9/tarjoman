# Tarjoman Production Roadmap

**Architecture:** TARJOMAN-A0-PROD-1  
**Date:** 2026-09-21  
**Status:** READY_FOR_OWNER_FREEZE  
**Baseline:** `58e97b802aa3efb318135a5923231c0a08550c4a`

This roadmap is execution order, not a wishlist. A later phase cannot silently pull unfinished foundational work forward. Each phase has explicit exit criteria.

## Phase 0 — Architecture and evidence baseline

**Goal:** eliminate architectural ambiguity before implementation.

### Deliverables
- `ARCHITECTURE_ZERO.md`
- this roadmap
- `research/` evidence pack
- ADR process
- immutable upstream baseline recorded

### Exit
- owner reviews and freezes Architecture Zero,
- contradictory README/skill claims are listed for correction,
- implementation branch starts from the frozen baseline.

---

## Phase 1 — Production foundation

**Priority:** P0

### Work
1. Move once to `src/tarjoman` package layout.
2. Introduce typed error taxonomy and application services.
3. Define canonical IR: Project, Artifact, Segment, ProtectedSpan, RunRecord.
4. Add typed configuration with config file + environment override.
5. Implement SQLite schema + numbered migrations.
6. Port current termbase/cache/voice ledger into schema.
7. Create prompt/profile version registry.
8. Split safe normalization from semantic diagnostics.
9. Add structured logging with run IDs.
10. Add lint/type/coverage/package-build CI.
11. Add ADR templates and architecture conformance tests.

### Exit criteria
- all existing deterministic behavior is covered or deliberately retired,
- zero direct provider SDK imports in core,
- DB migration test from empty → latest,
- JSON legacy project import path documented/tested,
- package imports with base dependencies only,
- current 96 tests are either migrated or replaced with equivalent coverage,
- README no longer claims unimplemented provider flags.

---

## Phase 2 — Real translation MVP

**Priority:** P0

### Work
1. Implement `OpenAICompatibleProvider`.
2. Add provider/model/base-url/API-key configuration.
3. Make Echo backend test-only and explicit.
4. Async translation orchestrator with bounded concurrency.
5. Timeouts, retries, rate-limit backoff, cancellation.
6. Glossary hard/soft constraint injection.
7. Context builder: neighbors + project summary + TM matches + entities.
8. Typed critique/revision findings.
9. Cache with full provenance/version key.
10. CLI:
   - translate
   - review
   - lint
   - project
   - glossary
   - tm
11. Provider contract tests with fake HTTP server.

### Exit criteria
- English→Persian real translation works with any tested OpenAI-compatible endpoint,
- no configured provider → explicit error, never source echo,
- interrupted multi-segment run can resume,
- hard glossary tests pass,
- protected structures survive translation,
- retry/cancellation behavior is deterministic.

---

## Phase 3 — Evaluation and Persian quality

**Priority:** P0

### Work
1. Build licensed/internal golden corpus by domain.
2. Freeze first reference baseline.
3. Integrate SacreBLEU/chrF++ optional eval.
4. Integrate COMET/XCOMET optional eval; add document-level path where practical.
5. Define human MQM annotation guide for Persian.
6. Add adversarial and prompt-injection samples.
7. Replace current “100-point quality score” marketing semantics with:
   - constraint report,
   - metric report,
   - MQM findings.
8. Expand Persian normalizer with tested adapters/rules.
9. Evaluate calque detectors for false positives before auto-fix decisions.
10. Add model/provider bake-off command and report format.

### Exit criteria
- every release can produce a versioned eval report,
- metric regression is visible by domain,
- zero critical invariant failures,
- human review process documented and used on an RC sample,
- no “publication-grade” claim without supporting report.

---

## Phase 4 — Format fidelity and professional translation memory

**Priority:** P1

### Work
1. Stable adapters for TXT/MD/HTML.
2. Subtitle adapters: SRT/VTT/ASS.
3. JSON selected-path translation.
4. DOCX ingest/export with run-level/paragraph structure preservation.
5. EPUB adapter.
6. TMX import/export.
7. TBX import/export.
8. XLIFF import/export subset.
9. Review diff package and status: draft/reviewed/approved.
10. Exact/fuzzy TM search.
11. Repetition detection / reuse.

### Exit criteria
- format round-trip fixtures exist,
- tags/placeholders/timecodes cannot be altered by model,
- DOCX fidelity suite passes before feature is advertised,
- project can export TM/termbase without vendor lock-in.

---

## Phase 5 — Audio, meeting, and lecture notes

**Priority:** P1

### Work
1. Optional audio extra with faster-whisper adapter.
2. FFmpeg/media decode boundary.
3. ASR result IR with segment/word timestamps.
4. Persian ASR normalization.
5. Optional WhisperX/diarization adapter.
6. Lecture-notes template.
7. Meeting-minutes template.
8. Decisions/action-items extraction with evidence spans.
9. Spoken→written Persian formalization.
10. SRT/VTT export from transcript.
11. Resume/checkpoint long transcription jobs.

### Exit criteria
- Persian audio fixture → transcript → notes/minutes end-to-end,
- each summary/decision/action item can reference transcript segment IDs,
- no invented owner/due date in extraction tests,
- audio module can be omitted from base install,
- CPU-only and accelerated paths fail gracefully.

---

## Phase 6 — Agent/API surfaces

**Priority:** P1

### Work
1. FastAPI optional server.
2. Versioned REST API + OpenAPI.
3. Persistent job status/progress/cancel.
4. Idempotency key support.
5. MCP server using official SDK/current spec.
6. Resource handles for large artifacts.
7. Agent-safe tool schemas.
8. Optional A2A Agent Card + task adapter.
9. Agent integration tests.

### Exit criteria
- CLI, Python, API, MCP return equivalent core results for same config,
- MCP tools are deterministic and schema-valid,
- no arbitrary shell/filesystem tool is exposed,
- restricted/local-only project policy cannot be bypassed through agent interfaces.

---

## Phase 7 — Review UX and lightweight web app

**Priority:** P2

Only begin after core behavior and API are stable.

### Candidate UX
- project dashboard,
- side-by-side source/target,
- segment diff,
- glossary/TM pane,
- quality findings,
- provider/cost/provenance,
- audio transcript timeline,
- lecture/meeting templates,
- human approval workflow.

### Exit
- UI is generated from API contracts,
- no duplicate business logic in frontend,
- accessibility + RTL review completed.

---

## Phase 8 — Production hardening and v1 release

**Priority:** P0 before v1 tag

### Work
- branch protection and required checks,
- coverage thresholds based on risk, not vanity,
- security review,
- dependency/SBOM scan,
- package install matrix,
- schema migration fixtures,
- load and soak tests for server mode,
- network-failure/provider-failure drills,
- privacy/log inspection,
- clean-room installation docs,
- changelog/release automation,
- backup/export/recovery docs,
- release candidate human MQM review.

### v1 exit
All `ARCHITECTURE_ZERO.md` “production-ready v1” conditions pass.

---

## Cross-phase rules

### Rule 1 — No fake green benchmarks
Echo/dummy backends may test mechanics but their results are labeled synthetic and never counted as translation-quality evidence.

### Rule 2 — No README-first features
A user-facing flag/feature is documented only after executable tests prove it exists.

### Rule 3 — No heavy base dependency
Torch/Whisper/COMET/LibreOffice/server frameworks remain extras.

### Rule 4 — Every model call has provenance
Provider, model, prompt/profile version, context hash, retries, and usage metadata are recorded.

### Rule 5 — Every semantic auto-fix is justified
If a rule can change meaning, it is a diagnostic or model-assisted review, not an unconditional regex replacement.

### Rule 6 — Architecture drift requires ADR
No “small shortcut” can bypass locked boundaries.
