

## Intro

  This is Open Design

  an open source alternative to Claude Design

  that lets you use whatever coding agent or model you already have installed

  to generate full web prototypes mobile apps pitch decks and more

  with 72 brand grade design systems built in

  and every project stays on your machine so nothing touches the cloud

  but its only been out for a month

  the docs are rough and you need to set up a local daemon

  so is it actually worth switching from Claude Design

  hit subscribe and let's find out


## Exp

  Claude Design was released on April 17th and was an instant hit

  but its proprietary cloud only and locked to one model at 20 dollars a month

  which basiucally means it's not for everyone

  so 11 days later Tom Huang and the team at nexu shipped this as an open source alternative

  which was also really popular 

  and it hit 39 thousand stars in under a month

  but how is this tool able to produce good designs just like claude design

  well because of two things working together

  the first is design systems

  full brand specs with typography spacing and colour tokens

 inspired from brands like Linear and Stripe and Spotify

  the second thing is skills, lots of skills

  structured rules for each output type

  so a dashboard skill knows how to lay out charts and a deck skill knows how to structure slides

  theres even an anti ai slop checklist baked into every prompt

  and before it generates anything it asks you about your audience tone and brand context

  if youve seen my video on impeccable this might sound familiar

  but there are some key differences which ill get into later

  one thing to note if you want to use open design with Claude you'll need an API key

  because Anthropic doesnt allow subscriptions to be used with third party tools

  but it works with 15 other agents so you have options

  so let's use it to redesign a youtube channel searcher I've been working on

  using a non claude model like, glm-5.1 to see if it can still produce amazing designs

---

## Demo

so to get started you can download the desktop app for mac or windows

[https://github.com/nexu-io/open-design/releases]

run it with docker, or build from source

which is what I've done, so while it's running

I can view the project on this url

which looks super overwhelming for someone like me who hasn't used claude design before

but we can click 

[it has picked up on my installed agent harnesses]

[go through execution and model, change to codex for reasoning effort, opencode for os models]

[pick glm]

[media providers, so openai for image genration, elevenlabs for text to speech or sound effects]

[skills, external mcps]

[orbit = which pulls data form connectors github linear gmail, gets data and uses ai to publish results into a single html page, once a day]

[you can let a coding agent control open design through an mcp server]

there's also pets whcih are from codex, basically there's a lot goin gon here

but we're going to leave the defaults and prototype something

[give it name]

[riff, design systems and templates]

[choose miro]

[mention prototype tab, deck for html presentations, or use an existing template]

[riff]


  Demo

  - use the yt-channels project as the base
  - pick a design system and skill
  - walk through the discovery form (audience, tone, brand context)
  - generate a prototype from a prompt related to the project
  - show the live preview in the sandboxed iframe
  - show the output quality and how it doesn't look like generic ai
  - export in a couple of formats
  - swap design system and regenerate to show the difference


## Outro

so that is a quick overview of open design

  is it worth using

  well if you already have a coding agent installed its a no brainer to try

  the design system and skills combo means the output actually looks pretty decent

  but how does it compare to impeccable

  personally I like how impeccable does the planning,

  it asks you a series of question sfirst about the design you want

  generates some mockups of the design, you pick the one you like and it goes from there

  so you can have pretty much no idea of the design you want at the start

  and end up with somethnig impressive

  open design and also claude design is more for someone 

  who already has some design knowledge because 

  it get's you to pick a design syustem up front

  but it does have a great ui for making comments and tweaks

  and requires less prompts to design someting

  but to be honest, it did a great job of desinging with glm

  and this is a great tool if I wanted to design something relatively quickly

  for not too much money

  but if you do have the money, claude design is pretty good

  I mean look at what it did with the same prompt
