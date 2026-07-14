---
title: How I Polish Software That Agents Built
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/how-i-polish-software-that-agents-built
published: '2026-07-13'
fetched: '2026-07-14'
topics:
- AI
- Technology
key_quotes: []
stance: {}
evolution_note: Initial analysis pending
tags:
- ai
- tech
---

# How I Polish Software That Agents Built

**Author**: Dan Shipper (Every)  
**Published**: 2026-07-13  
**Source**: [https://every.to/source-code/how-i-polish-software-that-agents-built](https://every.to/source-code/how-i-polish-software-that-agents-built)

---

<p><em>in Source Code</em></p><figure><img alt="" src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/4338/b3ec8a8216690472-Cover_image_monday_3.jpg" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>Was this newsletter forwarded to you? <u><a href="https://every.to/account" rel="noopener noreferrer" target="_blank">Sign up</a></u> to get it in your inbox.</em></p><p></p><hr class="quill-line" /><p></p><p>For most of the history of making software, writing code <em>was</em> the work. You spent your days typing out functions, fighting errors, debugging migrations, and reading through other people’s code to figure out why a function did what it did. Another day in the code factory. </p><p>That’s mostly over. With a good brainstorm and a <u><a href="https://every.to/source-code/stop-coding-and-start-planning" rel="noopener noreferrer" target="_blank">well-structured plan</a></u>, today’s models will write code, run tests, fix failures, and hand you back a clean pull request with code changes ready for review. I’ll open my laptop in the morning to a stack of green pull requests that agents shipped overnight, with features ready to merge before my first meeting. The factory has been automated. </p><p>What I’m left to do is sit with the result and decide whether it’s any good—and then push it further than the agent could take it itself. A model doesn’t know what <em>I</em> would call good, sitting in front of <em>this</em> feature in <em>this</em> product I’m building for <em>these</em> users. Without that final human judgment, everything the agent produces is functional, but forgettable. A few weeks ago I clicked on an email card in <strong><u><a href="https://cora.computer" rel="noopener noreferrer" target="_blank">Cora</a></u></strong> and knew instantly the animation was wrong—it slid in from the top of the screen instead of opening from where I’d clicked mid-screen. I told the agent, it fixed it, and I clicked again—better. </p><p>Polish is the final step in <u><a href="https://every.to/guides/compound-engineering" rel="noopener noreferrer" target="_blank">compound engineering</a></u>—the discipline I’ve been developing over the past year for building software in a way that gets smarter with every iteration. As more of the <u><a href="https://www.youtube.com/watch?v=G0LTv8hQ5Cs" rel="noopener noreferrer" target="_blank">middle parts of the process</a></u> gets automated, polish matters more now, because it’s the part of the work that’s still yours. Instead of the assembly line worker putting the code together, you’re the person at the end of the line who decides whether it’s good enough to put your name on. <strong> </strong></p><h2><strong>Polish in practice</strong></h2><p>The card animation that looked wrong is a good example of how polish works, because animation is something that agents still struggle with (although it will improve over time). </p><p>The pull request had passed every automated check. The review agents had nothing left to flag for me. I ran /ce-polish—part of the <u><a href="https://github.com/EveryInc/compound-engineering-plugin" rel="noopener noreferrer" target="_blank">compound engineering plugin</a></u>—which does three things and then gets out of my way. It checks out the branch I want to polish, starts the development server in the background, and opens the running app inside my editor, right next to the agent. From there, I clicked on an email card to open it and started my assessment. </p><div class="quill-block-image" id="quill-block-image-1783959555088"><div><a href="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/post/4338/optimized_795c99b1-a426-4311-8646-d1c71744dc22.jpg" rel="noopener noreferrer" target="_blank"><img alt="The updated version of the Cora Brief in development, which I refined using the polish step. (Image courtesy of Kieran Klaassen.)" src="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/post/4338/optimized_795c99b1-a426-4311-8646-d1c71744dc22.jpg" /></a><figcaption class="quill-image-caption">The updated version of the Cora Brief in development, which I refined using the polish step. (Image courtesy of Kieran Klaassen.)</figcaption></div></div><p><br /></p><p>Once the new design was open beside the agent, I could see that it still felt too loose. There was too much whitespace, and the cards needed to be more compact. I said so out loud via <strong><u><a href="https://monologue.to" rel="noopener noreferrer" target="_blank">Monologue</a></u></strong>. The agent tightened the layout; the app hot-reloaded; I looked again—better. A plan could tell the agent to make the Brief feel like a magazine. It couldn’t tell the agent when the page had the right density. I had to see it and decide for myself.</p><p>This is what polish looks like:...</p><p></p><hr class="quill-line" /><strong>Become a <a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a> to unlock this piece and learn about:</strong><p></p><ul><li>Why polish changed Kieran’s planning and reviewing, not just the end of the loop</li><li>When a muttered complaint becomes a rule the agent follows on every future feature</li><li>How the job of a great engineer has shifted from building to deciding what’s good enough</li></ul><div class="quill-button" id="quill-button-1770117651442"><a href="https://every.to/subscribe?source=post_button">Subscribe</a></div><p><em><a href="https://every.to/source-code/how-i-polish-software-that-agents-built">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.</p>

---

## Key Takeaways

## Related Topics

- [[topics/ai]]
- [[topics/technology]]
