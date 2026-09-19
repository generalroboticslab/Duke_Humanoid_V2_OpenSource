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

!!! unverified "UNVERIFIED — Canonical title: CITATION.cff and the BibTeX above give different titles"
    *Owner: PI.*

The umbrella repository's `CITATION.cff` lists the same authors and URL, under the
title "Duke Humanoid V2: a 31-DoF bipedal platform with two independently actuated
camera gimbals, designed around the visible-reachable workspace".

!!! missing "MISSING — Paper citation (preprint not posted) and which record covers the hardware"
    *Owner: PI.*

## Licence

| Artefact | Licence |
| --- | --- |
| Code (umbrella, simulation, deploy) | Apache-2.0 |
| Hardware design files (CAD, drawings, BOM) | **TODO**{ .dh-missing } not declared |
| This documentation and its figures | **TODO**{ .dh-missing } not declared |

Apache-2.0 grants no rights in a mechanical design.

!!! missing "MISSING — Hardware licence (e.g. CERN-OHL-S or -W) and documentation licence (e.g. CC-BY-4.0), with the licence file beside the CAD and on the download page; note V1 was MIT"
    *Owner: PI + the university's licensing office. Blocks the release.*

## Third-party material

- The workspace-study comparison models keep their own licences; the **Fourier
  GR-3 model is GPL-3.0** (the README says how to remove it).
- The two Unitree G1 URDFs in `simulation/asset/unitree_g1/` are cuRobo exports
  and ship without a `LICENSE` file; the README points to
  [mjlab](https://github.com/mujocolab/mjlab), which carries the MuJoCo
  Menagerie model.

    !!! missing "MISSING — Licence file for the two Unitree G1 URDFs"
        *Owner: PI.*

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

!!! missing "MISSING — Third-party terms: SDKs not vendored here (e.g. the RealSense SDK that deploy imports), component firmware and EULAs, and CAD derived from vendor models"
    *Owner: hardware lead.*
