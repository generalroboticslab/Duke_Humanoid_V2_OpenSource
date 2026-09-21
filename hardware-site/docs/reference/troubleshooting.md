# Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Interfaces appear as `can0`, `can1`…; setup script finds no buses | No `udev` rule: adapters named in plug order | Add the rules on [Software](../software.md); reload, replug |
| Wrong adapter reset or mapped | Two rules share a `NAME`; the last wins | One line per name |
| Bus will not come up or reset | `usbreset` missing on a minimal Ubuntu | Install `usbutils`; check `which usbreset` |
| `/dev/ttyUSB0` never appears (Ubuntu 22.04) | `brltty` claims USB-serial devices | `sudo apt remove brltty`, replug |
| Torso tilted, perception geometry wrong | Robot hung with bent legs | Re-hang with legs straight |
| Pinned process exits with an affinity error | Core list copied from a CPU with more cores | Re-derive core sets for your CPU |
| Joint misbehaves after driver board re-mount or phase-lead reorder | Stale encoder calibration | Re-calibrate in the vendor tool |
| Actuator faults when its control mode changes | Mode switched while running | Send stop first, then switch |

Inspect a bus (replace `canN`, e.g. `can23`; see [SocketCAN](https://docs.kernel.org/networking/can.html)):

```bash
ip -details -statistic link show canN        # state and error counters
candump any,0:0,#FFFFFFFF -extA              # all frames on all interfaces, error frames decoded
canbusload canN@1000000 -cbr                 # bus load, in a second terminal
```

!!! note "Not recorded — entries from real failures: missing or wrong actuator ID, reversed joint, binding after bearing press, misfit part, no depth, high idle current, short pack life, harness failure at a joint"
    *Owner: hardware lead, continuously.*
