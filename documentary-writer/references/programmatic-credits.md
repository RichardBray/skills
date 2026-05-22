# Anthropic is charging developers twice for Claude
# Anthropic just killed free programmatic access to Claude
# Claude's "free credits" are actually a price increase
# Your Claude subscription just got a lot worse
# Anthropic doesn't want you using other tools with Claude

[https://x.com/mattpocockuk/status/2040536403289764275]

THUMB: anthropic logo, credit card, $20 crossed out, developer looking confused


## Intro

anthropic just introduced something called programmatic credits

a monthly allowance that separates your claude subscription into two buckets

one for chatting on claude dot ai and one for everything else

so tools like the agent sdk the claude dash p command and third party apps like openclaw

all now pull from a separate credit pool billed at full api rates

which means your 200 dollar max subscription gives you 200 dollars of api credits per month

that at full api rates can disappear in a single afternoon

but the way anthropic announced it makes it sound like a bonus

like theyre giving you something extra on top of your subscription

if you look a bit closer though its something much worse

so hit subscribe and lets dig into what this actually means


## Exp

to understand why this exists you need to go back to when claude code first launched

because from the beginning anthropic let you use the agent sdk and claude dash p with your subscription

which meant developers could build tools on top of claude using their existing plan

and thats exactly what happened

matt pocock built sandcastle a library for running coding agents in sandboxes

theo built t3 code a desktop app for managing multiple coding agents

zed the open source code editor added claude as a built in agent

all of them powered by claude through your subscription

but the problem was developers on a 200 dollar max plan were running workloads that would cost ten to thirty times more at api rates

[https://levelup.gitconnected.com/why-i-stopped-paying-api-bills-and-saved-36x-on-claude-the-math-will-shock-you-46454323346c]

and anthropic was absorbing the difference

so on january 9th they quietly blocked subscription tokens from working outside official apps

no announcement no warning just a silent update that broke workflows overnight

[https://openclaw.rocks/blog/anthropic-oauth-ban]

some developers even had their accounts banned for triggering abuse filters

anthropic reversed those bans but the restriction itself stayed

then in february they updated their terms of service to formally ban third party harness usage

[https://www.theregister.com/software/2026/02/20/anthropic-clarifies-ban-on-third-party-tool-access-to-claude/5014546]

but to make things worse in april they enforced it for real blocking openclaw and everything like it

they even started scanning git status in claude codes system prompt for keywords like hermes and openclaw

so if your commit history happened to mention one of those tools you could get flagged

even if you werent actually using them

there are three theories about why anthropic did this

the first is compute efficiency

anthropic said third party tools dont use their prompt caching properly

which means every request costs them more to serve than the same request through claude code

but on may 6th anthropic signed a deal with spacex for over 220 thousand gpus

[https://www.cnbc.com/2026/05/06/anthropic-spacex-data-center-capacity.html]

so if compute was the problem they just solved it

the second is telemetry

they claimed third party tools generate unusual traffic patterns without any of the telemetry claude code provides

[https://x.com/trq212/status/2009689809875591565]

which makes it hard for them to debug rate limits or account bans

but they could just require third party tools to send that telemetry through the sdk

instead of blocking them entirely

and the third is competitive positioning

why let someone else build a free version of claude code on top of your own subscription

and this one is harder to debunk

because every restriction theyve made pushes developers toward claude code and away from everything else

and at this point developers didnt even know what they were allowed to use anymore

so now anthropic has landed on this credit system

which sounds like a great deal until you do the maths


---


## Exp 2

every paid subscriber gets a monthly credit equal to their subscription price

20 dollars on pro 100 on max 5x and 200 on max 20x

and these credits are only for programmatic usage

so the agent sdk claude dash p github actions and any third party app built on the sdk

but heres the catch these credits get billed at full api rates

to put that into perspective on the pro plan you get around 45 messages every 5 hours all month long

but 20 dollars of api credit using opus could be gone in two days

and on max you were getting unlimited programmatic usage through your subscription

now that same 200 dollars of credit might last a week if youre lucky

and once your credit runs out you either stop or enable extra usage which charges you at full api rates on top of your subscription

to make things worse unused credits dont roll over they just expire at the end of the month

and all of this kicks in on june 15th and you have to opt in through your account settings to activate it


## Outro

on one hand this is good because theres finally clarity

developers now know they can use tools like openclaw hermes and conductor without getting banned

but on the other hand it costs a lot more than it used to

and its clear anthropic would prefer you stay inside their ecosystem

theyve built claude code claude cowork managed agents and routines

all designed to make you feel like you dont need anything else

which is basically vendor lock in

and its actually working ive moved from opencode to claude code because i didnt want to get banned

ive stopped using nano claw and now use claude routines

i do miss the customisability i had but its so much cheaper to use the subscription that ive kind of had to do it

but it feels strange to be paying more for something that used to be included

especially when you compare it to what openai is doing

codex is included in every chatgpt subscription with no separate credit system

they opened their platform to openclaw and its 3 million users

and theyre offering enterprise customers two free months of codex to switch from claude

[https://pub.aimind.so/you-can-get-two-months-of-codex-enterprise-for-free-right-now-and-openai-didnt-pick-this-week-at-9416e022fa26]

so while anthropic is putting up walls openai is tearing them down

and the question now is whether claude is still good enough to justify paying more for less

for me right now it is but that gap is closing fast

[https://x.com/mattpocockuk/status/2054637261388447956]



---

[https://clawd.rip/]

[https://www.reddit.com/r/ClaudeCode/comments/1tc832e/anthropic_just_ripped_off_everyone_and_they_still/]
