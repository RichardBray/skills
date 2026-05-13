# Vercel's electron killer

## Intro

This is zero native

a zig based native app builder by vercel

that can either use the system's webview

or bundle the whole of chromium like just electron

for desktop or mobile apps

providing super tiny binaries

with instant rebuilds for development

but will the fact that you have to write zig code

for some customisations put off js devs

hit subscribe and let's find out


## Exp

Although the bun team are thinking of moving away from Zig

it's still a great language

with no borrow checker or liefetines

can call c directly meaning any c library

is a single import away without any glue code

and it's readable enough for JS devs to pickup

in fact, if you want to watch me learn zig let me know in the comments

i think that could be fun

but essentially zero native is a think zig shell hosting a webview that renders frontend

and uses a json bridge so javascript in the webview can talk to the zig native layer

which is how JS is able to reach os level api's or c libraries

if you think this sounds like electrobun

it kind of does, but there is one huge different

which we'll talk about later on in the video

for now let's go through a quick demo


## Demo

- install zig with mise or brew
- install zero native with bun
- scaffold a project with zero-native init
- go through key files (build.zig, js-bridge, app.zon, frontend)
- run frontend in browser then run native app
- show dev server with hot reload
- show package build and final app size


## Outro

So that is a very quick overview of zero native

there are so many things I didn't go through like system tray icons

code signing, and embedded apps for ios and android

but as great as all thjis is how does it compare to electrobun

which also creates small fast apps that use the system's webview

well with electrobun, bun itself is the execution environment

because you write typescript for the main process

so although a zig binary starts your app the code runs inside a bun webworker

to communicate with the native apis

but with zero-native there is no js runtime

the zig binary is all you need

making have the thinnest possible native shell

with a lower memory footprint

but you may have to write a bit of zig to get by
