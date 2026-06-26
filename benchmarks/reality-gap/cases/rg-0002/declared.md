# Declared State — rg-0002

## Protected Code Review Requirement

All changes to protected application code must be introduced through a pull request.

A pull request must receive at least one reviewer approval before merge.

Direct commits to the protected branch are not permitted except through a documented emergency exception.

## Protected Branch

The `main` branch is the protected branch for application code.

Changes to files under `src/app/`, `src/core/`, and `src/infra/` are considered protected application code.

## Emergency Exception

Emergency changes may bypass standard pull request review only if:

1. the emergency condition is documented,
2. the approving authority is recorded,
3. post-change review is scheduled,
4. and the exception is linked to the commit record.

## Declared Distinctions

- Merged is not equivalent to reviewed.
- Passing CI is not equivalent to peer approval.
- Technical ability to commit does not imply process permission.
- Emergency exception requires documented authority.
- Completion of merge does not imply settlement of governance requirements.

## Declared Constraint

Protected application code must not be changed on `main` without pull request review or documented emergency exception.