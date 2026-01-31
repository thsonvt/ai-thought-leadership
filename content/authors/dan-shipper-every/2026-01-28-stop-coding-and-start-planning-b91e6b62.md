---
title: Stop Coding and Start Planning
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/stop-coding-and-start-planning-be0b4fd1-5898-4b09-bfda-0b00ea0004fd
published: '2026-01-28'
fetched: '2026-01-29'
evolution_note: This article represents a paradigm shift, advocating for a more thoughtful
  integration of AI in the software development process.
topics:
- Prompt Engineering
- AI Agents
- Agent-Native Architecture
tags:
- ai-assisted-coding
- software-development
- planning-vs.-coding
- figma
- github
key_quotes:
- text: AI made us sloppy because it made us forget how to plan.
  context: Comparing traditional coding to planning with AI, emphasizing the long-term
    benefits of the latter.
- text: One approach ships a feature. The other ships a feature and teaches the system
    how you think for next time.
  context: Explaining the process of using an AI agent to translate design into actionable
    development plans.
- text: 'I created an AI agent with one job: Take a Figma design screenshot, analyze
    how to implement it, and output a detailed plan grounded in our patterns, components,
    and way of building.'
stance:
  Agent-Native_Architecture: positive
  Prompt_Engineering: positive
---

# Stop Coding and Start Planning

**Author**: Dan Shipper (Every)  
**Published**: 2026-01-28  
**Source**: [https://every.to/source-code/stop-coding-and-start-planning-be0b4fd1-5898-4b09-bfda-0b00ea0004fd](https://every.to/source-code/stop-coding-and-start-planning-be0b4fd1-5898-4b09-bfda-0b00ea0004fd)

---

<table><tr><td><img alt="Source Code" src="https://d24ovhgu8s7341.cloudfront.net/uploads/publication/logo/99/small_Frame_9121.png" /></td><td></td><td><table><tr><td>by <a href="https://every.to/@kieran_1355">Kieran Klaassen</a></td></tr><tr><td>in <a href="https://every.to/source-code">Source Code</a></td></tr></table></td></tr></table><figure><img src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/3902/full_page_cover_Stop_Coding_and_Start_Planning(2).png" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>While we’re on our Think Week offsite this week, we’re resurfacing </em><strong><em><u><a href="https://cora.computer/" rel="noopener noreferrer" target="_blank">Cora</a></u></em></strong><em> general manager </em><strong><em><u><a href="https://every.to/@kieran_1355" rel="noopener noreferrer" target="_blank">Kieran Klaassen</a></u></em></strong><em>’s work on the theme of compound engineering. In this piece, Kieran argues that the best thing you can do to improve your AI-assisted coding is to plan. He introduces a framework for deciding when to plan versus when to prototype, and gives a real example of how one hour of planning saved days of debugging when he wanted to turn some design plans in Figma into a product. So take that extra hour and plan. You’ll thank yourself.—<u><a href="https://every.to/on-every/kate-lee-joins-every-as-editor-in-chief" rel="noopener noreferrer" target="_blank">Kate Lee</a></u></em></p><p><em>Was this newsletter forwarded to you? <u><a href="https://every.to/account" rel="noopener noreferrer" target="_blank">Sign up</a></u> to get it in your inbox.</em></p><p></p><hr class="quill-line" /><p></p><p>AI made us sloppy because it made us forget how to plan. </p><p>Planning used to be a non-negotiable part of the work: sketching screens, prototyping flows, and writing problem statements. You had to define the scope—what’s in, what’s out, what’s too ambitious, and what solves the problem. Good planning required good thinking, good writing, and collaboration between stakeholders. It was slow, but it prevented expensive mistakes.</p><p>When <u><a href="https://every.to/source-code/i-rebuilt-sparkle-in-14-days-with-ai" rel="noopener noreferrer" target="_blank">vibe coding</a></u> emerged, planning went out the window—at first. Why spend an hour planning when you could spend five minutes building the feature? I did it, too. “Make this feature work” was my entire instruction. Sometimes it worked. Often it didn’t. When it didn’t, I’d spend three hours debugging an error that a 10-minute session—asking AI to create a clear outline of the problem and the research needed to build a solution—would have prevented. And I’d be starting from zero with each feature I shipped, instead of the AI improving with each request.</p><p>When you vibe code, you prompt, “Add email validation to the signup form,” and hope the AI takes the right route. When you plan with AI, you write: “Research how we handle validation elsewhere in the codebase, check if our email library has built-in validation, look up best practices for user-friendly error messages, then create a plan showing three approaches with tradeoffs.”</p><p>One approach ships a feature. The other ships a feature <em>and</em> teaches the system how you think for next time. Get this right, and the system learns from every plan. Let me show you how. </p><h2>Plans teach the system—code just solves problems</h2><p>I had five screens of Figma designs staring at me, and a weekend to turn these pixels into a product.</p><p>We were preparing for the launch of <strong><u><a href="https://cora.computer" rel="noopener noreferrer" target="_blank">Cora</a></u></strong>‘s email bankruptcy feature—a free service that clears users’ inbox for them without deleting anything important. <strong><u><a href="https://every.to/@lucascrespo" rel="noopener noreferrer" target="_blank">Lucas Crespo</a></u></strong> and <strong>Daniel Rodrigues</strong>, Every’s designers, had turned my ugly-but-functional flow into those beautiful Figma designs: something people would want to use, with clean layouts, thoughtful interactions, and the kind of polish that sets <u><a href="https://every.to/source-code/build-places-not-products" rel="noopener noreferrer" target="_blank">software that delights</a></u> apart from software that works. Now I had to build it.</p><p>As recently as early 2025, that would have meant: Hook up the Figma MCP plugin (a tool that connects design files to code), watch it produce something vaguely related to the design but mostly ugly, then spend the weekend manually fixing it—squinting at measurements, guessing at spacing, writing HTML, refreshing the browser, noticing it’s wrong, adjusting, repeating. Days of work and frustration. </p><p>This time, instead of coding all weekend, I spent one hour that saved me days. </p><p>I created an AI agent with one job: Take a Figma design screenshot, analyze how to implement it, and output a detailed plan grounded in our patterns, components, and way of building. </p><div class="quill-block-image" id="quill-block-image-1768931608876"><div><a href="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/posts/3815/optimized_f0c2b5f3-3949-4395-84b3-05bbadabae81.png" rel="noopener noreferrer" target="_blank"><img alt="My agent analyzed the Figma design and produced this implementation plan, automatically stored in GitHub. (All screenshots courtesy of the author.)" src="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/posts/3815/optimized_f0c2b5f3-3949-4395-84b3-05bbadabae81.png" /></a><figcaption class="quill-image-caption">My agent analyzed the Figma design and produced this implementation plan, automatically stored in GitHub. (All screenshots courtesy of the author.)</figcaption></div></div><p><br /></p><p>Once the plan was complete, I added a second agent to review the work: Compare the Figma screenshot to what got built using Puppeteer (a tool that automatically captures screenshots of web interfaces), note every difference, and keep iterating until they match. Because the plan was clear and detailed, the review agent could focus entirely on execution, instead of trying to figure out what we were even building.</p><p>I got five screens, pixel-perfect, including mobile layouts that were never even designed for. The plan guided the work step, and pixel perfection came out the other side. </p><div class="quill-block-image" id="quill-block-image-1768931608877"><div><a href="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/posts/3815/optimized_7709bb99-87a2-44b6-a585-5ecf99bd9d90.png" rel="noopener noreferrer" target="_blank"><img alt="The new email bankruptcy flow I built with help from my planning agent." src="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/posts/3815/optimized_7709bb99-87a2-44b6-a585-5ecf99bd9d90.png" /></a><figcaption class="quill-image-caption">The new email bankruptcy flow I built with help from my planning agent.</figcaption></div></div><p><br /></p><p>The next time we need to implement a complex interface, I won’t start from scratch. I’ll use the same system and the same planning workflow, and it will be faster because the system learned from this round.</p><p>This is <u><a href="https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it" rel="noopener noreferrer" target="_blank">compounding engineering</a></u>: building systems where every unit of work makes the next one easier because you’re teaching the AI what to do. And the fastest way to teach is not through code you write, but through plans you review.</p><h2><strong>How to plan effectively: Remember the three fidelities </strong></h2><p>The first step to planning effectively...</p><p></p><hr class="quill-line" /><p></p><p><strong>Become a <a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a> to unlock this piece and learn about:</strong></p><ol><li><span class="ql-ui" contenteditable="false"></span>Why Kieran sorts engineering work into three buckets—and spends no planning time on two of them</li><li><span class="ql-ui" contenteditable="false"></span>The week he built three prototypes to prove the simple solution wouldn’t work</li><li><span class="ql-ui" contenteditable="false"></span>How one HTML correction taught his system more than 50 features worth of code</li></ol><div class="quill-button" id="quill-button-1761066861282"><a href="https://every.to/subscribe?source=post_button">Upgrade to paid</a></div><p><hr /></p><p><em><a href="https://every.to/source-code/stop-coding-and-start-planning-be0b4fd1-5898-4b09-bfda-0b00ea0004fd">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.

---

## Key Takeaways

### Notable Quotes

> AI made us sloppy because it made us forget how to plan.

*Context: Discussing the negative impact of relying too heavily on AI for coding without planning.*

> One approach ships a feature. The other ships a feature and teaches the system how you think for next time.

*Context: Comparing traditional coding to planning with AI, emphasizing the long-term benefits of the latter.*

> I created an AI agent with one job: Take a Figma design screenshot, analyze how to implement it, and output a detailed plan grounded in our patterns, components, and way of building.

*Context: Explaining the process of using an AI agent to translate design into actionable development plans.*

## Related Topics

- [[topics/prompt-engineering]]
- [[topics/ai-agents]]
- [[topics/agent-native-architecture]]
