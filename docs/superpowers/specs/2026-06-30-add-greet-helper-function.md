# Spec: Add `greet` Helper Function

- **Task ID:** afae37f2-21cb-4f35-aeb8-d4d50d2651c1
- **Date:** 2026-06-30
- **Status:** Draft
- **Author:** Spec Agent (LifeOS autonomous development loop)

---

## 1. Goal

Provide a small, dependency-free utility function, `greet`, that builds a
friendly greeting message from a person's name. The function must:

- Return a deterministic greeting string for a given name.
- Trim surrounding whitespace from the input name.
- Fall back to a sensible default ("there") when the name is missing, empty,
  or whitespace-only, yielding `"Hello, there!"`.
- Be safe to call with no arguments.

This is the first reusable helper in the repository and establishes the
`src/` layout plus a runnable test setup using only the Node.js standard
library (no third-party dependencies).

### Non-Goals

- No internationalization / localization of the greeting.
- No CLI, HTTP endpoint, or UI integration.
- No support for greeting multiple names in a single call.
- No logging, persistence, or configuration.

---

## 2. Architecture

A single pure function exported from an ES module under `src/`. The function
has no side effects and no external dependencies, making it trivially testable
and importable by future code.

```
                +------------------------+
   name: string |                        |  greeting: string
  ------------->|     greet(name?)       |------------------>
   (optional)   |  - normalize input     |  "Hello, <name>!"
                |  - apply default        |
                +------------------------+
```

Behavioural contract:

| Input                | Output             |
|----------------------|--------------------|
| `"Ada"`              | `"Hello, Ada!"`    |
| `"  Ada  "`          | `"Hello, Ada!"`    |
| `""`                 | `"Hello, there!"`  |
| `"   "`              | `"Hello, there!"`  |
| `undefined` / none   | `"Hello, there!"`  |

Testing uses the built-in `node:test` runner and `node:assert/strict`, so no
package installation is required to run the suite.

---

## 3. File Map

| File | Status | Purpose |
|------|--------|---------|
| `src/greet.js` | **new** | Implements and exports the `greet` helper as an ES module. |
| `test/greet.test.js` | **new** | Unit tests covering the behavioural contract above. |
| `package.json` | **new** | Declares `"type": "module"` and a `test` script (`node --test`). No dependencies. |
| `.github/workflows/ci.yml` | existing | Already runs on `pull_request`; the implementation may extend it to run `npm test`, but this is optional. |

---

## 4. Key Interfaces

### `greet(name?)` — `src/greet.js`

```js
/**
 * Build a friendly greeting message.
 *
 * @param {string} [name] - The name to greet. Leading/trailing
 *   whitespace is trimmed. When omitted, empty, or whitespace-only,
 *   the greeting falls back to "there".
 * @returns {string} A greeting in the form "Hello, <name>!".
 */
export function greet(name) { /* ... */ }
```

- **Default export:** none. Use the named export `greet`.
- **Determinism:** identical inputs always produce identical outputs.
- **Purity:** no I/O, no mutation of inputs, no global state.

### Suggested `package.json` (minimal)

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

---

## 5. Acceptance Criteria

1. `greet("Ada")` returns `"Hello, Ada!"`.
2. `greet("  Ada  ")` returns `"Hello, Ada!"` (whitespace trimmed).
3. `greet("")`, `greet("   ")`, and `greet()` all return `"Hello, there!"`.
4. The function is exported as a named ES-module export `greet`.
5. `node --test` passes locally with zero installed dependencies.
