# Printing guide

| Process | Parts | Material |
| --- | --- | --- |
| FDM | 40 covers, mounts, plates and pads | PLA; TPU for the pads and covers |
| SLS | The drivetrain parts below — each transmits actuator torque or carries a bearing | Nylon 12 |

| SLS part | Qty |
| --- | ---: |
| `3DP_arm05_RS02_shaft_bearing_retainer` | 4 |
| `3DP_arm06_RS02_shaft_coupler` | 2 |
| `3DP_arm11_wrist_roll` | 2 |
| `3DP_arm14_wrist_block` | 2 |
| `3DP_arm15_end_effector_attachment` | 2 |
| `3DP_grip05_pinion` | 2 |

Process and material per part: [Printed parts](../bom/index.md#printed-parts). Files: the STL in each row.

1. Print one fit-critical part first — one that mates with a machined part or takes a heat-set insert — and check the fit.
2. Print the set.
3. Ream holes to size (FDM prints undersize); melt heat-set inserts in with a soldering iron.

<figure markdown>
  ![Soldering iron setting a heat-set insert in a printed battery holder](../assets/photos/body-heat-set-inserts.webp){ loading=lazy width="400" }
  <figcaption>Heat-set insert going into a printed battery holder.</figcaption>
</figure>

✅ **Check:** the test part fits before the set is printed.
