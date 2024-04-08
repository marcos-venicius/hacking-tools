# GFinder

File files from a domain of a specifc type and/or download them

```
usage: gfinder [-h] [-a USER_AGENT] url [dorks ...]

Find files from a website over the internet and/or download them

positional arguments:
  url                   URL to search from (example.com, .com.br, *, ...)
  dorks                 inurl:"text", intext:"text", intitle:"title", "specifc term", ext:pdf

options:
  -h, --help            show this help message and exit
  -a USER_AGENT, --user-agent USER_AGENT
                        Custom user agent

./gfinder.py example.com ext:pdf - ./gfinder.py example.com "index of"
```
