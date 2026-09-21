# Pre-power checks

Pass groups A to G in order with **no pack in the machine**; never use a pack to
find a wiring fault.

!!! abstract "At a glance"
    - **You will:** sign and date each group.
    - **Tools:** rated hoist, multimeter, bench supply.

## A. Check mechanics and site

| # | Check | Pass |
| --- | --- | --- |
| A1 | Rated hoist carries full weight | Hoist rated well above 36 kg; safety factor **TODO**{ .dh-missing } ([Safety](../before-you-start/safety.md)) |
| A2 | Legs | Hang straight, no torso tilt (tilt corrupts perception geometry) |
| A3 | Floor | Clear within the robot's reach and fall path |
| A4 | Final-integration fastener check | Signed |
| A5 | Both checks on [Routing](routing.md#verifying-a-routing-job) | Pass; wiggle-test power state **UNVERIFIED**{ .dh-unverified } |
| A6 | Two people; the e-stop (emergency stop) holder does not connect the battery | Confirmed aloud |

## B. Test continuity and isolation

Nothing energised.

| | | |
| --- | --- | --- |
| B1 | Every scheduled power conductor, end to end | Conducts |
| B2 | Every unscheduled pair | Open |
| B3 | Motor bus + to − | Rises as drive capacitance charges, settles high. **Steady low = short: stop.** Settled value **TODO**{ .dh-missing } |
| B4 | Each bus rail to chassis | **TODO**{ .dh-missing } |
| B5 | 12 V rail + to − | **TODO**{ .dh-missing } |
| B6 | Each conductor to its sleeve or shield | **TODO**{ .dh-missing } |

!!! note "Not measured on the reference robot — resistance thresholds for B3–B6"
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
fitted: **UNVERIFIED**{ .dh-unverified } ([Power system](power-system.md#feed-the-12-v-rail)).

| | | |
| --- | --- | --- |
| D1 | 20–60 V → 12 V converter, no load | 12 V ± **TODO**{ .dh-missing } |
| D2 | 48 V → 12 V converter #1, no load | 12 V ± **TODO**{ .dh-missing } |
| D3 | 48 V → 12 V converter #2, no load | 12 V ± **TODO**{ .dh-missing } |
| D4 | Each converter at expected load | **TODO**{ .dh-missing } |
| D5 | Supply current at each step | Stop above **TODO**{ .dh-missing } |

!!! note "Not measured on the reference robot — bench supply settings, output tolerance and expected load for D1–D5"
    *Owner: electrical lead.*

## E. Test CAN buses

| | | |
| --- | --- | --- |
| E1 | CAN_H–CAN_L, each bus, unpowered | About 60 Ω (120 Ω: a terminator missing; 40 Ω: one extra) |
| E1a | H and L, adapter to last motor | Both conduct |
| E1b | H–L, and each line to ground | No short |
| E2 | Adapter labels vs `99-candlelight.rules` | Agree |
| E3 | Adapter USB plugs, firm pull | Stay in |
| E4 | Every drop vs the [actuator map](can-bus.md#the-actuator-map) | Exact match |

## F. Check packs

On the bench, before either pack goes into the robot; join them in series only
after F1–F4 pass.

| | | |
| --- | --- | --- |
| F1 | Terminal voltage, each pack | 22.2 V nominal, 25.2 V full; minimum **TODO**{ .dh-missing } |
| F2 | Cell spread, each pack (balance lead) | **TODO**{ .dh-missing } |
| F3 | Condition | No swelling, damaged wrap or lead |
| F4 | Pack-to-pack voltage difference | **TODO**{ .dh-missing } |

!!! note "Yours to determine — pack acceptance thresholds for F1, F2 and F4"
    *Owner: electrical lead + safety officer.*

## G. Check safety systems

Cutting power drops the robot: the e-stop is a last resort, not a routine stop.

| | | |
| --- | --- | --- |
| G1 | E-stop position | Reachable from outside the robot's reach |
| G2 | E-stop contacts | Open pressed, closed reset |
| G3 | What the e-stop interrupts | **TODO**{ .dh-missing } ([Power system](power-system.md#protection-disconnect-and-e-stop)) |
| G4 | Who holds the e-stop | Known to all, aloud |

✅ **Check:** all seven groups pass and are signed.
