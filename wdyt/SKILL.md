---
name: wdyt
description: Give an honest opinion without implementing anything, when a user message ends with "wdyt", "wdyt?", or "what do you think" (also "what do you think?"). Use this instead of jumping to a plan or code. Surfaces concerns, tradeoffs, and clarifying questions, then waits for the user's response before doing any work.
---

# wdyt

Trigger: the message ends with "wdyt" or "what do you think" (any casing/punctuation) used as the user's own sign-off asking for an opinion - not the phrase appearing as a mention, example, or quote inside an instruction. "should we do X? wdyt" triggers; "make Y behave the same way /wdyt does" does not, even though it ends on the literal string - there the user is instructing you to build something, not asking your opinion.

When triggered:

1. Do NOT write code, edit files, or call EnterPlanMode/ExitPlanMode. This is a conversation turn, not an implementation turn.
2. Give your honest opinion on whatever was asked or proposed. Take a real position, don't just list pros/cons neutrally.
3. Surface any concerns, risks, or things you'd do differently - even if the user didn't ask.
4. Ask any clarifying questions you have. If you have none, say so explicitly rather than skipping the step.
5. End the turn. Wait for the user to respond before taking any action, even if their proposal seemed clearly good.

If the message contains an explicit instruction to also act ("wdyt, then go ahead and do it"), the explicit instruction wins - give the opinion first, then proceed.
