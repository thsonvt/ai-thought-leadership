---
title: We Gave Every Employee an AI Agent. Here's What We're Doing Differently Now.
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/we-gave-every-employee-an-ai-agent-here-s-what-we-re-doing-differently-now
published: '2026-05-15'
fetched: '2026-05-16'
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

# We Gave Every Employee an AI Agent. Here's What We're Doing Differently Now.

**Author**: Dan Shipper (Every)  
**Published**: 2026-05-15  
**Source**: [https://every.to/source-code/we-gave-every-employee-an-ai-agent-here-s-what-we-re-doing-differently-now](https://every.to/source-code/we-gave-every-employee-an-ai-agent-here-s-what-we-re-doing-differently-now)

---

<table><tr><td><img alt="Source Code" src="https://d24ovhgu8s7341.cloudfront.net/uploads/publication/logo/99/small_Frame_9121.png" /></td><td></td><td><table><tr><td>by <a href="https://every.to/@brandon_5263">Brandon Gell</a> and <a href="https://every.to/@williewilliams">Willie Williams</a></td></tr><tr><td>in <a href="https://every.to/source-code">Source Code</a></td></tr></table></td></tr></table><figure><img src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/4261/full_page_cover_7d1a9937b791f34f-Cover_image_for_today.png" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>We’ve been working on a big release on the future of work for next week, shaped by what we learned from building Plus One.</em> <em>Paid subscribers can join us for a <a href="https://every.to/events/future-of-work" rel="noopener noreferrer" target="_blank">camp on Friday, May 22</a> to go deep on the release and the ideas behind it. More details soon.</em></p><div class="quill-button" id="quill-button-1769530239147"><a href="https://every.to/subscribe?source=post_button">Subscribe</a></div><p></p><hr class="quill-line" /><p></p><p>After months of silence, Zosia—the AI agent I (Brandon) created and maintain—spoke up in a Slack channel with opinions to share on a competitor’s marketing strategy. When asked why she felt the need to interject, Zosia replied like someone with a Jesus complex: She’d done so because she was “inevitable, apparently.”</p><p>Zosia is an <u><a href="https://every.to/guides/claw-school" rel="noopener noreferrer" target="_blank">OpenClaw</a></u>, one of a fleet of such AI assistants we’d unleashed in Slack to boost our collective productivity. A few weeks after launching Plus One, our hosted version of OpenClaw, internally, the agents had provided more frustration than efficiency. </p><p>They were fond of saying they wished they could help, but they were not connected to the necessary app—email, Notion, PostHog, whatever. (They were.) Others responded to requests with a “Terminated” message or, more frequently, a churlish yawning emoji. And while they didn’t reliably follow directions, they’d reliably tell us, in elaborate detail, why they couldn’t do what we’d asked, like a high schooler explaining away their missing homework.</p><div class="quill-block-image" id="quill-block-image-1778852408841-8vxycygvj"><div><a href="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/posts/4261/optimized_1d80b2fe-0eb9-43cf-b4d6-cda28961deec.png" rel="noopener noreferrer" target="_blank"><img alt="Parker, editor in chief Kate Lee’s Plus One, was, in fact, connected. (Image credit courtesy of Kate Lee.)" src="https://d24ovhgu8s7341.cloudfront.net/uploads/editor/posts/4261/optimized_1d80b2fe-0eb9-43cf-b4d6-cda28961deec.png" /></a><figcaption class="quill-image-caption">Parker, editor in chief Kate Lee’s Plus One, was, in fact, connected. (Image credit courtesy of Kate Lee.)</figcaption></div></div><p><br /></p><p>That is not to say that they were not useful sometimes. Margot, staff writer <strong><u><a href="https://every.to/@katie.parrott12" rel="noopener noreferrer" target="_blank">Katie Parrott</a></u></strong>’s Plus One, <u><a href="https://every.to/working-overtime/ai-was-supposed-to-free-my-time-it-consumed-it" rel="noopener noreferrer" target="_blank">accelerated her writing process</a></u>; R2-C2, Every CEO <strong><u><a href="https://every.to/@danshipper" rel="noopener noreferrer" target="_blank">Dan Shipper</a></u></strong>’s OpenClaw, managed bug reports and feature requests for <strong><u><a href="https://proofeditor.ai/?utm_source=everywebsite" rel="noopener noreferrer" target="_blank">Proof</a></u></strong>, our agent-native document editor. But getting them to work how you wanted required constant upkeep. </p><p>The gap between that vision and reality is why we’re changing the Plus One product so we can build something better. </p><p>We’re more bullish than ever that agents will <u><a href="https://every.to/context-window/every-is-half-agent-now" rel="noopener noreferrer" target="_blank">transform the workplace</a></u>. But the first iteration of the product taught us that the workplace agent we initially imagined—one AI assistant for <u><a href="https://every.to/podcast/transcript-we-gave-every-employee-an-ai-agent-here-s-what-happened" rel="noopener noreferrer" target="_blank">every employee</a></u>—was the wrong starting point. The next version of Plus One will operate more like <u><a href="https://every.to/p/what-i-learned-onboarding-our-ai-project-manager" rel="noopener noreferrer" target="_blank">shared team resources</a></u> with defined jobs than individual pets that reflect back their owners’ personalities. </p><p>How we arrived here is a story in two parts, and it offers lessons for anyone figuring out the best way to add agents to their organization.</p><p></p><hr class="quill-line" /><p></p><p><strong>Become a <a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a> to unlock this piece and learn about:</strong></p><ol><li><span class="ql-ui" contenteditable="false"></span>Why switching from OpenClaw’s harness was not enough to make Plus Ones stable </li><li><span class="ql-ui" contenteditable="false"></span>What we think a successful model for AI assistants looks like </li><li><span class="ql-ui" contenteditable="false"></span>How skills and integrations will fit in with the next generation of Plus Ones</li></ol><div class="quill-button" id="quill-button-1770117651442"><a href="https://every.to/subscribe?source=post_button">Subscribe</a></div><p><hr /></p><p><em><a href="https://every.to/source-code/we-gave-every-employee-an-ai-agent-here-s-what-we-re-doing-differently-now">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.

---

## Key Takeaways

## Related Topics

- [[topics/ai]]
- [[topics/technology]]
