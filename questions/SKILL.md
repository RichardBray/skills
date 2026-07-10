---
name: questions
description: Ask the user a few casual clarifying questions before acting. Reliable trigger is the explicit /questions command. Soft trigger is the message's last character being a question mark, but that's a phrase-match heuristic the model may miss - use /questions when you want it guaranteed. Lighter, more conversational sibling of "grill me" style interviews - not relentless, just a couple of genuine questions to sharpen the request before doing work.
---

# Questions

Primary trigger: the explicit `/questions` command. This is deterministic - always invoke when typed, same as `/wdyt`.

Soft trigger: the message's **last character** is a literal "?" (not a question mark anywhere earlier in the message). This is a phrase-match heuristic, not a hook - the model can miss it. If reliable triggering matters, use `/questions` instead of relying on this.

If the trailing token is "wdyt" (with or without a "?"), that's the `wdyt` skill instead, not this one - don't double-trigger both.

When triggered, before diving into implementation:

1. Skim the request for real ambiguity - things that would change what you build or how (scope, approach, priorities, missing constraints). Don't invent ambiguity that isn't there.
2. If nothing is genuinely unclear, say so in one line and proceed. Don't force questions for the sake of it.
3. If there's something worth asking, ask 1-3 casual questions - conversational tone, not an interrogation. Offer your best guess/recommendation alongside each question so the user can just confirm rather than having to think from scratch.
4. Ask them together if they're independent, or one at a time if later questions depend on earlier answers. Use your judgment - this isn't a rigid one-at-a-time interview like a full "grilling" session.
5. Wait for the user's answers before starting implementation.

This is casual, not relentless: a couple of genuine questions to remove ambiguity, not an exhaustive walk down every branch of a design tree. If the user seems to want more rigor ("grill me on this"), that's a different, more thorough mode - not this one.
