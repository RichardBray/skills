# questions

Ask a few casual clarifying questions before acting, when a message ends with a question or is open-ended/ambiguous. Lighter and more conversational than a full "grill me" interview.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill questions
```

## Usage

```
/questions
```

Or end a message with a question mark - that's a soft trigger the model may or may not pick up, so use `/questions` when you want it guaranteed:

```
Should I put this validation in the API or the frontend?
```

If there's real ambiguity, asks 1-3 casual questions (with a recommended answer alongside each) and waits for a response before implementing. If nothing's actually unclear, says so and proceeds.
