---
type: "CEP Technical Reference"
id: "cep-glossary"
title: "CEP Glossary"
description: "Approved vocabulary for CEP semantic exchange records and their GodSpeed profile use."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - glossary
  - vocabulary
timestamp: "2026-11-20T00:00:00Z"
---

# CEP semantic exchange

CEP gives producers and consumers shared forms for carrying meaning, authority decisions, evidence, and settlement.

## Language

**Semantic Envelope**:
A unit of exchange with a declared semantic kind, scope, provenance, and lineage.

**Envelope Profile**:
A named exchange contract that constrains an envelope for a specific purpose.

**Semantic Snapshot**:
An exchange record reporting the represented state of a system, organization or model at a particular point. In the GodSpeed profile it reports a model's represented form and validation at a particular revision; an invalid snapshot can report diagnostics without an available model representation.

**Context Bundle**:
An exchange record carrying bounded, source-attributed context and uncertainty for a consumer.

**Execution Trace**:
An attributed record of execution activity and its immediate outcome.

**Evidence Packet**:
An exchange record carrying material relevant to a stated question or claim, with its evidentiary basis and provenance.

**Settlement Packet**:
An exchange record carrying a judgment, its basis, and the authority and scope to which it applies.

**World Transition**:
The exchange record of a movement of work from one pinned Semantic World revision to another. The record does not itself establish permission: any required authority decision is made separately and referenced from the record.

**Uncertainty**:
A declared limit on what the exchange’s evidence establishes, including an unresolved alternative or an incomplete observation.

## Sources and boundary

The [envelope specification](spec/CEP-0008-semantic-envelope.md), [evidence model](spec/CEP-0006-evidence-model.md), [settlement model](spec/CEP-0007-settlement-model.md), and [GodSpeed profiles](spec/profiles/GODSPEED-PROFILES-v1.md) govern these terms. The scoped `world_ref` carries the [DomainForge World Reference contract](https://github.com/GodSpeedAI/DomainForge/blob/35c4ed1/docs/reference/sea-application-contract.md#L931-L957).

An Execution Trace can supply material for an Evidence Packet. A Settlement Packet carries a judgment under its own authority and evidentiary basis. SEA-Forge’s E6 work-contract settlement and its CEP operation settlement differ in subject, admissibility and finality. A Context Bundle can reference material from a Context Kernel Context Packet, but the two are independently scoped.
