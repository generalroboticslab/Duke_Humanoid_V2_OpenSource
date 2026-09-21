# Citation and licence

## Citation

```bibtex
@misc{duke_humanoid_v2,
  title  = {Visible-Reachable Workspace for Perception-Aware Humanoid Design},
  author = {Boxi Xia and Zijiang Yang and Ryan Shin and Bokuan Li and Eric Lu
            and Jacob Lee and Jiaxun Liu and Boyuan Chen},
  year   = {2026},
  url    = {https://github.com/generalroboticslab/duke_humanoid_v2}
}
```

**Cite the repository record above.** The umbrella repository's `CITATION.cff`
is the canonical machine-readable form: same authors and URL, Apache-2.0,
released 2026-08-26, under the title "Duke Humanoid V2: a 31-DoF bipedal
platform with two independently actuated camera gimbals, designed around the
visible-reachable workspace". The BibTeX above is the short form for the paper.

!!! note "Yours to determine — paper citation (preprint not posted) and which record covers the hardware"
    *Owner: PI.*

## Licence

All artefacts published from this release are under the
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0):

| Artefact | Licence |
| --- | --- |
| Code (umbrella, simulation, deploy) | Apache-2.0 |
| Hardware design files (CAD, drawings, BOM) | Apache-2.0 |
| This documentation and its figures | Apache-2.0 |

> Apache-2.0 grants no rights in a mechanical design: a downstream builder who
> makes a physical robot inherits no patent grant from this licence.

The umbrella repository's `LICENSE` file is the canonical copy. The CAD
release ships its own `LICENSE` so a builder who only downloads the design
files still has the terms in hand. V1 was MIT; this release is Apache-2.0.

## Third-party material

- The workspace-study comparison models keep their own licences; the **Fourier
  GR-3 model is GPL-3.0** (the README says how to remove it).
- The two Unitree G1 URDFs in `simulation/asset/unitree_g1/` are cuRobo exports
  and ship without a `LICENSE` file. They belong to the code repository, not to
  this hardware release: no G1 file is redistributed here, and nothing on this
  site needs one to build the robot. Their mesh paths point into
  [mjlab](https://github.com/mujocolab/mjlab), which carries the MuJoCo
  Menagerie model of the G1.

    !!! note "Yours to check — the upstream licence terms if you reuse the G1 URDFs"
        Follow the mesh paths to mjlab and to Menagerie, and take the terms from
        there. *Owner: PI.*

- Vendor documents (not redistributed): RobStride 02/03/04
  manuals ([robstride.com/download](https://www.robstride.com/download)); SYD
  Dynamics TransducerM user guide
  ([download centre](https://syd-dynamics.com/download-center)); Amass
  XT30(2+2)-F.G.B datasheet; maxon,
  ["CAN bus topology and bus termination"](https://support.maxongroup.com/hc/en-us/articles/360009241840-CAN-bus-topology-and-bus-termination).

| Vendored SDK (in `deploy/control/hardware_bindings/`) | Licence | Notice |
| --- | --- | --- |
| FEETECH serial servo SDK, `ft_servo/` | MIT | `ft_servo/NOTICE.md`: upstream pinned at `064a6db`, one local fix in `SCSerial.cpp` |
| SYD Dynamics EasyProfile SDK (TransducerM TM171), `imu/EasyProfile/` | BSD-2-Clause | `imu/EasyProfile/NOTICE.md`: ship it alongside any binary of `imu_nanobind` |

!!! note "Yours to check — third-party SDK, firmware and EULA terms for what you install"
    *Owner: hardware lead.*
