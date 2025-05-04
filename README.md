# Mindloop MCP

**MindLoop** allows AI agents to employ spaced repitition learning through an MCP server. Particularly, it uses the Free Spaced Repetition Scheduler (FSRS) algorithm to model memory/forgetting.

## Getting started

- Go to https://mindloop.net to get an API key.
- Set it as MINDLOOP_API_KEY environment variable, or if you prefer, you can change the default API key used by changing the default value away from "FILL_ME_IN".
- On https://mindloop.net or using the API, load in CSV data of facts that you want the AI agent to help with memorizing.
- When configuring your MCP server, use the prompt:

```
Test me one at a time, grabbing one question at a time from MindLoop. Use cloze deletions when testing me, and do not reveal the answer ahead of time. Always record whether I recalled or not. In the case that I get it correct, you should also record the ease with which I got it correctly.
```
