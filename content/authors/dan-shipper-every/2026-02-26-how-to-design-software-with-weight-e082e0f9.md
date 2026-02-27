---
title: How to Design Software With Weight
author: Dan Shipper (Every)
author_id: dan-shipper-every
url: https://every.to/source-code/how-to-design-software-with-weight
published: '2026-02-26'
fetched: '2026-02-27'
topics:
- Product Development
- User Experience
- Design Principles
- Software Design
key_quotes:
- text: I studied vintage radios.
  context: Daniel Rodrigues shares an unconventional source of inspiration for designing
    the Monologue iOS app.
- text: I found myself crouched beside a light switch in my apartment, pressing it
    on and off, watching how the shadow moved.
  context: Daniel Rodrigues describes his hands-on approach to understanding how physical
    interactions can inform digital design.
- text: The app is deliberately sparse—few buttons and a restrained color palette—but
    each element is designed to feel like something you could reach out and touch.
  context: The philosophy behind Monologue's design, focusing on minimalism and tactile
    feedback.
stance:
  Figma: positive
evolution_note: This article represents a deep dive into the practical application
  of design principles in software development, showcasing a blend of expertise and
  innovative thinking.
tags:
- design-thinking
- ux/ui-design
- product-innovation
- interaction-design
- minimalism
---

# How to Design Software With Weight

**Author**: Dan Shipper (Every)  
**Published**: 2026-02-26  
**Source**: [https://every.to/source-code/how-to-design-software-with-weight](https://every.to/source-code/how-to-design-software-with-weight)

---

<table><tr><td><img alt="Source Code" src="https://d24ovhgu8s7341.cloudfront.net/uploads/publication/logo/99/small_Frame_9121.png" /></td><td></td><td><table><tr><td>by <a href="https://every.to/@lucasfischer">Lucas Fischer</a> and <a href="https://every.to/@daniel_5fbd21_1">Daniel Rodrigues</a></td></tr><tr><td>in <a href="https://every.to/source-code">Source Code</a></td></tr></table></td></tr></table><figure><img src="https://d24ovhgu8s7341.cloudfront.net/uploads/post/cover/3951/full_page_cover_swithc_cover.png" /><figcaption>Midjourney/Every illustration.</figcaption></figure><p><em>TL;DR:</em><strong><em> </em></strong><em>Design has always been core to what we do at Every—it’s a big part of what makes our products feel like ours. </em><strong><em>Daniel Rodrigues</em></strong><em> is Every’s senior designer, and </em><strong><em>Lucas Fischer</em></strong><em> is the design engineer who helped bring our smart dictation app </em><strong><em><u><a href="https://monologue.to" rel="noopener noreferrer" target="_blank">Monologue</a></u></em></strong><em> to iOS. This is their first time writing for us, and they’re pulling back the curtain on the design process: studying vintage radios, crouching beside light switches to understand how shadows move, and exploring 20 wrong keyboard concepts to find one right one. If you’ve ever wondered what it takes to make software feel like something you could reach out and touch, this is your read.—<u><a href="https://every.to/@kate_1767" rel="noopener noreferrer" target="_blank">Kate Lee</a></u></em></p><p></p><hr class="quill-line" /><p></p><p>While designing the <u><a href="https://apps.apple.com/us/app/monologue-smart-dictation/id6755956193" rel="noopener noreferrer" target="_blank">iOS app</a></u> for Every’s smart dictation app <strong><u><a href="https://www.monologue.to/" rel="noopener noreferrer" target="_blank">Monologue</a></u></strong>, I <strong>(<u><a href="https://x.com/darustudio" rel="noopener noreferrer" target="_blank">Daniel Rodrigues</a></u></strong>, Every’s senior designer<strong>) </strong>did a lot of things I didn’t expect. I studied vintage radios. Design engineer <strong><u><a href="https://lucas.love/" rel="noopener noreferrer" target="_blank">Lucas Fischer</a></u></strong> and I worked with a musician to craft the sound a button makes when you tap it. And at one point in January, I found myself crouched beside a light switch in my apartment, pressing it on and off, watching how the shadow moved. I needed to understand how a real button catches light to make a fake one feel real. </p><p>Until recently, <u><a href="https://www.monologue.to/" rel="noopener noreferrer" target="_blank">Monologue</a></u> only lived on Mac desktops. A week ago, <u><a href="https://every.to/on-every/introducing-monologue-for-ios" rel="noopener noreferrer" target="_blank">we brought it</a></u> where most people do their typing: their phones. The app is deliberately sparse—few buttons and a restrained color palette—but each element is designed to feel like something you could reach out and touch, like the light switch on the wall. </p><p>What follows is an inside look at the design principles and engineering decisions that we used to make a few buttons on a screen feel like something more.</p><h3>Decide where quality matters most</h3><p>I designed <u><a href="https://every.to/on-every/introducing-monologue-effortless-voice-dictation" rel="noopener noreferrer" target="_blank">Monologue’s desktop app for Mac</a></u> with its general manager, <strong><u><a href="https://every.to/@naveen_6804" rel="noopener noreferrer" target="_blank">Naveen Naidu</a></u></strong>, in September 2025, so I had an established design language to work from: a love letter to how using tech devices used to feel, with a black-and-white palette and a nostalgic 1990s vibe that resonates with millennials and Generation Z’s pining for the good old days of tech. </p><p>The main difference in designing Monologue for iOS was creating an experience that looked—and felt—good on a much smaller screen. This constraint made the work easier because it pushed us to keep the interface minimal and clean while still infusing it with character.</p><p>Before I opened Figma, the key design tool I use, the most important decision was figuring out where to focus my energy. Three things stood out: the onboarding flow, the keyboard, and a recorder for long-form notes... </p><p></p><hr class="quill-line" /><p></p><p><strong>Become a <a href="https://every.to/subscribe" rel="noopener noreferrer" target="_blank">paid subscriber to Every</a> to unlock this piece and learn about:</strong></p><ol><li><span class="ql-ui" contenteditable="false"></span>Why Daniel built 20 versions of a keyboard he knew were wrong</li><li><span class="ql-ui" contenteditable="false"></span>The Braun radio and Swedish synthesizer behind Monologue’s most-tapped button</li><li><span class="ql-ui" contenteditable="false"></span>The engineering workaround that let the team test dozens of UI states </li></ol><div class="quill-button" id="quill-button-1770117651442"><a href="https://every.to/subscribe?source=post_button">Subscribe</a></div><p><hr /></p><p><em><a href="https://every.to/source-code/how-to-design-software-with-weight">Click here</a> to read the full post</em></p><p>Want the full text of all articles in RSS? <a href="https://every.to/subscribe">Become a subscriber</a>, or <a href="https://every.to">learn more</a>.

---

## Key Takeaways

### Notable Quotes

> I studied vintage radios.

*Context: Daniel Rodrigues shares an unconventional source of inspiration for designing the Monologue iOS app.*

> I found myself crouched beside a light switch in my apartment, pressing it on and off, watching how the shadow moved.

*Context: Daniel Rodrigues describes his hands-on approach to understanding how physical interactions can inform digital design.*

> The app is deliberately sparse—few buttons and a restrained color palette—but each element is designed to feel like something you could reach out and touch.

*Context: The philosophy behind Monologue's design, focusing on minimalism and tactile feedback.*

## Related Topics

- [[topics/product-development]]
- [[topics/user-experience]]
- [[topics/design-principles]]
- [[topics/software-design]]
