# OpenAI's secret open source orchestrator


## Intro

This is openai's symphony

an open source tool for orchestrating long running coding agents

using an exisintg issue tracker like linear

to help agent autonomously complete tasks without human supervision

but why does an agent have to build it from scratch

before you can use it

and does it only work with codex

is this the beginning of more open source tools

from openai

hit subscribe and let's find out


## Exp

Symphony exists because openai hit a human attention bottleneck

engineers could only supervice 3-5 codex sessions concurretly

before context switching began killing productivity

which of course wasn't going to scale

so guess how openai fixed the fast agents with slow human managers problem

they got rid of the humans by building symphony, well kind of

because with symphony, humans just put tasks on a board

each agent will claim the task automatically

and only involve a human when there is something to review

symphony claims to be agent agnostic but as you can guess

it works best with codex, let's go through it


## Demo

- show symphony running and polling for tasks in linear
- create a linear issue
- symphony picks it up and spawns a codex agent
- creates a new workspace for it
- once done it changes the linear issue status and adds a comment
- show the final output


## Outro

if you're already comfortable with or work at a company that uses linear

this is a great

I personally don't use codex

but imagine if you had a team and this is the only way they interacted

with ai for working on a project

a central coding agent for all their skills, plugins and mcp tool

everyone can see what prompts other team members have used and their status

and you won't have toi pay for individual subscriptions

although it's quite difficult to come up with a completely isolated task

that doesn't affect someone elses part of the code depending on the team size

which I'm sure companies out there are looking into

but as cool as this is, in my opinion, multica does do a better job
