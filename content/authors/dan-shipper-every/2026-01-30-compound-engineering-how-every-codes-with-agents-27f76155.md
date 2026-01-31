---
title: 'Compound Engineering: How Every Codes With Agents'
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/compound-engineering-how-every-codes-with-agents-af3a1bae-cf9b-458e-8048-c6b4ba860e62
published: '2026-01-30'
fetched: '2026-01-31'
topics:
- AI Agents
- Compound Engineering
- Artificial Intelligence in Development
- Software Engineering
key_quotes:
- text: What happens to software engineering when 100 percent of your code is written
    by agents?
  context: Introduction to the concept of AI agents taking over traditional coding
    tasks.
- text: In traditional engineering, you expect each feature to make the next feature
    harder to build—more code means more edge cases, more interdependencies, and more
    issues that are hard to anticipate.
  context: Contrasting traditional engineering practices with compound engineering.
- text: By contrast, in compound engineering, you expect each feature to make the
    next feature easier to build.
  context: Explaining the core principle of compound engineering.
stance:
  claude_code: positive
  droid: neutral
  codex: neutral
evolution_note: This article represents a paradigm shift in the authors' approach
  to software development, emphasizing the transformative potential of AI in coding.
tags:
- compound-engineering
- ai-coding
- software-development
- ai-agents
- anthropic
- openai
---

# Compound Engineering: How Every Codes With Agents

**Author**: Dan Shipper (Every)  
**Published**: 2026-01-30  
**Source**: [https://every.to/source-code/compound-engineering-how-every-codes-with-agents-af3a1bae-cf9b-458e-8048-c6b4ba860e62](https://every.to/source-code/compound-engineering-how-every-codes-with-agents-af3a1bae-cf9b-458e-8048-c6b4ba860e62)

---

<table><tr><td><img alt="Source Code" src="https://d24ovhgu8s7341.cloudfront.net/uploads/publication/logo/99/small_Frame_9121.png" /></td><td></td><td><table><tr><td>by <a href="https://every.to/@danshipper">Dan Shipper</a> and <a href="https://every.to/@kieran_1355">Kieran Klaassen</a></td></tr><tr><td>in <a href="https://every.to/source-code">Source Code</a></td></tr></table></td></tr></table><figure><img src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/3904/full_page_cover_Compound_Engineering__How_Every_Codes_With_Agents(2).png" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>While we’re on our Think Week offsite this week, we’re resurfacing </em><strong><em><u><a href="https://cora.computer/" rel="noopener noreferrer" target="_blank">Cora</a></u></em></strong><em> general manager </em><strong><em><u><a href="https://every.to/@kieran_1355" rel="noopener noreferrer" target="_blank">Kieran Klaassen</a></u></em></strong><em>’s work on the theme of compound engineering. In this final piece, Kieran teams up with </em><strong><em><u><a href="https://every.to/@danshipper" rel="noopener noreferrer" target="_blank">Dan Shipper</a></u></em></strong><em> to describe how compound engineering allows Every’s lean team to provide multiple software products to thousands of users. They propose a four-step loop (plan, work, review, compound) for software teams writing code with AI so you can create the same development magic. Read on for the complete framework, and learn why planning dominates 80 percent of the process.—<u><a href="https://every.to/on-every/kate-lee-joins-every-as-editor-in-chief" rel="noopener noreferrer" target="_blank">Kate Lee</a></u></em></p><p><em>Was this newsletter forwarded to you? <u><a href="https://every.to/account" rel="noopener noreferrer" target="_blank">Sign up</a></u> to get it in your inbox.</em></p><p></p><hr class="quill-line" /><p></p><p>What happens to software engineering when 100 percent of your code is written by agents? This is a question we’ve had to confront head-on at Every as <u><a href="https://every.to/vibe-check/vibe-check-opus-4-5-is-the-coding-model-we-ve-been-waiting-for" rel="noopener noreferrer" target="_blank">AI coding has become so powerful</a></u>. Nobody is writing code manually. It feels weird to be typing code into your computer or staring at a blinking cursor in a code editor. </p><p>So much of engineering until now assumed that coding is hard and engineers are scarce. Removing those bottlenecks makes traditional engineering practices—like manually writing tests, or laboriously typing human readable code with lots of documentation—feel slow and outdated. In order to deal with these new powers and changing constraints, we’ve created a <u><a href="https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it" rel="noopener noreferrer" target="_blank">new style of engineering</a></u> at Every that we call <strong>compound engineering</strong>. </p><p>In traditional engineering, you expect each feature to make the next feature harder to build—more code means more edge cases, more interdependencies, and more issues that are hard to anticipate. By contrast, in compound engineering, you expect each feature to make the next feature <em>easier </em>to build. This is because compound engineering creates a learning loop for your agents and members of your team, so that each bug,  failed test, or <em>a-ha</em> problem-solving insight gets documented and used by future agents. The complexity of your codebase still grows, but now so does the AI’s knowledge of it, which makes future development work faster.</p><p>And it works. We run five software products in-house (and are incubating a few more), each of which is primarily built and run by a single person. These products are used by thousands of people every day for important work—they’re not just nice demos.</p><p>This shift has huge implications for how software is built at every company, and how ambitious and productive every developer can be: Today, if your AI is used right, a single developer can do the work of five developers a few years ago, based on our experience at Every. They just need a good system to harness its power.</p><p>The rest of this piece will give you a high-level sense of how we practice compound engineering inside of Every. By the time you’re done, you should be able to start doing the basics yourself—and you’ll be primed to go much deeper.</p><h2>Compound engineering loop</h2><p>A compound engineer orchestrates agents running in parallel, who plan, write, and evaluate code. This process happens in a loop that looks like this:</p><ol><li><span class="ql-ui" contenteditable="false"></span><strong>Plan:</strong> Agents read issues, research approaches, and synthesize information into detailed implementation plans.</li><li><span class="ql-ui" contenteditable="false"></span><strong>Work:</strong> Agents write code and create tests according to those plans.</li><li><span class="ql-ui" contenteditable="false"></span><strong>Review: </strong>The engineer reviews the output itself and the lessons learned from the output.</li><li><span class="ql-ui" contenteditable="false"></span><strong>Compound:</strong> The engineer feeds the results back into the system, where they make the next loop better by helping the whole system learn from successes and failures. This is where the magic happens.</li></ol><p>We use Anthropic’s <u><a href="https://every.to/source-code/how-i-use-claude-code-to-ship-like-a-team-of-five" rel="noopener noreferrer" target="_blank">Claude Code</a></u> primarily for compound engineering, but it is tool-agnostic—some members of our team also use startup Factory’s <u><a href="https://every.to/vibe-check/vibe-check-i-canceled-two-ai-max-plans-for-factory-s-coding-agent-droid" rel="noopener noreferrer" target="_blank">Droid</a></u> and OpenAI’s <u><a href="https://every.to/vibe-check/vibe-check-codex-openai-s-new-coding-agent" rel="noopener noreferrer" target="_blank">Codex CLI</a></u>. If you want to get more hands-on with how we do this, we’ve built a <u><a href="https://github.com/EveryInc/compound-engineering-plugin" rel="noopener noreferrer" target="_blank">compound engineering plugin</a></u> for Claude Code that lets you run the exact workflow we use internally yourself. </p><p>Roughly 80 percent of compound engineering is in the plan and review parts, while 20 percent is in the work and compound. </p><p>Let’s dive in.</p><p></p><hr class="quill-line" /><p></p><p><strong>Become a <u><a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a></u> to unlock this piece and learn about:</strong></p><ol><li><span class="ql-ui" contenteditable="false"></span>Why the hardest part of AI coding happens before any code gets written</li><li><span class="ql-ui" contenteditable="false"></span>The “money step” that turns every bug into a permanent advantage</li><li><span class="ql-ui" contenteditable="false"></span>How compound engineering quickly makes new hires as effective as veterans</li></ol><div class="quill-button" id="quill-button-1765469873479"><a href="https://every.to/subscribe?source=post_button">Subscribe</a></div><p><hr /></p><p><em><a href="https://every.to/source-code/compound-engineering-how-every-codes-with-agents-af3a1bae-cf9b-458e-8048-c6b4ba860e62">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.

---

## Key Takeaways

### Notable Quotes

> What happens to software engineering when 100 percent of your code is written by agents?

*Context: Introduction to the concept of AI agents taking over traditional coding tasks.*

> In traditional engineering, you expect each feature to make the next feature harder to build—more code means more edge cases, more interdependencies, and more issues that are hard to anticipate.

*Context: Contrasting traditional engineering practices with compound engineering.*

> By contrast, in compound engineering, you expect each feature to make the next feature easier to build.

*Context: Explaining the core principle of compound engineering.*

## Related Topics

- [[topics/ai-agents]]
- [[topics/compound-engineering]]
- [[topics/artificial-intelligence-in-development]]
- [[topics/software-engineering]]
