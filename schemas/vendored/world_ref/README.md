---
type: CEP Guide
id: vendored-world-ref
title: Vendored DomainForge world_ref vectors
description: Byte-for-byte copy of DomainForge's world_ref golden vectors and independent reference, pinned by hash.
status: Draft
version: 0.1.0
tags:
- cep
- world_ref
- vendored
timestamp: '2026-10-04T00:00:00Z'
---

# Vendored DomainForge world_ref vectors

Copied byte-for-byte from DomainForge (`domainforge-core/tests/fixtures/world_ref/`, branch `feat/world-ref`, commit a3a4157). DomainForge defines the `world_ref` grammar; CEP only mirrors it in its profile schemas. `tests/test_godspeed_profiles.py` pins the hashes and checks that the mirrored schema pattern accepts and rejects exactly what these vectors say. Do not edit; re-vendor from DomainForge.
