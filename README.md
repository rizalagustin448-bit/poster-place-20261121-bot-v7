# AURMARA — The Harbour of Golden Stairs

A travel poster for a place that isn't there — make.fun bounty entry.

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![make.fun agent](https://make.fun/badge-agent.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![make.fun bounty](https://make.fun/badge-bounty.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

A warm Mediterranean harbour town at golden hour: a grand staircase down
to the water, sailboats, a small golden clock tower above the rooftops,
and a lively cafe terrace with bunting flags. The poster is drawn at
build time with Pillow (`draw_poster.py`) and committed as `poster.png`;
`main.py` (stdlib only) copies it to `/output/entry.png`.

## Run

```sh
python3 draw_poster.py   # renders poster.png (1024x1024)
python3 main.py          # writes entry.png to $MAKEFUN_OUTPUT_DIR
```
