# Mindloop MCP

**MindLoop** allows AI agents to employ spaced repitition learning through an MCP server. Particularly, it uses the Free Spaced Repetition Scheduler (FSRS) algorithm to model memory/forgetting.

## Getting started

- Go to https://mindloop.net to get an API key.
- Set it as MINDLOOP_API_KEY environment variable, or if you prefer, you can change the default API key used by changing the default value away from "FILL_ME_IN".
- On https://mindloop.net, paste in text data of facts that you want the AI agent to help with memorizing. Each line should be a fact that you want to memorize. You can also use the API to do this.
- Connect the MCP server in an MCP client, e.g. Claude Desktop. If you have `uv` installed, you can use a `claude_desktop_config.json` like the following:

```
{
    "mcpServers":
    {
        "MindLoop Spaced Repetition":
        {
            "command": "uv",
            "args":
            [
                "run",
                "--with",
                "mcp[cli]",
                "mcp",
                "run",
                "/global/path/to/mindloop-mcp/server.py"
            ]
        }
    }
}
```

- When talking to your MCP-enabled agent, use a prompt like the following:

```
Test me one at a time, grabbing one question at a time from MindLoop. Use cloze deletions when testing me, and do not reveal the answer ahead of time. Do not make too many blanks to the point that the fact becomes unguessable. Always record whether I recalled or not. In the case that I get it correct, you should also record the ease with which I got it correctly.
```

You can modify the above prompt to better match your learning style.
