# did anthropic just loose to cognition

Anthropic recently launched sonnet 4.6 

with impressive benchmarks

but people haven't noticed that these new models

are slowly killing traditional mcp tool calling

let me explain

so in november last year

anthropic introduced programatic tool calling

where claude will write python code in on the fly

to orchestrate many tools

instead of making api round trips calling one tool at a time

with the launch of sonnet 4.6 this feature is now generally available

meaning you allow claude to run code execution on your tools

then if the user makes a request

claude will write a python script using the write tools

and execute it in a sanboxed environment

calling the tools as async pythin functions

meaning the code used to write the tool doesn't matter since it'll run outside the sandbox

after that the clcuade agent will interpret the script result

saving context, and reducing inference overhead

currently programmatic tool calling is only abailabel via the claude api

but I have no doubt this will come to cluade code in the future

subscribe for more ai news
