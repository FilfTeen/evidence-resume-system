# Schema Guide

The schemas describe a neutral claim bundle. They are intentionally compact so that validation behavior is easy to inspect.

## Evidence Items

Evidence items use stable identifiers, a generic kind, a neutral summary, and optional support notes. They should describe review support at a high level instead of storing raw material.

## Claims

Claims contain a statement, a status, and evidence identifiers. A claim is valid only when each listed evidence identifier exists in the bundle.

## Decisions

Decisions record review outcomes for claims. Allowed statuses are `approved`, `blocked`, and `reviewRequired`.

## Report Settings

Report settings define the title and section order for deterministic Markdown output. Titles should describe the review output rather than a person, organization, or application.
