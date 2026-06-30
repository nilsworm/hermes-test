# Plan: Add `greet` Helper Function

- **Task ID:** afae37f2-21cb-4f35-aeb8-d4d50d2651c1
- **Date:** 2026-06-30
- **Status:** Ready
- **Author:** Planner Agent (LifeOS autonomous development loop)
- **Spec:** `docs/superpowers/specs/2026-06-30-add-greet-helper-function.md`
- **Spec PR (merged):** https://github.com/nilsworm/hermes-test/pull/1

---

## 1. Overview

Implement a small, dependency-free `greet(name?)` helper that produces a
deterministic greeting string. This is the first reusable helper in the repo,
so it also bootstraps the `src/` layout, a `test/` directory, and a minimal
`package.json` that runs tests via the Node.js built-in test runner
(`node --test`) with **zero third-party dependencies**.

### Behavioural contract (from spec)

| Input                | Output             |
|----------------------|--------------------|
| `"Ada"`              | `"Hello, Ada!"`    |
| `"  Ada  "`          | `"Hello, Ada!"`    |
| `""`                 | `"Hello, there!"`  |
| `"   "`              | `"Hello, there!"`  |
| `undefined` / none   | `"Hello, there!"`  |

### Acceptance criteria (from spec)

1. `greet("Ada")` returns `"Hello, Ada!"`.
2. `greet("  Ada  ")` returns `"Hello, Ada!"` (whitespace trimmed).
3. `greet("")`, `greet("   ")`, and `greet()` all return `"Hello, there!"`.
4. The function is exported as a named ES-module export `greet`.
5. `node --test` passes locally with zero installed dependencies.

---

## 2. Approach

Strict TDD. Each task follows the loop:
**failing test → run to verify fail → implement → run to verify pass → commit.**

Because the test runner depends on `package.json` declaring `"type": "module"`
and a `test` script, we set up that scaffolding first (Task 0) so subsequent
red/green steps run cleanly. The scaffolding task still ends with a runnable
(empty/placeholder) check so the loop stays verifiable.

### File map

| File | Status | Purpose |
|------|--------|---------|
| `package.json` | **new** | Declares `"type": "module"` and `test` script (`node --test`). No dependencies. |
| `src/greet.js` | **new** | Implements and exports the named `greet` helper as an ES module. |
| `test/greet.test.js` | **new** | Unit tests covering the behavioural contract. |
| `.github/workflows/ci.yml` | existing | Optionally extended to run `npm test`. |

---

## 3. Tasks

### Task 0 — Bootstrap project scaffolding (`package.json`)

Goal: create the minimal `package.json` so `node --test` can resolve ES
modules and `npm test` works.

- **Failing test / verify need:**
  Confirm there is no test setup yet.
  ```bash
  test -f package.json && echo "EXISTS" || echo "MISSING"   # expect: MISSING
  node --test 2>&1 | tail -5                                  # expect: no test files / no tests found
  ```
- **Implement:** create `package.json`:
  ```json
  {
    "name": "hermes-test",
    "version": "0.1.0",
    "type": "module",
    "scripts": {
      "test": "node --test"
    }
  }
  ```
- **Run to verify pass:**
  ```bash
  test -f package.json && echo "EXISTS"   # expect: EXISTS
  npm test 2>&1 | tail -5                  # expect: runs node --test (0 tests yet, exits cleanly or "no tests")
  ```
- **Commit:**
  ```bash
  git add package.json
  git commit -m "chore: add minimal package.json with node --test script"
  ```

---

### Task 1 — Happy path: `greet("Ada")` → `"Hello, Ada!"`

- **Write failing test:** create `test/greet.test.js`:
  ```js
  import test from 'node:test';
  import assert from 'node:assert/strict';
  import { greet } from '../src/greet.js';

  test('greets a provided name', () => {
    assert.equal(greet('Ada'), 'Hello, Ada!');
  });
  ```
- **Run to verify fail:**
  ```bash
  npm test 2>&1 | tail -20
  # expect: FAIL — cannot find module '../src/greet.js' (greet not implemented)
  ```
- **Implement:** create `src/greet.js` with the minimal named export:
  ```js
  export function greet(name) {
    return `Hello, ${name}!`;
  }
  ```
- **Run to verify pass:**
  ```bash
  npm test 2>&1 | tail -20   # expect: 1 passing
  ```
- **Commit:**
  ```bash
  git add src/greet.js test/greet.test.js
  git commit -m "feat: add greet helper with happy-path greeting"
  ```

---

### Task 2 — Trim surrounding whitespace: `greet("  Ada  ")` → `"Hello, Ada!"`

- **Write failing test:** append to `test/greet.test.js`:
  ```js
  test('trims surrounding whitespace from the name', () => {
    assert.equal(greet('  Ada  '), 'Hello, Ada!');
  });
  ```
- **Run to verify fail:**
  ```bash
  npm test 2>&1 | tail -20
  # expect: FAIL — got "Hello,   Ada  !" (whitespace not trimmed)
  ```
- **Implement:** update `src/greet.js` to trim:
  ```js
  export function greet(name) {
    const trimmed = (name ?? '').trim();
    return `Hello, ${trimmed}!`;
  }
  ```
- **Run to verify pass:**
  ```bash
  npm test 2>&1 | tail -20   # expect: 2 passing
  ```
- **Commit:**
  ```bash
  git add src/greet.js test/greet.test.js
  git commit -m "feat: trim whitespace from greet input"
  ```

---

### Task 3 — Default fallback: empty / whitespace-only / missing → `"Hello, there!"`

- **Write failing test:** append to `test/greet.test.js`:
  ```js
  test('falls back to "there" for empty string', () => {
    assert.equal(greet(''), 'Hello, there!');
  });

  test('falls back to "there" for whitespace-only string', () => {
    assert.equal(greet('   '), 'Hello, there!');
  });

  test('falls back to "there" when called with no arguments', () => {
    assert.equal(greet(), 'Hello, there!');
  });
  ```
- **Run to verify fail:**
  ```bash
  npm test 2>&1 | tail -20
  # expect: FAIL — got "Hello, !" instead of "Hello, there!"
  ```
- **Implement:** finalize `src/greet.js` with the documented default:
  ```js
  /**
   * Build a friendly greeting message.
   *
   * @param {string} [name] - The name to greet. Leading/trailing
   *   whitespace is trimmed. When omitted, empty, or whitespace-only,
   *   the greeting falls back to "there".
   * @returns {string} A greeting in the form "Hello, <name>!".
   */
  export function greet(name) {
    const trimmed = (name ?? '').trim();
    const target = trimmed === '' ? 'there' : trimmed;
    return `Hello, ${target}!`;
  }
  ```
- **Run to verify pass:**
  ```bash
  npm test 2>&1 | tail -20   # expect: 5 passing
  ```
- **Commit:**
  ```bash
  git add src/greet.js test/greet.test.js
  git commit -m "feat: default greet to 'there' for empty/missing names"
  ```

---

### Task 4 — (Optional) Extend CI to run the test suite

Goal: make the existing PR-triggered workflow run the real suite instead of a
placeholder echo. Keep it dependency-free.

- **Write failing check:** inspect current workflow.
  ```bash
  grep -q "node --test\|npm test" .github/workflows/ci.yml && echo "HAS TESTS" || echo "NO TESTS"
  # expect: NO TESTS
  ```
- **Implement:** update `.github/workflows/ci.yml`:
  ```yaml
  name: CI
  on: [pull_request]
  jobs:
    check:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-node@v4
          with:
            node-version: '20'
        - run: npm test
  ```
- **Run to verify pass:**
  ```bash
  grep -q "npm test" .github/workflows/ci.yml && echo "HAS TESTS"   # expect: HAS TESTS
  npm test 2>&1 | tail -5                                            # expect: all tests passing locally
  ```
- **Commit:**
  ```bash
  git add .github/workflows/ci.yml
  git commit -m "ci: run npm test on pull requests"
  ```

---

## 4. Final Verification

Run the full suite from a clean state and confirm all acceptance criteria:

```bash
npm test 2>&1 | tail -20
# expect: 5 passing, 0 failing, no third-party deps installed
ls node_modules 2>/dev/null && echo "DEPS PRESENT (unexpected)" || echo "NO DEPS (expected)"
```

Checklist mapped to spec acceptance criteria:

- [ ] AC1: `greet("Ada")` → `"Hello, Ada!"` (Task 1)
- [ ] AC2: `greet("  Ada  ")` → `"Hello, Ada!"` (Task 2)
- [ ] AC3: `greet("")`, `greet("   ")`, `greet()` → `"Hello, there!"` (Task 3)
- [ ] AC4: named ES-module export `greet` (Tasks 1–3)
- [ ] AC5: `node --test` passes with zero installed dependencies (Final)

## 5. Risks & Notes

- **No dependencies:** rely solely on `node:test` and `node:assert/strict`.
  Do not add any runtime or dev dependencies.
- **ESM resolution:** `"type": "module"` plus explicit `.js` extensions in
  imports are required for Node ESM; ensure imports use `../src/greet.js`.
- **Nullish handling:** use `name ?? ''` so `undefined` (no argument) is
  handled identically to empty strings, satisfying "safe to call with no
  arguments".
- **Task 4 is optional** per the spec ("may extend it... but this is
  optional"); it can be dropped without affecting acceptance criteria.
