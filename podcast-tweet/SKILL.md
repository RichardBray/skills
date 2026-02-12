---
name: podcast-tweet
description: Generate an engaging podcast episode tweet with guest handle and topics
user-invocable: true
argument-hint: "[episode description]"
---

Generate an engaging podcast tweet based on the episode description. The tweet must:

- Start with "In the latest podcast episode,"
- Include the guest's Twitter handle (@username)
- Describe the guest's journey and key topics discussed
- List multiple things covered in the episode (comma-separated)
- End with what the guest is building/working on
- Be concise but comprehensive

Format your response as:
In the latest podcast episode, @[handle] tells us [journey and topics], and [what they're building/doing].

Display the tweet in chat only. Do not write to any file.
