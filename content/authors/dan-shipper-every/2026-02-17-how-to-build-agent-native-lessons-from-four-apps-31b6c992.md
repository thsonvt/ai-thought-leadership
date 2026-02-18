---
title: 'How to Build Agent-native: Lessons From Four Apps'
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/how-to-build-agent-native-lessons-from-four-apps
published: '2026-02-17'
fetched: '2026-02-18'
topics:
- Experimentation in AI
- AI in Software Development
- Software Design Principles
- Agent-native Architecture
key_quotes:
- text: Nobody programmed it to do any of this.
  context: Describing how an app with agent-native architecture operates without explicit
    programming for specific tasks.
- text: The AI is the app.
  context: Summarizing the core principle of agent-native architecture where AI takes
    the central role in application functionality.
- text: Rules belong in the tools, not the instructions.
  context: Highlighting a design principle in agent-native architecture to embed safeguards
    within tools rather than relying on AI to interpret instructions safely.
stance:
  agent-native_architecture: positive
  claude_code: positive
evolution_note: This article represents a deep dive into the practical applications
  and philosophies behind agent-native architecture, indicating a shift towards more
  AI-centric software development.
tags:
- agent-native
- ai-development
- software-architecture
- innovation
- ai-tools
- software-experimentation
---

# How to Build Agent-native: Lessons From Four Apps

**Author**: Dan Shipper (Every)  
**Published**: 2026-02-17  
**Source**: [https://every.to/source-code/how-to-build-agent-native-lessons-from-four-apps](https://every.to/source-code/how-to-build-agent-native-lessons-from-four-apps)

---

<table><tr><td><img alt="Source Code" src="https://d24ovhgu8s7341.cloudfront.net/uploads/publication/logo/99/small_Frame_9121.png" /></td><td></td><td><table><tr><td>by <a href="https://every.to/@katie.parrott12">Katie Parrott</a></td></tr><tr><td>in <a href="https://every.to/source-code">Source Code</a></td></tr></table></td></tr></table><figure><img src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/3940/full_page_cover_How_to_Build_Agent-Native.png" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>Was this newsletter forwarded to you? <u><a href="https://every.to/account" rel="noopener noreferrer" target="_blank">Sign up</a></u> to get it in your inbox.</em></p><p></p><hr class="quill-line" /><p></p><p><strong><u><a href="https://every.to/@danshipper" rel="noopener noreferrer" target="_blank">Dan Shipper</a></u></strong> scanned a page from <strong>Erik Larson</strong>’s <strong>Winston Churchill</strong> biography, <em>The Splendid and the Vile,</em> and pressed save. The app he was demo-ing identified the book, generated a summary, and produced character breakdowns calibrated to exactly where he was in the story—no spoilers past page 203.</p><p>Nobody programmed it to do any of this.</p><p>Instead, Dan’s app has a handful of basic tools—“read file,” “write file,” and “search the web”—and an AI agent smart enough to combine them in a way that matches the user’s request. When it generates a summary, for example, that’s the agent deciding on its own to search the web, pull in relevant information, and write a file that the app displays.</p><p>This is what we call <u><a href="https://every.to/chain-of-thought/agent-native-architectures-how-to-build-apps-after-the-end-of-code" rel="noopener noreferrer" target="_blank">agent-native architecture</a></u>—or, in Dan’s shorthand, “<u><a href="https://every.to/context-window/claude-code-in-a-trenchcoat" rel="noopener noreferrer" target="_blank">Claude Code in a trench coat</a></u>.” On the surface, it looks like regular software, but instead of pre-written code dictating every move the software makes, each interaction routes to an underlying agent that figures out what to do. There’s still code involved—it makes up the interface and defines the tools that are available to the agent. But the agent decides which tools to use and when, combining them in ways the developer never explicitly programmed. </p><p>At our first Agent Native Camp, Dan and the general managers of our software products <strong><u><a href="https://cora.computer/" rel="noopener noreferrer" target="_blank">Cora</a></u></strong>, <strong><u><a href="https://makeitsparkle.co/" rel="noopener noreferrer" target="_blank">Sparkle</a></u></strong>, and <strong><u><a href="https://monologue.to/" rel="noopener noreferrer" target="_blank">Monologue</a></u></strong> shared how they’re each building in light of this fundamental shift. They’re working at different scales and with different constraints, so they’re drawing the lines in different places. Here’s what they shared about how the architecture works, what it looks like in production, and what goes wrong when you get it right.</p><h5><strong>Key takeaways</strong></h5><ol><li><span class="ql-ui" contenteditable="false"></span><strong>The AI is the app.</strong> Instead of coding every feature, you define a few simple tools the AI is allowed to use—for instance, read a file, write a file, and search the web. When you ask it to do something, it decides on its own which tools to reach for and how to combine them.</li><li><span class="ql-ui" contenteditable="false"></span><strong>Simpler tools get smarter results.</strong> The smaller and more basic you make each tool, the more creatively the AI combines them. Claude Code is powerful because its core tool—running terminal commands—can do almost anything.</li><li><span class="ql-ui" contenteditable="false"></span><strong>Rules belong in the tools, not the instructions.</strong> You can ask an AI to be careful, but it might ignore you. If an action is irreversible—like deleting files—the safeguard has to be built into the tool itself.</li><li><span class="ql-ui" contenteditable="false"></span><strong>You don’t have to start over to start learning.</strong> Give the AI a safe space to interact with your existing app and experiment outside the live product. You’ll learn what the agent needs without risking what already works. Just don’t get attached to the code—as models improve, expect to throw things out and rebuild every few months. </li></ol><h2><strong>How agent-native works</strong></h2><p>Traditional software can only do what it’s explicitly programmed to do by its code. Click “sort by date,” and it sorts by date. Click “export,” and you get a CSV. It will never spontaneously summarize your inbox or reorganize your files by topic—unless someone wrote the code for that exact feature.</p><p>Instead of coded features, an agent-native app has tools (small, discrete actions like “read file” or “delete item”) and skills (instructions written in plain English that describe how to combine those tools). An agent uses those tools and skills to produce an outcome that you specify, such as identifying what book you are reading from one page. </p><p>Three principles make this work: </p><p></p><hr class="quill-line" /><p></p><p><strong>Become a <a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a> to unlock this piece and learn about:</strong></p><ol><li><span class="ql-ui" contenteditable="false"></span>Why Yash’s AI agent went into “god mode”—and why rewriting the prompt didn’t stop it</li><li><span class="ql-ui" contenteditable="false"></span>Why the most radical agent-native architecture looks like it was built in 1995</li><li><span class="ql-ui" contenteditable="false"></span>A simple test for whether you’ve built an agent-native app, or just a chatbot with extra steps</li></ol><div class="quill-button" id="quill-button-1770117651442"><a href="https://every.to/subscribe?source=post_button">Subscribe</a></div><p><hr /></p><p><em><a href="https://every.to/source-code/how-to-build-agent-native-lessons-from-four-apps">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.

---

## Key Takeaways

### Notable Quotes

> Nobody programmed it to do any of this.

*Context: Describing how an app with agent-native architecture operates without explicit programming for specific tasks.*

> The AI is the app.

*Context: Summarizing the core principle of agent-native architecture where AI takes the central role in application functionality.*

> Rules belong in the tools, not the instructions.

*Context: Highlighting a design principle in agent-native architecture to embed safeguards within tools rather than relying on AI to interpret instructions safely.*

## Related Topics

- [[topics/experimentation-in-ai]]
- [[topics/ai-in-software-development]]
- [[topics/software-design-principles]]
- [[topics/agent-native-architecture]]
