# Pre-power checks

Pass groups A to G in order with **no pack in the machine**; never use a pack to
find a wiring fault.

!!! abstract "At a glance"
    - **You will:** sign and date each group.
    - **Tools:** rated hoist, multimeter, bench supply.

## A. Check mechanics and site

| # | Check | Pass |
| --- | --- | --- |
| A1 | Rated hoist carries full weight | Hoist rated well above 36 kg; safety factor ≥ 5:1 per ASME B30.9 **UNVERIFIED**{ .dh-unverified } ([Safety](../fabrication/index.md#safety)) |
| A2 | Legs | Hang straight, no torso tilt (tilt corrupts perception geometry) |
| A3 | Floor | Clear within the robot's reach and fall path |
| A4 | Final-integration fastener check | Signed |
| A5 | Both checks on [Routing](#verifying-a-routing-job) | Pass; wiggle-test runs with motors **unpowered** (arms still polled on CAN) **UNVERIFIED**{ .dh-unverified } |
| A6 | Two people; whoever holds the operator kill switch does not connect the battery | Confirmed aloud |

## B. Test continuity and isolation

Nothing energised.

| | | |
| --- | --- | --- |
| B1 | Every scheduled power conductor, end to end | Conducts (< 1 Ω for power, < 5 Ω for signal) |
| B2 | Every unscheduled pair | Open (> 1 MΩ) |
| B3 | Motor bus + to − | Rises as drive capacitance charges, settles at the bench supply. **Steady low = short: stop.** > 100 kΩ once charged is the typical pass **UNVERIFIED**{ .dh-unverified } |
| B4 | Each bus rail to chassis | > 1 MΩ **UNVERIFIED**{ .dh-unverified }; < 100 kΩ is a fault |
| B5 | 12 V rail + to − | > 10 kΩ with no load (converter input caps charge) **UNVERIFIED**{ .dh-unverified }; steady < 100 Ω is a short |
| B6 | Each conductor to its sleeve or shield | > 1 MΩ **UNVERIFIED**{ .dh-unverified } |

!!! note "Not measured on the reference robot — exact resistance thresholds for B3–B6"
    *Owner: electrical lead.*

## C. Check polarity

A wrongly loaded XT30 shell mates with reversed polarity.

| | | |
| --- | --- | --- |
| C1 | Every power connector, bench supply on the source side | + at the pin the pinout names |
| C2 | Both pack connectors | Match the robot side |
| C3 | Series pack link, packs disconnected | One pack's + to the other's −; free − to ground blocks, free + to surge protector |
| C4 | CAN (Controller Area Network) pair at every drop | CAN_H to CAN_H throughout |
| C5 | Every soldered XT30, second pass | + at the named pin |
| C6 | Every soldered XT30, tug | Nothing moves |

## D. Bench-test converters

Bench supply, low current limit, before any converter sees a pack. Which are
fitted: **UNVERIFIED**{ .dh-unverified } ([Power system](#feed-the-12-v-rail)).

| | | |
| --- | --- | --- |
| D1 | 20–60 V → 12 V converter, no load | 12.0 V ± 5 % (11.4–12.6 V) **UNVERIFIED**{ .dh-unverified } |
| D2 | 48 V → 12 V converter #1, no load | 12.0 V ± 5 % **UNVERIFIED**{ .dh-unverified } |
| D3 | 48 V → 12 V converter #2, no load | 12.0 V ± 5 % **UNVERIFIED**{ .dh-unverified } |
| D4 | Each converter at expected load | Output stays within ± 5 %, no thermal shutdown over 5 min at rated load **UNVERIFIED**{ .dh-unverified } |
| D5 | Supply current at each step | Stop above the converter's rated input current × 1.1 (e.g. < 11 A on a 10 A converter) **UNVERIFIED**{ .dh-unverified } |

!!! note "Not measured on the reference robot — exact bench supply settings, expected load, and per-converter rated current for D1–D5"
    *Owner: electrical lead.*

## E. Test CAN buses

| | | |
| --- | --- | --- |
| E1 | CAN_H–CAN_L, each bus, unpowered | About 60 Ω (120 Ω: a terminator missing; 40 Ω: one extra) |
| E1a | H and L, adapter to last motor | Both conduct |
| E1b | H–L, and each line to ground | No short |
| E2 | Adapter labels vs `99-candlelight.rules` | Agree |
| E3 | Adapter USB plugs, firm pull | Stay in |
| E4 | Every drop vs the [actuator map](#the-actuator-map) | Exact match |

## F. Check packs

On the bench, before either pack goes into the robot; join them in series only
after F1–F4 pass.

| | | |
| --- | --- | --- |
| F1 | Terminal voltage, each pack | 22.2 V nominal, 25.2 V full; reject below 21.0 V (3.5 V/cell soft floor) on arrival **UNVERIFIED**{ .dh-unverified } |
| F2 | Cell spread, each pack (balance lead) | < 0.05 V across all six cells **UNVERIFIED**{ .dh-unverified } |
| F3 | Condition | No swelling, damaged wrap or lead |
| F4 | Pack-to-pack voltage difference | < 0.10 V **UNVERIFIED**{ .dh-unverified } |

!!! note "Yours to confirm — exact pack acceptance thresholds for F1, F2 and F4"
    *Owner: electrical lead + safety officer.*

## G. Confirm software stops

The reference build's first stop is software, not hardware: see the three
layers on [Safety](../fabrication/index.md#rules). Verify each layer
fires when you trigger it.

| | | |
| --- | --- | --- |
| G1 | Operator-side stream silence | Stop `humanoid_auto_operator.py` (or `humanoid_real_env.py`): the robot's nav 1 s / arm 0.5 s / gaze 2 s failsafes fire and the base stops, arms ramp to default, gimbals park |
| G2 | CAN watchdog | Pause `humanoid_setup_can.py`: the watchdog latches a frozen arm into damped hold until restart |
| G3 | Physical disconnect | Pull the pack connector: every drive releases the bus and the rig drops to gantry support |
| G4 | Who triggers each | Known to all, aloud |

✅ **Check:** all six groups pass and are signed.
