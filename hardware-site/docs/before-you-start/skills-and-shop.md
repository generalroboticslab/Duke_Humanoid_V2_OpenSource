# Skills and shop access

!!! missing "MISSING — Prerequisite skills confirmed by an actual build"
    *Owner: whoever performs the first external build.*

## Fabrication

| You need | For |
| --- | --- |
| CNC milling, or a vendor | {{ bom_count("cnc-parts.csv") }} machined part rows |
| FDM (fused deposition modelling) printing | PLA and TPU parts |
| SLS (selective laser sintering) printing, or a service bureau | Nylon parts |
| Bearing and press fits | Bearings sit directly in machined housings |
| Digital caliper (0.01 mm); ideally a bore gauge and surface plate | [Incoming inspection](../fabrication/incoming-inspection.md) |

!!! missing "MISSING — Whether 3 axes suffice (any 4/5-axis or turned part), minimum work envelope, FDM substitute for SLS parts, required finishes"
    *Owner: hardware lead, from the CAD. Blocks [CNC guide](../fabrication/cnc-guide.md).*

## Electrical and assembly

| Skill | Detail |
| --- | --- |
| Soldering XT30 | Solder the cups at about 480 °C; tin until solder wets the gold plating |
| Crimping signal connectors | Motor, encoder and sensor harnesses |
| Soldering CAN (Controller Area Network) twisted pair | Inline, no stubs, twist within 10–15 mm of the joint; about 60 Ω across a terminated bus |
| Multi-drop CAN with termination | Six buses at 1 Mbit/s |
| Heat-set inserts | Soldering iron, into printed parts |

## Software

- Linux administration: kernel modules, `udev` rules, CPU pinning
- An ordered multi-process terminal bring-up
- Basic Python

Planned grasps need a separate CUDA machine; see [Software](../software.md).

!!! missing "MISSING — GPU machine specification and cost (GPU/VRAM, CPU, RAM, OS, CUDA version, the machine used)"
    *Owner: controls lead.*

## People and space

Two people, a bench, a gantry, a charging station away from flammables, and
clear floor. See [Safety](safety.md).

!!! missing "MISSING — Bench and floor space used by the reference build"
    *Owner: hardware lead.*
