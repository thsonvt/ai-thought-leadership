---
title: 'Compound Engineering Camp: Every Step, From Scratch'
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/compound-engineering-camp-every-step-from-scratch
published: '2026-03-13'
fetched: '2026-03-14'
topics:
- AI in Software Engineering
- Compound Engineering
- Software Development
- Coding Efficiency
key_quotes:
- text: So he decided to create a system that would remember—one that plans before
    it codes, reviews outputs to enforce his taste, and stores every lesson so the
    AI applies it next time.
  context: Describing Kieran's motivation for creating the compound engineering system.
- text: The official compound engineering plugin has more than 10,000 GitHub stars
    and is used by a growing community of builders, including engineers at Google
    and Amazon, who say it changed how they think about software.
  context: Highlighting the impact and adoption of the compound engineering plugin
    among the software development community.
- text: The plugin’s compounding step stores lessons as artifacts that future agents
    can discover, the core of compound engineering.
  context: Explaining the fundamental principle behind compound engineering, where
    learnings are stored and reused.
stance:
  compound_engineering_plugin: positive
  Cora: positive
  Claude_Code: neutral
evolution_note: This article represents a deep dive into the practical application
  and benefits of compound engineering, indicating a mature phase of exploration and
  advocacy.
tags:
- compound-engineering
- software-development
- ai
- coding-efficiency
- plugin
- innovation
---

# Compound Engineering Camp: Every Step, From Scratch

**Author**: Dan Shipper (Every)  
**Published**: 2026-03-13  
**Source**: [https://every.to/source-code/compound-engineering-camp-every-step-from-scratch](https://every.to/source-code/compound-engineering-camp-every-step-from-scratch)

---

<table><tr><td><img alt="Source Code" src="https://d24ovhgu8s7341.cloudfront.net/uploads/publication/logo/99/small_Frame_9121.png" /></td><td></td><td><table><tr><td>by <a href="https://every.to/@katie.parrott12">Katie Parrott</a></td></tr><tr><td>in <a href="https://every.to/source-code">Source Code</a></td></tr></table></td></tr></table><figure><img src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/3970/full_page_cover_Compound_Engineering_Camp__The_Full_Loop__Live.png" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>TL;DR: </em><strong><em><u><a href="https://cora.computer/" rel="noopener noreferrer" target="_blank">Cora</a></u></em></strong><em> general manager </em><strong><em><u><a href="https://every.to/@kieran_1355" rel="noopener noreferrer" target="_blank">Kieran Klaassen</a></u></em></strong><em> has written prolifically about <u><a href="https://every.to/source-code/compound-engineering-the-definitive-guide" rel="noopener noreferrer" target="_blank">compound engineering</a></u>, his philosophy of software engineering for the AI age. In this piece, based on a camp he gave for paid subscribers a few weeks ago, we get an inside look at how exactly Kieran builds with the compound engineering plugin for the first time. He walks through, step by step, the process of going from a single prompt to a working app in under an hour. If you’ve been curious about how to build with compound engineering, this is the piece to read.—<u><a href="https://residenceinnbymarriottphiladelphiabalacynwyd.reservationstays.com/hotels/lMVXOwZj?utm_source=adwords_semro&amp;utm_campaign=G%3ARS%3AUS%3APMAX%3ADSA-Chains%3AUS%3AEN&amp;gad_source=1&amp;gad_campaignid=21191562182&amp;gbraid=0AAAAAo1QcNk9-_L5jMXja7zRKGllt1NBQ&amp;gclid=CjwKCAjw687NBhB4EiwAQ645dmbNhmZp29zw6xIQJVuhLZo6e0f98Lfj638CAlZ8EQfzpy7hQxr2vhoC3-oQAvD_BwE&amp;redirect_auth_retry=true&amp;expand_params=false" rel="noopener noreferrer" target="_blank">Kate Lee</a></u></em></p><p><em>Was this newsletter forwarded to you?<a href="https://every.to/account" rel="noopener noreferrer" target="_blank"> </a><u><a href="https://every.to/account" rel="noopener noreferrer" target="_blank">Sign up</a></u> to get it in your inbox.</em></p><p></p><hr class="quill-line" /><p></p><p>This time last year, any time <strong><a href="https://every.to/@kieran_1355" rel="noopener noreferrer" target="_blank">Kieran Klaassen</a></strong> opened a new session in Claude Code, he started from scratch. The lessons from his past code reviews, the style preferences he’d painstakingly explained, and the bugs he’d already flagged—Kieran remembered them all, but from the machine’s perspective, it was like it had never happened.</p><p>He’d been building <strong><u><a href="https://cora.computer/" rel="noopener noreferrer" target="_blank">Cora</a></u></strong>, Every’s AI email assistant, and getting tired of copy-pasting the same prompts, correcting the same overengineered tests, and flagging the same bugs. “A human would remember,” Kieran said. “The AI wouldn’t.”</p><p>So he decided to create a system that <em>would </em>remember—one that plans before it codes, reviews outputs to enforce his taste, and stores every lesson so the AI applies it next time. The result is what we now know as <u><a href="https://every.to/guides/compound-engineering" rel="noopener noreferrer" target="_blank">compound engineering</a></u>, a signature approach to coding with AI where every bug, fix, and code review makes the system permanently smarter. The official <u><a href="https://github.com/EveryInc/compound-engineering-plugin" rel="noopener noreferrer" target="_blank">compound engineering plugin</a></u> has more than 10,000 GitHub stars and is used by a growing community of builders, including engineers at Google and Amazon, who say it changed how they think about software.</p><p>At our first <u><a href="https://every.to/events/compound-engineering-camp" rel="noopener noreferrer" target="_blank">Compound Engineering Camp</a></u>, Kieran walked subscribers through the full loop live, building an app from a one-line prompt to a working product in under an hour. Below is the workflow as Kieran demo-ed it, plus what it means for how software gets built from here.</p><h5><strong>Key takeaways</strong></h5><ol><li><span class="ql-ui" contenteditable="false"></span><strong>Brainstorm before you plan.</strong> The plugin has a brainstorm step that interviews you collaboratively and fills the gap between your vague idea and a detailed spec. </li><li><span class="ql-ui" contenteditable="false"></span><strong>Planning should run without you.</strong> Once the requirements of the project are clear, the plugin has a plan step that researches your codebase, checks for existing patterns, surfaces past learnings, and produces an implementation plan with zero additional input needed.</li><li><span class="ql-ui" contenteditable="false"></span><strong>Use different models for different steps.</strong> Kieran uses faster models—such as <u><a href="https://every.to/vibe-check/vibe-check-claude-haiku-4-5-anthropic-cooked" rel="noopener noreferrer" target="_blank">Claude Haiku 4.5</a></u> or <u><a href="https://every.to/vibe-check/vibe-check-gemini-2-5-pro-and-gemini-2-5-flash" rel="noopener noreferrer" target="_blank">Gemini 2.5 Flash</a></u>—for brainstorming, <u><a href="https://every.to/vibe-check/opus-4-6" rel="noopener noreferrer" target="_blank">Opus</a></u> for planning, <u><a href="https://every.to/vibe-check/vibe-check-codex-openai-s-new-coding-agent" rel="noopener noreferrer" target="_blank">Codex</a></u> for implementation, and sometimes Gemini for code review.</li><li><span class="ql-ui" contenteditable="false"></span><strong>Compound when the context is fresh.</strong> The plugin’s compounding step stores lessons as artifacts that future agents can discover, the core of compound engineering. Run it right after something breaks or works—before the AI compacts your conversation and you lose the specifics of what you were talking about.</li></ol><h2><strong>The compound engineering loop</strong></h2><p>A founder who does everything themselves hits a ceiling, Kieran says. The ones who scale are ...</p><p></p><hr class="quill-line" /><p></p><p><strong>Become a <a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a> to unlock this piece and learn about:</strong></p><ol><li><span class="ql-ui" contenteditable="false"></span>Why Kieran argues that writing code is only 30 percent of the job</li><li><span class="ql-ui" contenteditable="false"></span>The fourth step most AI coding workflows skip entirely</li><li><span class="ql-ui" contenteditable="false"></span>How Kieran built a working app in under an hour from one prompt, running 25 agents in parallel </li></ol><div class="quill-button" id="quill-button-1770117651442"><a href="https://every.to/subscribe?source=post_button">Subscribe</a></div><p><hr /></p><p><em><a href="https://every.to/source-code/compound-engineering-camp-every-step-from-scratch">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.

---

## Key Takeaways

### Notable Quotes

> So he decided to create a system that would remember—one that plans before it codes, reviews outputs to enforce his taste, and stores every lesson so the AI applies it next time.

*Context: Describing Kieran's motivation for creating the compound engineering system.*

> The official compound engineering plugin has more than 10,000 GitHub stars and is used by a growing community of builders, including engineers at Google and Amazon, who say it changed how they think about software.

*Context: Highlighting the impact and adoption of the compound engineering plugin among the software development community.*

> The plugin’s compounding step stores lessons as artifacts that future agents can discover, the core of compound engineering.

*Context: Explaining the fundamental principle behind compound engineering, where learnings are stored and reused.*

## Related Topics

- [[topics/ai-in-software-engineering]]
- [[topics/compound-engineering]]
- [[topics/software-development]]
- [[topics/coding-efficiency]]
