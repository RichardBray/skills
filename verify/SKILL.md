---
name: verify
description: Check a change works end to end in the running app - web apps and sites through Agent Browser, Electrobun desktop apps through their local UI plus computer use for native parts. Use after building a feature or fix, before calling it done, or when asked to test or verify something in the app.
---

# Verify

Drive the real app. Don't stop at unit tests.

**Web app or site**
1. Start it (`bun run dev`) and note the URL.
2. `agent-browser skills get core` for usage, then open the URL and exercise the change the way a user would.
3. Check the console for errors and take a screenshot of the result.

**Electrobun app**
- Unless it bundles CEF, it runs in the system webview, which has no CDP, so Agent Browser can't attach to the window.
- Test the UI through the local server the Bun process serves, with Agent Browser.
- Use computer use only for native parts: the window, menus, file dialogs.

**Then**
- If the project has Playwright end-to-end tests, add or extend a spec for this flow so it stays covered.
- Report what you did, what you saw, and where the screenshots are.
