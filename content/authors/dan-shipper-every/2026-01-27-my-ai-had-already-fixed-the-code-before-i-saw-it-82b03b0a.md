---
title: My AI Had Already Fixed the Code Before I Saw It
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it-f4a29a07-ea95-409f-bcb2-487a970bed4a
published: '2026-01-27'
fetched: '2026-01-29'
evolution_note: This article represents a paradigm shift towards embracing AI as a
  proactive, self-improving partner in coding.
topics:
- AI Agents
- Claude Code
- Test-Driven Development (TDD)
- Compounding Engineering
tags:
- ai-in-software-development
- code-review
- machine-learning
- software-engineering
- automation
key_quotes:
- text: Before I opened my laptop, the code had reviewed itself.
  context: Expressing the efficiency and effectiveness of using AI for code review
    and improvement.
- text: It felt like cheating, but it wasn\u2019t\u2014it was compounding.
  context: Explaining the concept of compounding engineering where initial efforts
    in training AI lead to self-improving systems.
- text: 'Compounding engineering asks for an upfront investment: You have to teach
    your tools before they can teach themselves.'
stance:
  TDD: neutral
  claude_code: positive
  compounding_engineering: positive
---

# My AI Had Already Fixed the Code Before I Saw It

**Author**: Dan Shipper (Every)  
**Published**: 2026-01-27  
**Source**: [https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it-f4a29a07-ea95-409f-bcb2-487a970bed4a](https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it-f4a29a07-ea95-409f-bcb2-487a970bed4a)

---

<table><tr><td><img alt="Source Code" src="https://d24ovhgu8s7341.cloudfront.net/uploads/publication/logo/99/small_Frame_9121.png" /></td><td></td><td><table><tr><td>by <a href="https://every.to/@kieran_1355">Kieran Klaassen</a></td></tr><tr><td>in <a href="https://every.to/source-code">Source Code</a></td></tr></table></td></tr></table><figure><img src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/3901/full_page_cover_My_AI_Had_Already_Fixed_the_Code_Before_I_Saw_It.png" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>While we’re on our Think Week offsite this week, we’re resurfacing </em><strong><em><u><a href="https://cora.computer/" rel="noopener noreferrer" target="_blank">Cora</a></u></em></strong><em> general manager </em><strong><em><u><a href="https://every.to/@kieran_1355" rel="noopener noreferrer" target="_blank">Kieran Klaassen</a></u></em></strong><em>’s work on the theme of compound engineering. In this piece, Kieran lays out his definition of the term and the shift it represents: What if your AI tools learned—and autonomously applied those lessons to future work? That’s what happened when his Claude Code agent incorporated three months of prior feedback without being asked. The future of development is self-improving systems, not just faster coding.—<u><a href="https://every.to/on-every/kate-lee-joins-every-as-editor-in-chief" rel="noopener noreferrer" target="_blank">Kate Lee</a></u></em></p><p><em>Was this newsletter forwarded to you? <u><a href="https://every.to/account" rel="noopener noreferrer" target="_blank">Sign up</a></u> to get it in your inbox.</em></p><p></p><hr class="quill-line" /><p></p><p>Before I opened my laptop, the code had reviewed itself.</p><p>I launched GitHub expecting to dive into my usual routine—flag poorly named variables, trim excessive tests, and suggest simpler ways to handle errors. Instead, I found a few strong comments from <u><a href="https://www.anthropic.com/claude-code" rel="noopener noreferrer" target="_blank">Claude Code</a></u>, the AI that writes and edits in my terminal:</p><p>“Changed variable naming to match pattern from PR [pull request] #234, removed excessive test coverage per feedback on PR #219, added error handling similar to approved approach in PR #241.”</p><p>In other words, Claude had learned from three prior months of code reviews and applied those lessons without being asked. It had picked up my tastes thoroughly, the way a sharp new teammate would—and with receipts.</p><p>It <u><a href="https://every.to/working-overtime/ai-phobia-is-really-just-fear-that-easier-equals-cheating" rel="noopener noreferrer" target="_blank">felt like cheating</a></u>, but it wasn’t—it was compounding. Every time we fix something, the system learns. Every time we review something, the system learns. Every time we fail in an avoidable way, the system learns. That’s how we build <strong><u><a href="https://cora.computer/" rel="noopener noreferrer" target="_blank">Cora</a></u></strong>, Every’s AI-enabled email assistant, now: Create systems that create systems, then get out of the way.</p><p>I call this <strong>compounding engineering</strong>: building self-improving development systems where each iteration makes the next one faster, safer, and better.</p><p>Typical AI engineering is about short-term gains. You prompt, it codes, you ship. Then you start over. Compounding engineering is about building systems with memory, where every pull request teaches the system, every bug becomes a permanent lesson, and every code review updates the defaults. AI engineering makes you faster today. Compounding engineering makes you faster tomorrow, and each day after.</p><p>Three months of compounding engineering on Cora have completely changed the way I think about code. I can’t write a function anymore without thinking about whether I’m teaching the system or just solving today’s problem. Every bug fix feels half-done if it doesn’t prevent its entire category going forward, and code reviews without extractable lessons seem like wasted time.</p><p>When you’re done reading this, you’ll have the same affliction.</p><h2><strong>The 10-minute investment that pays dividends forever</strong></h2><p>Compounding engineering asks for an upfront investment: You have to teach your tools before they can teach themselves.</p><p>Here’s an example of how this works in practice: I’m building a “frustration detector” for Cora; the goal is for our AI assistant to notice when users get annoyed with the app’s behavior and automatically file improvement reports. A traditional approach would be to write the detector, test it manually, tweak, and repeat. This takes significant expertise and time, a lot of which is spent context-switching between thinking like a user and thinking like a developer. It’d be better if the system could teach itself.</p><p>So I start with a sample conversation where I express frustration—like repeatedly asking the same question with increasingly terse language. Then I hand it off to Claude with a simple prompt: “This conversation shows frustration. Write a test that checks if our tool catches it.”</p><p>Claude writes the test. The test fails—the natural first step in <u><a href="https://en.wikipedia.org/wiki/Test-driven_development" rel="noopener noreferrer" target="_blank">test-driven development (TDD)</a></u>. Next, I tell Claude to write the actual detection logic. Once written, it still doesn’t work perfectly, which is also to be expected. Now here’s the beautiful part: I can tell Claude to <em>iterate on the frustration detection prompt </em>until the test passes.</p><p>Not only that—it can keep iterating. Claude adjusts the prompt and runs the test again. It reads the logs, sees why it missed a frustration signal, and adjusts again. After a few rounds, the test passes. </p><p>But AI outputs aren’t deterministic—a prompt that works once might fail the next time.</p><p>So I have Claude run the test 10 times. When it only identifies frustration in four out of 10 passes, Claude analyzes why it failed the other six times. It studies the <u><a href="https://every.to/also-true-for-humans/7-22" rel="noopener noreferrer" target="_blank">chain of thought</a></u> (the step-by-step thinking Claude showed when deciding whether someone was frustrated) from each failed run and discovers a pattern: It’s missing hedged language a user might use, like, “Hmm, not quite,” which actually signals frustration when paired with repeated requests. Claude then updates the original frustration-detection prompt to specifically look for this polite-but-frustrated language.</p><p>On the next iteration, it’s able to identify a frustrated user nine times out of 10. Good enough to ship.</p><p>We codify this entire workflow—from identifying frustration patterns to iterating prompts to validation—in CLAUDE.md, the special file Claude pulls in for context before each conversation. The next time we need to detect a user’s emotion or behavior, we don’t start from scratch. We say: “Use the prompt workflow from the frustration detector.” The system already knows what to do.</p><p>And unlike human-written code, the “implementation” here is a prompt that Claude can endlessly refine based on test results. Every failure teaches the system. Every success becomes a pattern. (We’re planning to open-source this prompt testing framework so other teams can build their own compounding workflows.)</p><h2><strong>From terminal to mission control</strong></h2><p>Most engineers treat AI as an extra set of hands. Compounding engineering turns it into an entire team that gets faster, sharper, and more aligned with every task.</p><p>At Cora, we’ve used this approach to:...</p><p></p><hr class="quill-line" /><p></p><p><strong>Become a <a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a> to unlock this piece and learn:</strong></p><ol><li><span class="ql-ui" contenteditable="false"></span>Exactly how Kieran has used compounding engineering to build Cora</li><li><span class="ql-ui" contenteditable="false"></span>His five-step compounding engineering playbook</li><li><span class="ql-ui" contenteditable="false"></span>How to work with three agents at once</li></ol><div class="quill-button" id="undefined"><a href="https://every.to/subscribe?source=post_button">Upgrade to paid</a></div><p><hr /></p><p><em><a href="https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it-f4a29a07-ea95-409f-bcb2-487a970bed4a">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.

---

## Key Takeaways

### Notable Quotes

> Before I opened my laptop, the code had reviewed itself.

*Context: Describing the author's experience with Claude Code autonomously improving code based on past feedback.*

> It felt like cheating, but it wasn’t—it was compounding.

*Context: Expressing the efficiency and effectiveness of using AI for code review and improvement.*

> Compounding engineering asks for an upfront investment: You have to teach your tools before they can teach themselves.

*Context: Explaining the concept of compounding engineering where initial efforts in training AI lead to self-improving systems.*

## Related Topics

- [[topics/ai-agents]]
- [[topics/claude-code]]
- [[topics/test-driven-development-tdd]]
- [[topics/compounding-engineering]]
