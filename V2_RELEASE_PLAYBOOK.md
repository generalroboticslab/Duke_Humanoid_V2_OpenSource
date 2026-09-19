# Duke Humanoid V2 开源发布 Playbook

以 Menlo/Asimov、OpenArm 2.0、ToddlerBot 2.0、Berkeley Humanoid Lite 四个已发布项目为对标，
对照 `/Users/rivery/Desktop/DukeV2OpenSource/reference/duke-humanoid-v2/repo/` 的当前状态。

本文写给准备发布的 Duke 团队自己看，不是对外材料，所以直说问题。

---

## 1. 一句话结论

**V2 是一个优秀的软件发布和一个不存在的硬件发布**：仓库里有 0 个 BOM 文件、0 个机器人 CAD 文件
（3 个 `.step` 全是 perception 测试夹具）、0 条装配步骤、0 张爆炸图、0 个扭矩/螺纹胶规格、0 张线束图，
而论文的全部贡献恰恰是一个**物理设计选择**（两个独立驱动的相机云台）——
今天没有任何人能照着这个 release 把这台机器人造出来，
而项目页 `reference/duke-humanoid-v2/vrw-anonymous/docs/index.html` 还写着
"We will open source our entire software and humanoid hardware design"。

次要但同样致命的一点：即使今天决定发 BOM，内部的
`reference/bom/duke-humanoid-v2_BOM.xlsx` 也**不处于可发布状态**——
`$14,881.99` 这个总额逐行审计通不过（详见第 4 章）。

---

## 2. 四个对标项目速览

| 项目 | BOM 形式 | 装配文档 | CAD 发布方式 | 软件 | 文档站 | License | 成本透明度 |
|---|---|---|---|---|---|---|---|
| **Menlo / Asimov 1** | ❌ 无公开 BOM，Tally 表单索取；每步页有 "Parts needed" 表（78/83） | ★★★★ 83 步页、0 张照片、430 个可深链 3D 动画 | STEP(v0) / MJCF+URDF(v1)，裸 GitHub 路径，无 Release | API 文档好，训练代码 0 链接，固件不公开 | Next.js + Fumadocs，136 页，有 llms.txt + llms-full.txt | **完全没有**（全站 0 次 "license"） | ❌ 全站无任何价格 |
| **OpenArm 2.0** | ★★★★ 1.0 分 7 页、按子装配 ×制造类别，带照片/型号/单价/总价（JPY） | ★★★ 1.0 有 10 页 ~71 步 + 5 页布线；2.0 **没有** | STEP/STL/F360，1.0 在独立 repo，2.0 在 Google Drive 裸链接 | 9 repo 星座，apt PPA / uv / pip / Docker，HF 上有 ACT 权重 | Docusaurus 3.10，Algolia 搜索，有版本切换；无 llms.txt | ★★★★ CERN-OHL-S-2.0(硬件) / Apache-2.0(代码+文档)，逐 repo 标注 | ★★★ 1.0 逐行 JPY 价格 + 9 个分页小计，但从不打印跨页合计（把 9 个小计相加为 ¥587,586） |
| **ToddlerBot 2.0** | ★★★ 发布的 Google Sheet + repo 内 `toddlerbot_BOM_release.csv`，100 行，两个配置并列 | ★★ 一页 + 11 页 PDF（1.0 版，已过时）+ 14 个分装配视频 | Onshape（无版本号）+ MakerWorld 3MF；repo 内只有仿真 STL | 单 monorepo，conda+pip，权重在 Google Drive，一行命令跑 demo | Sphinx + Furo，42 页（20 页是 `api/` autodoc），无版本切换，无 llms.txt | ★★★ MIT(代码+文档) / **CC BY-NC-SA 4.0**(硬件) | ★★★★ 分档小计：本体 $5,727.94 / 工具 $1,976.13 / 可选 $2,252.73 |
| **Berkeley Humanoid Lite** | ❌ 只有一个 Google Sheet iframe，repo 内无文件、无导出 | ★★ `getting-started-with-hardware/` 6 页文字 + 9 个 YouTube 视频（装配两页里 6 个）；机械步骤几乎全靠视频 | Onshape（4 个活文档）+ MakerWorld 3mf；**GitHub Release assets 为空** | uv + uv.lock(261 包)，6 个 ONNX 权重 + 6 个配置 YAML 一一配对 | GitBook，27 页，有搜索 + AI 问答 + **llms.txt** | ★★ MIT(代码) / CC BY-SA 4.0(资产)；**文档无 license** | ★★ $4,312 US / $3,236 China 逐行，但只在论文 PDF 里 |
| **Duke V2（今天）** | ❌ 仓库内 0 个 BOM；内部 xlsx 不可发布 | ❌ 完全没有 | ❌ 无机器人 CAD；只有仿真网格（本体 17，`duke_v2/` 全部 338） | ★★★★★ 最强项：pinned deploy / 635 测试 / 权重带 md5 和训练命令 / 一行命令复现图 | ❌ 无文档站，靠 3 个长 README | ⚠️ 三 repo 统一 Apache-2.0，硬件/文档无单独声明 | ❌ 公开处 0 成本数据（全仓库仅两处美元数字，都是同一条相机数消融论证里的 "$600"） |

**这张表说明四件事。**
第一，四个项目没有一个在所有维度上及格，所以不存在"照抄某一个"的选项，只能逐维度挑最好的那个：
BOM 抄 OpenArm 1.0，装配可视化抄 Asimov，成本分档抄 ToddlerBot，工程笔记与复现实验抄 Berkeley。
第二，**最贵的错误都不是技术性的**——Asimov 有全世界最好的装配手册，却因为全站没有 "license" 一词
而在法律上不可被下游复用；Berkeley 把 $5,000 论点押在一个不能 diff、不能 pin、不能归档的 Google Sheet 上。
第三，V2 今天的形状和这四个都不一样：别人是"硬件发了但软件半成品"，V2 是"软件完成度最高、硬件为零"，
这意味着补齐的工作量是可以精确列举的（第 5 章），而不是弥散的。
第四，V2 在一个维度上做了四个对标都没做的事——`deploy/control/docs/auto_operator_safety_contract.md`
的 261 条编号安全机制（`SAFE-*-NNN`，3,411 行）和 `auto_operator_incidents.md` 的 10 条事故登记；
在本次抓取的四个镜像里 grep 不到等价物。
注意这只是**软件侧**的，而且它换不来任何人身安全保障（见 3.8）；
这个习惯应该被搬到机械侧，而不是当成已经覆盖了安全。

---

## 3. 逐维度差距分析

### 3.1 BOM

**别人怎么做的.** 最强样本是 OpenArm 1.0：
`reference/openarm/md/1.0/hardware/bill-of-materials/` 下 7 个页面
（`procuring-components.md` / `arm-manufactured.md` / `arm-off-the-shelf.md` / `gripper.md` /
`pedestal.md` / `end-effector-leader.md` / `electrical.md`），
**同时按子装配和按制造类别双重切分**，每页都分 "Manufactured Components" 和 "Off-the-shelf Components"，
leader 页再加第三块 "3D Printed Components"。
列是 Name | Photo | Model Number | Quantity | Unit Price | Total Price，
机加工件额外带 Manufacturing Method / Material / Manufacturer。
更关键的是它不是手写 markdown：每张表是 `reference/openarm/repo/website/src/components/*.tsx`
里的一个类型化数组，汇总页 `MechanicalComponentsTable.tsx` 直接 import 各表导出的 `*TotalCost()`，
所以**小计永远不可能和明细漂移**。
ToddlerBot 的贡献是另一维：`reference/bom/toddlerbot_BOM_release.csv` 把两个整机配置
（2XC / 2XM）做成**同一份物料表上的两对 QTY/Total 列**，并额外给出一行标注为
"$ of 2XC+ = $1,565.62" 的升级差价。

**V2 现状.** 仓库里 0 个 BOM 文件。全仓库的美元数字只有两处，且是同一条相机数消融论证的两次书写：
`README.md:197` 与 `simulation/mj_envs/asset_zoo/reachability_study/readme_reachability.md:193` 的 "approximately $600"。
内部 `reference/bom/duke-humanoid-v2_BOM_sheet1_main.csv` 是一张扁平表，
只有 ELECTRONICS(18 行) / HARDWARE(8 行) / MATERIALS(6 行) 三个分组，
没有按左腿/右臂/云台模块划分；MATERIALS 6 行全部无价，其中一行 LINK 列的内容字面是
`TODO: BREAK INTO INDIVIDUAL CNC PARTS`。

**差距.** 三层：(a) 根本没发；(b) 内部表没有子装配维度，所以读者无法只给相机云台模块报价——
而云台正是论文的全部卖点；(c) 内部表 6 行完全无价、另有 1 行是 `$0.00` 占位符、没有制造类别拆分、
0 个替代料、Sheet2 与 Sheet1 差 $450.76（第 4 章详述）。

**具体建议.** 见第 4 章的目标 schema。最小动作：把 BOM 作为
`hardware/bom/*.csv` 放进仓库（ToddlerBot 的做法），文档页从 CSV 渲染（OpenArm 的做法），
并按 `leg / arm / body / head_camera_module / gripper / electronics / harness` 七个子装配切分。

---

### 3.2 装配文档

**别人怎么做的.** 三种可抄的范式，强弱分明：
- **Asimov（最强）**：`reference/asimov/md/asimov/1/assembly-steps/` 下 83 个编号步骤页，
  按模块分（left-leg 14 / right-leg 14 / pelvis 9 / left-arm 17 / right-arm 17 / torso 12），
  子装配 A..F 并有显式 "Sub-assembly D (B + C)" 合并步。
  **全部 83 页 0 张照片**——每一句散文指令后面跟一个可深链的 3D 动画 iframe。
  md 里共 430 条深链；播放器 `project.json` 的 `steps` 字典有 431 个指令态，
  也就是有一个态没被任何页面引用。
  78/83 页顶部有自带的 "Parts needed"（Part | Count）表，
  紧固件精确到 **22 种尺寸**：M3–M5 确实是 18 种，但另有 M2.5x6 / M2.5x20 / M6x25 / M6x85 四种，
  所以引用时说"M2.5–M6 共 22 种"才不会让读者备错料；每处还区分 socket / flat head 并写明星形拧紧顺序。
  **螺纹胶只在准备页点名一次**：83 个步骤页里 "LOCTITE" 出现 0 次，
  步骤页一律只写 "Threadlocker | As needed"，牌号（LOCTITE 222 低强度，
  并写明 "do not substitute a high-strength grade"）在
  `reference/asimov/md/asimov/1/assembly-preparations/assembly-tools.md`。
  ToddlerBot 的手册第 1 页做了 Asimov 没做的一件事：给出总量——
  "All the screws that need threadlocker add up to about 100"，牌号 Vibra-TITE VC-3。
- **OpenArm 1.0**：`reference/openarm/md/1.0/hardware/assembly-guide/` 10 页 ~71 步 83 张图，
  每步一张只高亮被连接零件的 CAD 渲染，每步点名零件 ID 和紧固件数量
  （"Attach J5_A to the rotor of J5 motor using 6 M3x18 bolts"）；
  左右臂镜像差异用 inline TIP + 分手别照片处理；
  **每个子装配页开头有阻塞式 WARNING 强制你先配好 motor ID**——硬件步骤被固件前置条件门控。
  布线单列 5 页 66 张图：`reference/openarm/md/1.0/hardware/wiring-and-casing-guide/`。
- **ToddlerBot**：`reference/toddlerbot/repo/docs/_static/assembly_manual.pdf` 每个子装配页
  开头一个三段式套件清单 `Hardware: / Others: / 3D-print:`，精确到 "M2x8 (*18)"，
  并在第 1 页写下"先把所有五金分格清点，最后剩件即说明漏步"的验收协议。
  14 个分装配视频与 14 个手册章节一一绑定在同一页。

**V2 现状.** 完全没有。仓库有 82 个 `.png` 和 25 个 `.webp`，但每一张都是结果图：
`media/hardware.png` 是一张带橙色关节编号和绿色模块标签的论文尺寸图，不是装配辅助。
`grep -riE "loctite|threadlock|torque spec"` 返回空。
存在的是**已建成机器人的运维文档**，而且质量很高但起点在装配之后：
`repo/deploy/control/docs/SETUP.md`（673 行，纯软件/电气 bring-up）、
`repo/deploy/control/docs/OPERATIONS.md`（285 行，T0–T7 终端阶梯）。
唯一残存的机械提示埋在 OPERATIONS.md §3：
"Legs hang STRAIGHT when hanging the robot… three sessions died to this"——
这句话隐含吊装设备是工作流一部分，但该设备不在任何清单里。

**差距.** 从"有但不够好"到"零"的差距。没有任何单点改进能填，必须整体新建。

**具体建议.**
1. 目录结构照 Asimov 分模块：`docs/hardware/assembly/{leg,arm,torso,head-camera,gripper}/step-NN.md`，
   每个模块一个 Completion 页。
2. 每页顶部放 "Parts needed"（Part ID | Count）表，包括 "Threadlocker | As needed"——
   Asimov 78/83 页这么做，ToddlerBot 的分格清点协议是同一思路的另一半。
3. 每步一张只高亮被连接零件的渲染（OpenArm 做法），成本远低于 Asimov 的 3D 播放器；
   如果后续要上 3D，抄 Asimov 的 Origami 通道机制（第 6 章）。
4. **补 OpenArm 和 Asimov 都缺的那一项：扭矩值。** 两家都精确到螺钉规格和螺纹胶牌号，
   但全语料 0 个 N·m 数字——这是读者靠"再读仔细一点"补不上的唯一空白。
5. 用 OpenArm 的固件门控模式：每个子装配页开头写阻塞式警告，
   要求先完成 CAN ID 配置（V2 有六条 CAN 总线 can9/can21–can25，更需要这个）。
6. 把 OPERATIONS.md §3 的吊装要求（"Legs hang STRAIGHT when hanging the robot"）
   提升为装配前置条件，并把吊架/龙门作为一行写进 §4.2 的 `hardware/bom/tools.csv`
   （`class=off_the_shelf`，带 `vendor_url` 和最小承重 ≥ 36 kg 的 `notes`）——
   现在它只在一句运维散文里存在，任何清单都没有它。

---

### 3.3 CAD 与制造数据

**别人怎么做的.**
- **格式与托管**：OpenArm 发 STEP + STL + Fusion 360；ToddlerBot 的出厂格式是
  MakerWorld 上的**预切片 3MF**（`03_3d_printing.md` 全文只有 12 行："For BambuLab users, hit print"）；
  Berkeley 同样走 Onshape + MakerWorld。
- **最该抄的一条反例**：Berkeley 的 `reference/berkeley-humanoid-lite/releases.json`
  两个 tag 的 `"assets": []`——**GitHub Releases 里没有任何二进制**，
  而它自己的 assets 子模块里就躺着一个 57 行的
  `repo/source/berkeley_humanoid_lite_assets/.github/workflows/release.yml`，
  在每个 `v*` tag 上打包 `data/` 并上传。模式已经证明可行，只是没用在主仓库上。
- **打印参数**：Berkeley 把两个 profile（Actuator Housing / Actuator Shaft，针对 Bambu Lab X1C）
  写成 13 张截图
  （`docs-site/md/getting-started-with-hardware/3d-printing-instructions.md`），
  **文字里一个数字都没有**——没有层高、壁数、填充率、喷嘴温度。这是负面样板。
- **机加工数据的最佳解法**：OpenArm 给全部 32 个机加工/钣金件（arm 27 + gripper 4 + pedestal 1）登记了 MISUMI MEVIY 型号
  （如 `MVBLK-ASN-48S-4BGUX-L`），`procuring-components.md` 因此可以写
  "Method 2（推荐）：把型号粘进 MISUMI 页面，填数量，下单"，并加一句
  "this method ensures you get the exact geometry we've validated"。
  这一条同时消除了 CNC 件最大的批次间方差来源。

**V2 现状.** 全仓库 CAD 格式文件 3 个，全部是 perception 夹具：
`deploy/perception/asset/tag_cube_creation/v2_wrist_interface.step`、
`deploy/perception/asset/tripod_base/tripod_platform_v6.step` 和 `_v8.step`。
`simulation/README.md` 自己写明了排除："What this export leaves out: The original CAD (`*.step`)…"。
已发布的只有仿真几何。`simulation/asset/duke_v2/` 全树 338 个网格（337 `.obj` + 1 `.stl`），
但分布极不均衡：本体 `humanoid_v21/` 17 个（16 `.obj` + `base_link.stl`）、2 个 MJCF、6 个 URDF；
`parallel_gripper/` 28 个；`cartesian_hand_v3/` 288 个（一个已被取代的旧末端）；
而**论文的全部卖点 `head_cam/` 只有 5 个网格**——数量最多的是弃用件，卖点最少。
**0 张尺寸图纸，0 条公差，0 个打印参数。**

有一条已有的强实践值得保住：确定性。每个 MJCF 旁边都有生成脚本
（`humanoid_v21_creation_v3.py`、`head_camera_creation.py`、`parallel_gripper_creation.py`），
README 声明脚本能 bit-identical 重生成已提交 XML，"a non-empty `git diff` after running one means something drifted"。

**差距.** 机器人 CAD 为零；且 asset README 已经对不上导出内容——
`simulation/asset/duke_v2/humanoid_v21/README.md` 指向 `meshes/source_stp/`、
`humanoid_v21_high_res.xml`、`humanoid_v21_resolved.xml`、`cartesian_hand_v2/`、`asset/robot_studio`，
`simulation/asset/duke_v2/README.md` 指向 `cartesian_hand/`（实际目录是 `cartesian_hand_v3/`），
**六条路径全部不存在**。

**具体建议.**
1. 每个制造件发 STEP，每个打印件发 STL + 3MF，**挂在打了 tag 的 GitHub Release 上**
   （抄 Berkeley 那个 57 行 workflow，别抄它的空 assets）。
2. 打印参数**写成文字数字**再附 3mf：材料、层高、壁数、填充、方向、支撑。
   Berkeley 的 13 张截图是任何切片器、任何搜索引擎、任何其他打印机都读不了的。
3. 63 个 CNC 件补齐 material / tolerance class / finish / supplier 四列，
   并考虑 OpenArm 的 MEVIY 路线：如果能把件登记到一家在线机加工商，
   BOM 里那一串型号就取代了"上传 STEP 并祈祷对方读懂意图"。
4. 加一个导出期 link checker，任何 README 里指向不存在路径的链接直接 fail release——
   上面那六条死链就是这么漏出去的。

---

### 3.4 软件

**别人怎么做的.** OpenArm 的 9-repo 星座 + `reference/openarm/repo/README.md` 的
Repository | Documentation | License | Description 表；
`md/tutorial/inference.md` 里那份正式的 "Policy Server Contract"
（UNIX socket、Arrow IPC 观测包、JSON 动作块，以及显式的 16-DoF 布局
`right_arm[7]|right_gripper[1]|left_arm[7]|left_gripper[1]`）——这是让模型可替换的正确做法。
Berkeley 的 6 个 ONNX 权重与 6 个部署 YAML 一一配对（关节顺序、逐关节 kp/kd、力矩上限、控制周期）
让陌生人在买硬件之前就能跑真实策略。
ToddlerBot 的 `run_policy.py --policy replay --path motion/push_up_2xc.lz4 --vis view` 无需硬件无需下载。

**V2 现状.** 这是全项目最完成的一块。按"陌生人能否在不碰硬件的前提下复现论文数字"这一条衡量，
它强于四个对标中的任何一个（Berkeley 有权重但无离线测试套件，ToddlerBot 有一行命令 demo 但权重在
Google Drive，OpenArm 和 Asimov 都不发训练侧）：
- 三 repo 分离（umbrella / simulation / deploy），各自保留 history 和 issue tracker；
- `repo/.githooks/pre-push` 会阻止 submodule 指针落后于 checkout 的推送，注释里写明它防的是哪次事故；
- 依赖 pinning 故意分裂且两边都自证：`deploy/requirements.txt` 26 个包全 `==` 且注明
  "taken from the robot computer's environment rather than from a resolver"（Python 3.12.13）；
  `simulation/requirements.txt` 21 个裸包名，头部写 "Unversioned on purpose: install current releases"；
- 权重随仓库发布（3 × ~20 MB `.pt`，README 带 md5、训练命令、源 run 目录），
  并**公开记录了一次有缺陷的 sweep（dyn8）和一次被否决的晋升（dyn11，P_g1 0.092 vs 0.989）**；
- 三条一行命令的 demo，635 个离线测试（无需机器人/相机/GPU，2026-08-28 实测 190s）；
- `deploy/control/legged_env_bundle/` 用 byte-exact 上游形状子集解决了不可发布依赖，
  并精确点名什么仍然不工作（cuRobo plan server、`rebuild_deploy_model.py`）。

**差距.** 小而具体：
(a) checkpoints README 的文件表列 5 个 `.pt`，导出里只有 3 个——缺的两个是 dyn11 被否决的
cosine ckpt。`REPRODUCE.md` 本身是对的（"Three checkpoints therefore cover five columns"），
所以矛盾不在两份文档之间，而在 checkpoints README 内部：它一边写
"Do not add a checkpoint here without adding its row below"、一边写
"Cosine ckpts retained in checkpoints/ for inspection"，而导出里它们并不在；
(b) 三个 repo 都没有 tag、没有 release、没有 CHANGELOG，所以没人能 pin 到已知良好状态；
(c) 没有 policy/observation 契约文档（OpenArm 有），外部模型无法替换；
(d) `simulation` 侧写了"故意不 pin"的理由，却**没有配一份已测版本清单**——
全文 grep 不到任何 tested-configuration / known-good 版本记录，
`REPRODUCE.md` 的 "## Verified" 只说了在一张 RTX 4090 上跑过，没说跑的是哪些包版本。
理由成立不代表读者能复现：mjlab / mujoco-warp 上游一动，就没有已知良好解。
最小修法是提交一份 `simulation/requirements.lock.txt`（`pip freeze` 于跑出 Verified 那次的环境），
pin 的理由段原样保留，两者不冲突。

**具体建议.** 打 tag + 写 CHANGELOG（见 5.1）；
补一页 deploy 侧的观测/动作契约（31 DoF 的关节向量布局、50 Hz 策略周期、200 Hz CAN 环）；
把 checkpoints README 的表纳入导出期校验。

---

### 3.5 文档站

**别人怎么做的.** 四种生成器都被用过：Next.js+Fumadocs(Asimov 136 页)、
Docusaurus 3.10(OpenArm，Algolia 搜索 + 版本切换)、Sphinx+Furo(ToddlerBot 42 页，在 repo 内)、
GitBook(Berkeley 27 页)。
两个具体机制值得单独点名：
- **llms.txt**：Asimov 同时发 `reference/asimov/llms.txt`（28 KB 带注释导航）和
  `llms-full.txt`（599,878 B / 10,797 行，整站一个可 grep 文件）；
  Berkeley 的 `reference/berkeley-humanoid-lite/docs-site/_html/llms.txt` 只有 3.4 KB 就覆盖全部 27 页，
  且每页都能以 raw Markdown 取回。
- **文档与代码同仓同 PR**：ToddlerBot 的 `docs/` 在 repo 内、CI 每次 push 构建；
  Berkeley 的 GitBook 与 repo 完全解耦，**直接后果**是文档里 7 条 `python …py` 命令只有 3 条按字面可用
  （`scripts/rsl_rl/train.py`、`play.py`、`scripts/sim2sim/play_mujoco.py`）：
  2 条文件确实存在但路径写错（文档写 `berkeley_humanoid_lite_lowlevel/motor/ping.py` 和
  `…/robot/test_imu.py`，实际在子模块的 `scripts/motor/ping.py` 和 `scripts/test_imu.py`）、
  2 条文件全仓不存在（`policy/udp_joystick.py`、`robot/anyonehere.py`）、
  Isaac 版本停留在 4.5.0/2.1.0（pyproject 是 5.1.0/2.3.2.post1）、
  还有一处字面占位符 "press XXXX during bootup"。

**V2 现状.** 没有文档站，也没有任何生成器配置（全树无 mkdocs.yml / conf.py / docusaurus.config.* / llms.txt）。
替代物是三个长 README（umbrella 388 行自带 9 条 TOC 锚点）、
`deploy/control/docs/` 下的私有文档集（顶层 11 个 `.md`，含 `design-notes/` 共 14 个）、
以及一个未与 repo 互链的匿名项目页 `reference/duke-humanoid-v2/vrw-anonymous/`。
全 release 只有一个图示文件：`deploy/control/docs/figures/curobo_pipeline.svg`。

**差距.** 硬件文档一旦写出来，用 README 承载会立刻崩溃——
Asimov 是 136 页、OpenArm 108 页、ToddlerBot 42 页，没有一个能塞进 README。

**具体建议.** 选 **MkDocs Material**，不要 Sphinx——ToddlerBot 证明了 Sphinx 可行，
但它 42 页里 20 页是 autodoc，V2 的硬件文档一页 autodoc 都不需要，
而 MkDocs 的单文件 `mkdocs.yml` 比 Sphinx 的 `conf.py` + 扩展链省一个数量级的维护量。
落地清单：
- umbrella repo 根目录放 `mkdocs.yml`，文档源码放 `docs/`（Berkeley 的教训：GitBook 与 repo 解耦 → 4 条命令失效没人发现）；
- `nav` 顶层四节 `hardware / assembly / software / simulation`，硬件侧按修订版本开子树（`docs/hardware/v2.1/`），
  抄 Asimov 的"每个硬件版本一棵独立树"而不是版本下拉，这样 v2.1 页面永不腐烂；
- 开 `strict: true`（MkDocs 里等价于 OpenArm 的 `onBrokenLinks: 'throw'`），CI 里 `mkdocs build --strict` 即 link check；
- 装 `mkdocs-llmstxt` 产出 `llms.txt`，并让构建把每页 `.md` 原文一并发布（Berkeley 的做法，3.4 KB 覆盖 27 页，成本近似为零）。

---

### 3.6 License

**别人怎么做的.** OpenArm 是唯一做对的：硬件 CAD 走 **CERN-OHL-S-2.0**
（`github.com/enactic/openarm_hardware/LICENSE.txt`），其余 8 个 repo（含文档站本身）全 Apache-2.0，
而且在 `reference/openarm/repo/README.md` 的 9 行 repo 表里逐行标注 license，
并在 `md/1.0/hardware/assembly-guide/find-cad-files.md` **读者正要下载的那一页**再声明一次。
ToddlerBot 明确分家：MIT（代码+文档）/ CC BY-NC-SA 4.0（Onshape + STL 等设计）——
NC 条款正是它的整机售卖行需要挂免责声明的原因。
Berkeley 分了 MIT（代码）/ CC BY-SA 4.0（资产）但文档无 license。
**Asimov 是反面极值**：136 页 + 599,878 字节的 llms-full.txt 里 "license" 一词出现 0 次，
同时自称 "A Fully Open Platform"——下游实验室因此对已公开的 STEP/URDF/MJCF 没有任何合法衍生权。

**V2 现状.** 三个 repo 统一 Apache-2.0，三个 CITATION.cff 都声明 `license: Apache-2.0`。
第三方处理大体干净：`simulation/asset/` 下 5 个第三方资产各带自己的 LICENSE
（booster_t1 / apptronik_apollo / pal_talos / fourier_gr3 / toddlerbot_2xm_gripper），
`README.md` 的致谢表逐行标注 license 并**加粗点名唯一的 GPL 污染**
（"**The Fourier GR-3 model is GPL-3.0**"）并给出一句话的移除指令；
两个厂商 SDK 带 NOTICE 文件；`deploy/PROVENANCE.md` 用 URL + commit pin 全部第三方。

**但这一段不能整个当成强项**：致谢表上方那句 "Each keeps its upstream `LICENSE` beside its meshes"
对 `simulation/asset/unitree_g1/` 不成立——该目录只有 `g1_curobo.urdf` 和 `g1_full.urdf` 两个文件，
没有 LICENSE，表里那一行写的是 "see mjlab"。G1 恰好是论文里的头号 baseline。

**差距.** 今天没有硬件可覆盖所以问题未爆发，但 Apache-2.0 不是物理设计的合适工具，
文档与图表也没有 CC-BY 之类的授予。这是一个**尚未做出的决定**，且 release 没有承认它是开放问题。

**具体建议.** 发布时写一个 `LICENSES` 段落，三分：
代码 Apache-2.0 / 硬件与 CAD CERN-OHL-W 或 CERN-OHL-S（抄 OpenArm）/ 文档与图表 CC-BY-4.0。
选 W(weak) 还是 S(strong) 是团队的策略决定：S 要求衍生硬件也开源，W 不要求。
并且照 OpenArm 的做法，在 "下载 CAD" 那一页**再声明一遍**，因为 license 不会跟着文件走。

---

### 3.7 社区与支持

**别人怎么做的.**
- **OpenArm 最完整**：`repo/CODE_OF_CONDUCT.md`(5,484 B)、`CONTRIBUTING.md`、
  `.github/ISSUE_TEMPLATE/{1-bug-report,2-feature-request}.yml`（`blank_issues_enabled: false`）、
  Discord 频道图（#projects #faq #updates #weekly #hardware #controls），
  以及一个很聪明的机制：`repo/website/scripts/fetch-popular-issues.sh` 在 CI 里每晚跑，
  把 GitHub API 的 top-upvoted issues 生成 `static/data/popular-issues.json`，
  由 `repo/website/src/components/GitHubIssues.tsx` 渲染成 contribute 页上的实时"可认领工作队列"。
  还有 `preview-comment.yaml`：每个 docs PR 自动评论一个 GitHub Pages 预览 URL。
- **ToddlerBot 的支持契约最值得抄**：README 明写
  "we will ONLY monitor GitHub Issues and likely ignore questions from other sources"，
  接四条前置条件（读文档含 Tips and Tricks、读脚本注释、读装配手册、看装配视频），
  然后 "If we determine that your issue arises from not following these resources, we are unlikely to respond."
  它的 `bug_report.yml` 还是硬件感知的：必填 OS 下拉里直接是
  Linux / MacOS / Windows / Jetson / ROG Ally X / Steam Deck。
- **Berkeley 的 v1.1.0 release note 写成社区报告**：点名 12 位外部建造者，嵌入社区拼图和 3 个社区视频。

**V2 现状.** `find . -path "*.github*"` 在三个 repo 里返回**零个文件**。
没有 CONTRIBUTING、没有 CODE_OF_CONDUCT、没有 SECURITY.md、没有 issue 模板、没有 PR 模板、
没有 CI、没有 Discord/论坛/mailing list、没有 FAQ 页。
唯一的支持渠道是三个 repo 里访客自己猜的那一个 issue tracker，没有模板也没有响应政策。
故障排查写得其实很好，但是散在需要它的地方（`simulation/README.md` 的 CUDA 分支、
`SETUP.md §2 Common problems`、`OPERATIONS.md §4` 的 retreat-verdict 分诊表）。

**差距.** 全缺。这是九个维度里最空的一个。

**具体建议.** 一天之内可以做完的最小集：
`.github/ISSUE_TEMPLATE/{bug,hardware-build-question,reproduction-report}.yml` +
`PULL_REQUEST_TEMPLATE.md` + `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md` +
一个跑现有 635 测试的 CI workflow；
外加抄 ToddlerBot 的单方面支持契约（两人维护负担下这是唯一可持续的写法）。

---

### 3.8 安全

**别人怎么做的.** OpenArm 的 `reference/openarm/md/overview/safety-guide.md` 是开源硬件里罕见的好：
6 条配图要求（固定安装、保持距离、PPE 含强制护目镜、负载上限、E-stop 就绪、持续风险评估）
+ 4 项维护检查表（紧固件松动、机械限位损坏、关节异响、线缆连接器损伤），
并且**点名这个设计自己制造的危险**——"if power is lost due to an emergency stop,
the load being held will fall rapidly"，因为电机是可反驱的。
ToddlerBot 把电池安全写在 `features/03_diy_battery.md` 的 6 条 "Safety First!" 里。
Asimov 没有独立安全页但分布式安全做得扎实，并且**主动撤回未验证的验证章节**：
`reference/asimov/md/asimov/1/assembly-verifications.md` 写
"Do not use earlier drafts to approve power-on, motor zeroing, firmware activation, motion, or operation"。

**V2 现状.** 判断要分开说。
**软件安全侧的文档密度是四个对标里最高的**（这是文档密度，不是安全性本身的证明）：
`repo/deploy/control/docs/auto_operator_safety_contract.md` 3,411 行、261 条编号机制
（SAFE-NAV-001 … SAFE-GAPS-015），每条给出触发条件、响应、常数、起源事故、覆盖它的测试，
包括诚实标注 "**Tests:** none (mechanism lives robot-side; assumption untestable in this harness)"；
旁边 `auto_operator_incidents.md` 是 10 条事故登记（INC-1 … INC-10），
每条点名那个"看起来冗余、其实承重"的简化会把事故带回来。
**人身安全则是零**：没有 e-stop 流程、没有断电顺序、没有两块 6S 10000mAh 22.2V 锂电的处置指引、
没有旁观者安全距离、没有 PPE、没有上锁挂牌、没有吊架/支架规格——
而 OPERATIONS.md 本身就说这套栈 "drives a 36 kg humanoid with people beside it"，
且 §3 依赖机器人被吊起来。

**差距.** 一个 36 kg、1.2 m 的双足机器人在没有任何人身安全文档的情况下发布，
是本次 release 里**唯一有实际伤害风险**的缺口。

**具体建议.** 写 `docs/safety.md`，照 OpenArm 的结构，但内容必须是 V2 特有的危险：
6S 锂电充放存与火灾、E-stop 按钮位置与断电顺序、首次上电必须吊在架上、
旁观者距离、QDD 失电后腿部塌落（V2 是准直驱，和 OpenArm 的可反驱问题同类）、
以及一份定期检查表。同时把 OPERATIONS.md §3 那条 "three sessions died to this" 升格成 INC 编号条目。

---

### 3.9 可复现性证据

**别人怎么做的.** 三个层级，由弱到强：
- **ToddlerBot 把可复现性做成论文里的一个 Results 小节**
  （`reference/toddlerbot/project-page/md/index.md`）：在第二台实体机上做三个可证伪的实验——
  在 1 号机采集数据训练的操作策略 zero-shot 跑在 2 号机上（`hug_transfer.mp4`）、
  两台机协作完成长时序整理房间任务（`collaborate.mp4`）、1000× 加速的从零建造延时（`assembly_1000x.mp4`）。
  **跨实例策略迁移是正确的度量**，因为它一旦失败就是响亮的失败，同时检验了 CAD、打印配置、
  校准流程和手册四件事。诚实的地方：第二台是 Kaizhe Hu 建的，此人列在 2.0 团队名单里，
  所以"独立复现"是"另一个人照公开文档"，不是"另一个实验室"。
- **Berkeley 做了制造级复现实验**，注意是**两个分开的实验**，不要合并引用：
  (1) 跨打印机一致性（论文 Fig. 11）：在**两台不同的 3D 打印机**（P1/P2）上各打印 6512 执行器，
  比较 1 rad/s 下的平均效率与力矩跟踪误差，结论是力矩误差全程在 ±0.5 N·m 内；
  (2) 位置精度：另测 6 个新打印执行器的背隙，最大 0.0229 rad、标准差 0.0042 rad。
  (1) 直接回答了每个潜在建造者真正的问题："在我的打印机上能行吗"。
  外加 60 小时连续耐久测试（0.5 kg 摆、0.5 m 臂、-45°~+90°、0.5 Hz；
  前 12 小时每小时、之后每 12 小时暂停一次复测效率和背隙）。
  它的 v1.1.0 release 点名 12 位外部建造者，仓库 HEAD 本身就是外部贡献
  （PR #50，社区成员做的 Isaac Sim 5 迁移）。
- **OpenArm 把可复现性变成供应链**：`reference/openarm/md/purchase.md` 列 10 家厂商，
  带质量分级（Official Partner / Certified ★★★ / Evaluating / Not evaluated）、真实价格、交期、联系方式，
  并点名一家不兼容的仿制品。两家厂商用各自方式解决了同一个 LCSC 连接器干涉问题，都被拍照记录在
  `md/1.0/hardware/wiring-and-casing-guide/components.md`。

**V2 现状.** **没有任何证据表明团队之外有人造过这台机器人，也没有任何机制让人能造**——
没有 BOM、没有 CAD、没有装配文档，所以外部硬件复现是"不可能"，而不只是"未被证实"。
无装配工时估计、无 build log、无套件供应商、无复现实验。
软件/结果复现则明显优于平均：`simulation/REPRODUCE.md` 有专门的 "## Verified" 段，
记录在什么硬件上验证了什么，并诚实说明非确定性
（"The GPU contact solver is not bit-reproducible, which is why each configuration is repeated 3 times"、
"verdicts are not host-portable"），以及"重训不会复现出已发布的字节，这就是产物被提交而非被描述的原因"。
README 的 "Where each paper artifact lives" 表逐条给出再生成成本，
并诚实写下 deploy 那一行 "not reproducible offline, needs the robot"。

**上一代的教训值得记住**：Duke Humanoid V1 把硬件文档全部放在外部 Notion 页
（`reference/duke-humanoid-v1/repo/README.md` 里的 "Hardware wiki" 链接），
未版本化、在仓库之外，**今天已经私有**，参考资料库记录它是唯一完全无法归档的条目。
V2 没有重复这个错误——它只是还没有把硬件文档发到任何地方。

**差距.** 硬件复现证据为零，且今天不可能产生。

**具体建议.**
1. 发布时至少给出一个装配工时估计，写成 `docs/hardware/assembly/index.md` 顶部的一张三行表
   （子装配 | 人时 | 是否需要第二个人），数字取自团队自己上一次完整装配的记录即可，
   并注明"这是熟悉设计的人的耗时，首次装配请按 2–3 倍估"。
   Berkeley 只用了一句 "the entire robot can be assembled in about three days" 就足够，
   V2 现在连这一句都没有。
2. 中期做一个 ToddlerBot 式的跨实例实验：照公开文档建第二台，
   把 1 号机训练的策略 zero-shot 部署到 2 号机，跑一个双机任务。
   对 V2 尤其合适——相机云台的标定误差会立刻暴露在 VRW 指标上。
3. 把 Berkeley 的打印机一致性实验思路移植到 V2 的 CNC 件上：
   同一批图纸在两家不同加工商各做一套关键件，比较装配后的关节背隙。

---

## 4. BOM 专章

### 4.1 `$14,881.99` 能不能作为公开数字使用

**不能。** 理由是算术上的，不是措辞上的。我自己核对过两张表：

| 检查项 | 结果 |
|---|---|
| Sheet1 的 25 个有价行求和 | `$8,492.13` |
| Sheet1 的 `TOTAL CNC` | `$6,389.86` |
| 两者相加 | `$14,881.99` ✅ 与 GRAND TOTAL 精确相符 |
| Sheet2 的 63 个零件行 UNIT COST 列求和 | `$6,840.62` ❌ 与 `$6,389.86` 差 **$450.76** |
| Sheet2 的 UNIT COST × QUANTITY | `$16,009.04` ❌ 是所谓 CNC 总额的 2.5 倍 |
| Sheet2 注释行记录的四个小计 2076.98 / 1374.19 / 1317.87 / 1620.82 之和 | `6,389.86` ✅ 与 `TOTAL CNC` 相符 |
| 这四个小计能否切分 63 行 | ✅ 四块全部精确对上：第 1–15 行 = 2076.98、第 17–26 行 = 1374.19、第 28–37 行 = 1317.87、第 39–63 行 = 1620.82 |
| 四块一共覆盖多少行 | 60 行。**跳过的正是第 16、27、38 行** |
| 被跳过的三行 | `CNC_arm13_x2_RS05_shaft_coupler` $109.80 + `CNC_arm11_x2_wrist_roll` $239.58 + `B6_single_leg_tester_plate` $101.38 = **$450.76**，与缺口一分不差 |

**所以缺口不是谜，是可解释的。** 这四个小计是四批加工报价；那三行是报价之后补进表里、
再没有人把它们并回 `TOTAL CNC` 的。`$14,881.99` 因此不是"算错了"，
而是**算的是四批报价 + 电子件，不是这张零件表**——对内可用，对外发布就是错的，
因为外部读者会按零件表重算并得到不同的数。

修正后可用的数字有三个，发布时必须明确说清用的是哪一个：

| 口径 | CNC 小计 | 整机（+ Sheet1 的 $8,492.13） |
|---|---|---|
| 表里现状（漏 3 行） | `$6,389.86` | `$14,881.99` ← **不要对外用** |
| 全部 63 行 | `$6,840.62` | `$15,332.75` |
| 全部 63 行，剔除测试夹具 `B6` | `$6,739.24` | `$15,231.37` ← **最接近"整机机加工成本"** |

三个数字全部**不含**增材件与紧固件（见下），所以真实整机成本高于 `$15,231.37`，
高多少目前无法从这两张表得出。

具体缺陷清单：

1. **6 行完全无价**：`CNC Leg Parts`（LINK 列字面写着 `TODO: BREAK INTO INDIVIDUAL CNC PARTS`）、
   `CNC Arm Parts`、`CNC Body Parts`、`TPU`、`PLA`、`Nylon Powder for SLS` 全无单价/数量/总价/链接。
   第 7 行（紧固件）不是空白而是 `$0.00`，见下条——空白和 $0 的区别是：空白不进求和，$0 进了。
2. **紧固件根本没计价**：HARDWARE 组第一行字面是 `example: fasteners, nuts`，`$0.00`，无链接。
   一台 31 DoF 机器的每一颗螺钉、螺母、轴承现在是一个 $0 占位符。
3. **Sheet2 的 `UNIT COST` 列名是错的**：它实际是行总价（乘以数量后得 $16,009.04），
   所以读者无法用这张表给单个备件报价。
4. **命名体系混用**：36 行是 `CNC_leg01..18 / CNC_arm01..13 / CNC_body01..04`，
   22 行是 `01_m03_shaft_x3` / `08_hip_1_back_shaft_x2` 这类旧编号，5 行是 `B1_body_base_plate` 这类。
   后两类看起来是更早的单腿测试架遗留。
5. **测试夹具混在机器人总额里**：`B6_single_leg_tester_plate`（$101.38）不是机器人零件。
6. **重复行**：`CNC_leg02_x7_RS03_shaft_coupler` 出现两次，价格数量都不同（$274.02/6 和 $100.26/2）。
7. **数量与零件名内嵌计数矛盾**：63 行里**实测 25 行不一致**（脚本比对名字里的 `_xN` 与 QUANTITY 列）。
   例：`CNC_arm13_x2_...` 数量写 3；`CNC_leg12_x4_...` 写 5；`CNC_leg02_x7_...` 写 6 和 2；
   22 个旧编号行几乎全部不一致（`08_hip_1_back_shaft_x2` 写 1、`15_ankle_cap_x4` 写 2……）。
   格式也不统一（只有 `CNC_leg18_x2_foot_plate` 一行写 `2pcs`，其余写纯数字）。
   把数量编进零件名正是这 25 处冲突的来源，新 schema 里禁止这么做。
8. **63 个 CNC 件全部没有材料、公差、表面处理、供应商**。
9. **0 个替代料**。而 BOM 里恰恰有两类高风险件：
   `RealSense Depth Camera D436`（$354 × 2，RealSense 产品线供货一直不稳）
   和 6 种 Robstride QDD 执行器（31 个，占 $5,605）。
10. **3D 打印没有从 CNC 里拆出来**：TPU / PLA / Nylon Powder for SLS 三行裸挂在 MATERIALS 下，
    无成本、无数量、无打印机、无供应商。

### 4.2 目标 schema

模型取自 OpenArm（子装配 × 制造类别双切分 + 照片 + 型号 + 单价 + 总价）
和 ToddlerBot（单一物料表上并列多配置 + 分档小计）。

建议在仓库内落 `hardware/bom/` 目录，**一个子装配一个 CSV**，加一个汇总脚本：

```
hardware/bom/
  leg.csv
  arm.csv
  body.csv
  head_camera_module.csv     ← 论文卖点，必须能单独报价
  gripper.csv
  electronics.csv
  harness.csv
  tools.csv                  ← ToddlerBot 把工具单列成 $1,976.13 一档
  _totals.py                 ← 读全部 CSV，生成文档页和 GRAND TOTAL
```

每个 CSV 的列（全部必填，除标注外）：

| 列名 | 说明 | 依据 |
|---|---|---|
| `subassembly` | leg / arm / body / head_camera / gripper / electronics / harness | OpenArm 按子装配分页 |
| `class` | `off_the_shelf` / `machined` / `printed` / `consumable` | OpenArm 每页分 Manufactured / Off-the-shelf / 3D Printed，三类交期和失败模式完全不同 |
| `part_id` | 内部件号，与 CAD 文件名和装配步骤页一致 | OpenArm 每步点名 `J5_A`；Asimov 每步页 "Parts needed" 用 `600_03C` |
| `description` | 人可读名称 | 全部对标 |
| `mpn` | 制造商料号（现货件）或加工商登记号（机加工件） | OpenArm 的 MEVIY 型号 `MVBLK-ASN-48S-4BGUX-L` |
| `vendor` | 供应商名 | OpenArm / ToddlerBot |
| `vendor_url` | 采购链接 | ToddlerBot 100 行每行都有 |
| `alt_mpn` / `alt_url` | 替代料（可空，但 D436 和 Robstride 必须填） | ToddlerBot 有 Alternative Link 列；OpenArm 缺这项是它的已知弱点 |
| `qty_per_robot` | 整机用量，纯数字（禁止 `2pcs`） | 修复现有格式不一致 |
| `unit_cost_usd` | **真·单价**（现 Sheet2 是行总价，必须换算） | — |
| `total_cost_usd` | = qty × unit_cost，由脚本生成而非手填 | OpenArm 用 `*TotalCost()` 保证不漂移 |
| `material` | 机加工/打印件填 Al6061 / PA12 / TPU 等 | OpenArm 机加工行带 Material |
| `process` | CNC / sheet_metal / FDM / SLS | OpenArm 带 Manufacturing Method |
| `tolerance_finish` | 公差等级与表面处理（机加工件必填） | 四个对标都缺，是 V2 可以做得更好的地方 |
| `lead_time_days` | 交期（可空） | OpenArm purchase 页每家厂商都标交期 |
| `notes` | 自由文本，放坑与提示 | ToddlerBot 的 Note 列（"Can replace with Jetson Orin Nano if budget is tight"） |

打印件额外需要一张 `hardware/print_profiles.csv`：
`part_id, material, layer_height_mm, walls, infill_pct, orientation, supports, printer_tested`。
Berkeley 把这些做成 13 张截图是明确的反面教材。

### 4.3 迁移路径

按这个顺序做，每一步都能独立完成：

1. **拆 CNC 三行**。把 Sheet1 的 `CNC Leg/Arm/Body Parts` 三行删掉，
   用 Sheet2 的 63 行直接填进 `leg.csv` / `arm.csv` / `body.csv`——
   `CNC_leg*` / `CNC_arm*` / `CNC_body*` 的前缀已经给出了归属。
2. **清理 Sheet2 的历史残留**。22 个 `01_m03_shaft_x3` 式旧编号和 5 个 `B*` 行需要人工判定：
   哪些是现行零件的旧名（合并进对应 `CNC_*` 行）、哪些是单腿测试架遗留（删除，
   包括 `B6_single_leg_tester_plate`）。这一步会解释掉大部分 $450.76 的缺口。
3. **改列名并换算单价**。`UNIT COST` → `total_cost_usd`，再除以 `qty_per_robot` 得 `unit_cost_usd`。
   同时消解 `CNC_leg02` 的重复行和三处数量矛盾。
4. **补紧固件**。从 CAD 生成一张真实的紧固件清单（规格 × 数量），替换 `example: fasteners, nuts` 占位符。
   Asimov 步骤页里实测出现的 22 种尺寸（M2.5–M6）是可参考的粒度。
5. **给材料定价**。TPU / PLA / SLS nylon 按质量估算（ToddlerBot 的做法：
   `PLA-CF 1KG ×2 = $69.98` + `PLA 1KG ×1 = $19.99`，按耗材卷计价而非按件）。
6. **补两个高风险件的替代料**：RealSense D436 和 Robstride 系列。
7. **分档小计**。抄 ToddlerBot：本体 / 工具 / 可选（第三个相机模块的 ~$600 正好放这里），
   并在文档页上把三档和整机合计都打印出来。OpenArm 在这一点上只做了一半：
   `versioned_docs/version-1.0/hardware/bill-of-materials/procuring-components.mdx` 里的
   `<BoMSummary />` 会渲染**三个**类别合计（`ActuatorsTable` ¥397,356 / `MechanicalComponentsTable`
   ¥478,518 / `ElectricalComponentsTable` ¥84,564，各自打印在自己的 `<h3>` 里），
   **但从不把这三个数加起来**——读者得自己算出 ¥960,438 才知道一条手臂多少钱。
   注意别把 leader end-effector 的两张表（¥24,504）算进整机：那是遥操作主手，不是手臂本身。
8. **标注日期**。所有价格加一个 `priced_as_of` 日期（OpenArm 那三个 JPY 合计都没有日期，是它被点名的弱点）。

完成 1–5 步之前，**任何对外材料都不要引用整机成本数字**。

---

## 5. 优先级路线图

### 5.1 发布前必须做（没有这些就不该称为 open-source hardware release）

| 项 | 工作量 | 哪个对标证明它值得做 |
|---|---|---|
| 决定并声明三段 license：代码 Apache-2.0 / 硬件 CERN-OHL-W 或 -S / 文档 CC-BY-4.0 | 半天（决策为主） | Asimov：136 页 0 次 "license"，CAD 可下载但法律上不可衍生 |
| 修 `simulation/asset/duke_v2/**/README.md` 里的 6 条死链，并加导出期 link checker | 半天 | Berkeley：解耦文档导致 7 条命令里 4 条失效（2 条路径写错 + 2 条文件不存在）+ 一处 "press XXXX" 占位符 |
| 修 checkpoints README 的文件表（列 5 个、实际 3 个，缺的是两个 cosine ckpt），并纳入导出校验 | 2 小时 | 同上 |
| 把漏计的三行（`CNC_arm13` $109.80 / `CNC_arm11` $239.58 / `B6` $101.38）并回 `TOTAL CNC`，剔除 `B6` 测试夹具，并把"发布口径 = 全 63 行剔 B6 = $6,739.24 / 整机 $15,231.37"写死在表里 | 2 小时 | 这是 4.1 的核心结论，且是全表里最便宜的一处修正；不做则任何对外数字都是错的 |
| BOM 迁移第 1–5 步（拆 CNC、清历史残留、换算单价、补紧固件、给材料定价） | 1 周 | OpenArm 1.0 的 7 页 BOM；ToddlerBot 的 100 行 CSV |
| 把 BOM 以 CSV 形式放进仓库 `hardware/bom/` | 1 天（迁移完成后） | Berkeley：Google Sheet 不能 diff / pin / license / 归档，是它被点名的最大弱点 |
| 发 STEP（制造件）+ STL/3MF（打印件），挂在打了 tag 的 GitHub Release 上 | 3 天 | Berkeley：`releases.json` 的 `"assets": []` 是它自己 workflow 已解决却没用的问题 |
| 写 `docs/safety.md`：6S 锂电、E-stop 与断电顺序、首次上电吊装、旁观者距离、失电塌落 | 1 天 | OpenArm `md/overview/safety-guide.md`；V2 自己说 "36 kg humanoid with people beside it" |
| 加 `.github/`：3 个 issue 模板 + PR 模板 + CONTRIBUTING + CODE_OF_CONDUCT + 跑 635 测试的 CI | 1 天 | OpenArm 全套；ToddlerBot 的硬件感知 `bug_report.yml` |
| 三个 repo 打第一个 tag（`v1.0.0` / 硬件修订 `humanoid_v21`）+ CHANGELOG | 半天 | 现状是无 tag 无 release，没人能 pin |
| README 的 `LICENSES` 段里补一句 V1(MIT) → V2(Apache-2.0) 的换证说明 | 半小时 | `duke-humanoid-v1/repo/LICENSE` 是 MIT，代际之间换了证却没有任何迁移说明，下游会以为 V1 的条款还适用 |
| 给 `simulation/asset/unitree_g1/` 补 license 说明（或改掉 README 里 "Each keeps its upstream `LICENSE` beside its meshes" 这句话，因为对 G1 不成立） | 1 小时 | OpenArm 逐 repo 标注 license；G1 是论文头号 baseline |
| 改掉项目页的两处开源承诺，或在发布同时兑现：`vrw-anonymous/docs/index.html` 同时有 "We will open source our entire software and humanoid hardware design" 和 "will be open sourced on acceptance"；`project-page/md/index.md` 与 `project-page/_html/index.html` 只有后者。三处措辞要统一，且措辞必须与实际发出的东西一致 | 1 小时 | 承诺与交付不一致本身就是信誉成本 |

### 5.2 发布时最好有

| 项 | 工作量 | 哪个对标证明它值得做 |
|---|---|---|
| 分子装配的装配文档（leg/arm/torso/head-camera/gripper），每步一张高亮渲染 | 3–4 周 | OpenArm 10 页 71 步 83 图；Asimov 83 页 |
| 每步页顶部 "Parts needed" 表 + 分格清点协议 | 与上同步，+3 天 | Asimov 78/83 页；ToddlerBot 的"剩件即漏步"验收 |
| 紧固件规格表 + **扭矩值** + 螺纹胶牌号 | 1 周（含实测） | 四个对标全部缺扭矩，这是 V2 可以直接超过所有人的一项 |
| 线束文档：连接器针脚、线规、走线照片、六条 CAN 总线拓扑 | 1 周 | OpenArm 5 页 66 图的 wiring-and-casing-guide |
| 打印参数写成文字数字 + 附 3mf | 2 天 | Berkeley 的 13 张截图是明确反例 |
| 63 个 CNC 件补 material / tolerance / finish / supplier | 3 天 | OpenArm 每个机加工行都带这些 |
| 文档站（MkDocs Material，`mkdocs.yml` 在 umbrella repo 根、`docs/` 在仓库内，CI 跑 `mkdocs build --strict` 即 link check） | 1 周 | ToddlerBot 的 `docs/` 在 repo 内、每次 push 发布；Berkeley 解耦导致 4 条命令失效没人发现 |
| `llms.txt` + `llms-full.txt` | 2 小时 | Asimov 两个都发；Berkeley 3.4 KB 覆盖 27 页 |
| 装配工时估计 | 1 小时（有第一次完整装配记录即可） | Berkeley 论文的 "about three days" |
| BOM 替代料列（至少 D436 和 Robstride） | 2 天 | ToddlerBot 的 Alternative Link 列；OpenArm 缺这项是它的已知弱点 |
| deploy 侧的观测/动作契约页（31 DoF 关节向量布局、50 Hz / 200 Hz） | 1 天 | OpenArm `md/tutorial/inference.md` 的 Policy Server Contract |
| 项目页与 repo 双向互链（匿名期结束后） | 1 小时 | 现在项目页没有任何代码链接 |

### 5.3 发布后逐步补

| 项 | 工作量 | 哪个对标证明它值得做 |
|---|---|---|
| 机械侧事故登记：把 "three sessions died to this" 升格为 INC 编号条目并配图 | 持续 | V2 自己的 `auto_operator_incidents.md` 已证明这个模式有效 |
| "Tips and Tricks" 页，作为现场故障的滚动日志 | 持续 | ToddlerBot `docs-site/md/sections/05_tips_and_tricks.md` |
| 跨实例复现实验：照公开文档建第二台 + 策略 zero-shot 迁移 + 双机任务 | 1–2 月 | ToddlerBot 的 `hug_transfer.mp4` / `collaborate.mp4` |
| CNC 件跨加工商一致性实验（两家各做一套关键件，比较装配后背隙） | 2 周 | Berkeley 的两台打印机 × 6 个执行器实验 |
| 供应商/套件页，带质量分级与真实价格 | 持续 | OpenArm `md/purchase.md` 的 10 家厂商四级分级 |
| 每子装配一段短视频，绑定在对应手册章节旁 | 2 周 | ToddlerBot 的 14 视频 ↔ 14 章节 |
| 交互式 3D 装配（Origami 式通道机制） | 1–2 月 | Asimov：`project.json` 431 个指令态、步骤页里 430 条深链，整机 12 MB |
| CI 里从 GitHub API 生成"可认领 issue"排行榜 | 2 天 | OpenArm `repo/website/scripts/fetch-popular-issues.sh` + `src/components/GitHubIssues.tsx` |
| 硬件修订版本化文档（`/v2.1/`、`/v2.2/`） | 修订发生时 | OpenArm 的 Docusaurus 版本化——但**不要**抄它的 `removedInV2` 静默重定向 |

---

## 6. 可以直接抄的东西

每条都给出本地路径，可以直接打开看。

**BOM 与采购**

1. **按子装配 × 制造类别双切分的 BOM 页**——
   `reference/openarm/md/1.0/hardware/bill-of-materials/`（7 个页面，
   `arm-manufactured.md` 与 `arm-off-the-shelf.md` 并列即可看出切法）。
2. **让小计不可能漂移的实现**——
   `reference/openarm/repo/website/src/components/BoMTable.tsx` 与 `MechanicalComponentsTable.tsx`，
   计价工具在 `repo/website/src/utils/priceUtils.ts`；`.mdx` 页本身只有 4 行。
3. **多配置并列的单表 BOM + 升级差价行**——
   `reference/bom/toddlerbot_BOM_release.csv`（第 15 行的 `$ of 2XC+ = $1,565.62`，
   第 56/80/101 行的三档小计 $5,727.94 / $1,976.13 / $2,252.73）。
4. **整机售卖行 + 永久免责声明行**——同一文件第 2–3 行
   （WowRobo $4,299，紧跟一行 `Disclaimer` 类型："We are not affiliated with or endorse this company"）。
5. **把加工商料号写进 BOM**——
   `reference/openarm/md/1.0/hardware/bill-of-materials/procuring-components.md` 的 Method 2
   （粘贴 MEVIY 型号下单，"ensures you get the exact geometry we've validated"）。
6. **常缺货件的精确替代号**——
   `reference/toddlerbot/docs-site/md/hardware/02_pcb8ch.md`（JST EH plug → C160259 等）。

**装配与制造**

7. **83 页分模块步骤 + 子装配合并步的目录结构**——
   `reference/asimov/md/asimov/1/assembly-steps/`。
8. **每步页自带的 "Parts needed" 表**（含 "Threadlocker | As needed"）——同上任一 step 页。
9. **带产品照片、明确标注"非联盟链接"、标注哪些随套件发货的工具清单**——
   `reference/asimov/md/asimov/1/assembly-preparations/assembly-tools.md`（10,448 B，13 件必需 + 10 件可选，两段各自是一个 `## ` 标题下的 `### ` 列表）。
10. **六条菊花链的线序与预穿线规则**——
    `reference/asimov/md/asimov/1/assembly-preparations/electrical-preparation.md`。
11. **撤回未验证流程并说明原因**——
    `reference/asimov/md/asimov/1/assembly-verifications.md`
    （"Do not use earlier drafts to approve power-on…"），比留一份错的检查表更安全。
12. **固件前置条件门控硬件步骤**——
    `reference/openarm/md/1.0/hardware/assembly-guide/j1-j2-sub-assembly.md` 开头的阻塞式 WARNING。
13. **5 页 66 图的布线与外壳指南**——
    `reference/openarm/md/1.0/hardware/wiring-and-casing-guide/`；
    其中 `components.md` 还记录了对供应商缺陷的 13 步自制修复（3D 打印模具热弯连接器）。
14. **三段式子装配套件清单 + 剩件验收协议**——
    `reference/toddlerbot/repo/docs/_static/assembly_manual.pdf` 第 1 页与第 2 页。
15. **JLCPCB 逐屏下单流程（Gerber + BOM CSV + CPL）**——
    `reference/toddlerbot/docs-site/md/hardware/02_pcb8ch.md`（10 张截图）；
    OpenArm 的等价物在 `reference/openarm/repo/website/static/file/hardware/bill-of-materials/electrical/`。
16. **带期望现象和补救动作的 bring-up 检查点**——
    `reference/berkeley-humanoid-lite/docs-site/md/getting-started-with-hardware/flashing-the-motor-controllers.md`
    （LED ~1 Hz 闪、`ping.py` 打印 "Motor is online"、校准时拉 ~1 A 并先逆时针转一整圈，
    若方向相反则交换两相或设 `MOTOR_PHASE_ORDER = -1`）。

**CAD 与发布机制**

17. **在 tag 上打包上传 assets 的 57 行 workflow**——
    `reference/berkeley-humanoid-lite/repo/source/berkeley_humanoid_lite_assets/.github/workflows/release.yml`
    （对照 `reference/berkeley-humanoid-lite/releases.json` 里的 `"assets": []` 看这个模式为什么没用上）。
18. **内容寻址 + 通道指针的 3D 手册发布机制**——
    `reference/asimov/_html/_external/static.asimov.inc/manual/v1/origami/`
    （`index.html` 读 `channels/stable.json` 里的 `releaseId` 并跳转到
    `./releases/<sha256>/index.html`；整机 1162 个实例的动画手册 12 MB，
    旁边同一台机器的单个 eDrawings 静态快照是 124 MB）。
19. **打印参数的反面教材**——
    `reference/berkeley-humanoid-lite/docs-site/md/getting-started-with-hardware/3d-printing-instructions.md`
    （13 张截图，文字里零个数字）。
20. **手写的带日期变更日志，诚实记录几何错误**——
    `reference/berkeley-humanoid-lite/docs-site/md/releases.md`
    （"replacing the wrong 5010-5010 housing part and add the missing limit stopper part"）。

**文档站与机器可读**

21. **`llms.txt` + `llms-full.txt` 双发**——
    `reference/asimov/llms.txt`（28 KB 注释导航）与 `reference/asimov/llms-full.txt`（599,878 B 全语料）；
    轻量版看 `reference/berkeley-humanoid-lite/docs-site/_html/llms.txt`（3.4 KB / 27 页）。
22. **docs 在 repo 内 + CI 每次 push 构建**——
    `reference/toddlerbot/repo/docs/` 与 `repo/.github/workflows/deploy_page.yml`。
23. **从数据文件自动生成画廊**——
    `reference/toddlerbot/repo/docs/` 里的 `motion_gallery_ext.py`
    （构建时扫描 `motion/*.lz4`，读关键帧数和时长，生成 `motions.json`），
    保证画廊永远不会与仓库脱节。
24. **硬件修订的版本化与迁移页**——
    `reference/openarm/repo/website/docusaurus.config.ts`（`removedInV2` 数组 + `createRedirects()`）
    与 `reference/openarm/md/overview/whats-new-in-2.0.md`。
    **抄版本化和迁移页，不要抄静默重定向**——它让拿着 2.0 硬件的人读到 1.0 的完整制造文档而不被告知。

**License 与社区**

25. **repo 表里逐行标注 license，并在"下载 CAD"那一页再声明一次**——
    `reference/openarm/repo/README.md` 的 9-repo 表（8 Apache-2.0 + 1 CERN-OHL-S-2.0）+
    `reference/openarm/md/1.0/hardware/assembly-guide/find-cad-files.md` 的 "📌 Licensing" 段。
26. **硬件与代码分家的完整文本**——
    `reference/berkeley-humanoid-lite/repo/source/berkeley_humanoid_lite_assets/LICENCE`（CC BY-SA 4.0 全文）
    与 `repo/LICENCE`（MIT）。注意它的三个坑：assets 的 `pyproject.toml` 写着 `license = "MIT"`
    与旁边的 LICENCE 矛盾；lowlevel 子模块完全没有 license 文件；文件名拼 `LICENCE` 而 README 链 `LICENSE`。
27. **硬件感知的 issue 模板 + 单方面支持契约**——
    `reference/toddlerbot/repo/.github/ISSUE_TEMPLATE/bug_report.yml`（必填 OS 下拉含 Jetson / ROG Ally X）
    与 `reference/toddlerbot/repo/README.md` 的 "Submitting an Issue" 段。
28. **完整社区基建**——
    `reference/openarm/repo/CODE_OF_CONDUCT.md`、`repo/CONTRIBUTING.md`、
    `repo/.github/ISSUE_TEMPLATE/`、`md/overview/contribute.md`（"GitHub Issues = our idea pool"，
    未指派 issue 可自行认领），以及 `repo/.github/workflows/preview-comment.yaml`（PR 自动评论预览 URL）。
29. **围绕本设计特有危险来写安全指南**——
    `reference/openarm/md/overview/safety-guide.md`
    （点名可反驱关节在 E-stop 断电瞬间会让负载坠落，并附 4 项定期检查表）。

**可复现性**

30. **把可复现性写成论文 Results 的可证伪实验**——
    `reference/toddlerbot/project-page/md/index.md` 的 "Reproducibility: Hardware and Policies" 小节
    （跨实例策略迁移 / 双机协作 / 1000× 建造延时）。
31. **跨打印机一致性实验与 60 小时耐久协议**——
    `reference/berkeley-humanoid-lite/project-page/_html/static/paper/demonstrating-berkeley-humanoid-lite.pdf`
    （§D "Consistency Across Units"：6 个执行器 × 2 台打印机，比效率与力矩跟踪误差；
    背隙 0.0229 rad / std 0.0042 rad 出自 §B 另一组 6 个新打印执行器，别把两个实验说成一个）。
32. **把不好看的数字和好看的数字并排发**——
    `reference/toddlerbot/project-page/md/index.md`（19 分钟过热、7 次摔倒、21 min 打印 + 14 min 装配修复、
    侧手翻失败合集），这是让正面复现结论可信的原因。
33. **把 release note 写成社区报告**——
    `reference/berkeley-humanoid-lite/releases.json` 的 v1.1.0 条目
    （点名 12 位外部建造者，嵌入社区拼图与 3 个社区视频，并诚实预告 V2 及其原因）。
34. **发布带质量分级的供应商页**——
    `reference/openarm/md/purchase.md`（10 家厂商，Official Partner / Certified ★★★ / Evaluating / Not evaluated，
    真实价格与交期，并点名一个不兼容的仿制品）。

**V2 自己已经做对、不要在补硬件时弄丢的东西**

35. **编号安全机制 + 事故登记**——
    `reference/duke-humanoid-v2/repo/deploy/control/docs/auto_operator_safety_contract.md`（261 条）
    与 `auto_operator_incidents.md`（10 条，每条附"哪个简化会把它带回来"）。
    **把这个模式原样套到机械侧**——在本次抓取的四个镜像里 grep 不到等价物
    （这是对镜像的判断，不是对这四个项目全部资产的判断）。
36. **公开记录失败的 sweep 与被否决的晋升**——
    `simulation/mj_envs/tasks/visual_manipulation/test/checkpoints/README.md`
    （dyn8 的两主机字节不一致、dyn11 的 P_g1 0.092 vs 0.989）。
37. **诚实的再生成成本表**——
    `reference/duke-humanoid-v2/repo/README.md` 的 "Where each paper artifact lives"
    （含 "not reproducible offline, needs the robot"）。
38. **submodule 指针滞后即拒推的 pre-push 钩子**——
    `reference/duke-humanoid-v2/repo/.githooks/pre-push`。
39. **第三方 license 污染的点名与一句话移除指令**——
    `reference/duke-humanoid-v2/repo/README.md` 致谢表下方关于 Fourier GR-3 GPL-3.0 的加粗段。
40. **不要重蹈 V1 的覆辙**——
    `reference/duke-humanoid-v1/repo/README.md` 把硬件文档全放在外部 Notion 页，
    未版本化、在仓库之外，今天已私有且无法归档。V2 的硬件文档必须进仓库。

---

*本文基于 2026-09-17 的 `reference/duke-humanoid-v2/repo/` 浅克隆状态
（umbrella `a1dfdbb` / simulation `a55f704` / deploy `e2ac59b`，0 个 tag，history 深度 1）
与 `reference/bom/duke-humanoid-v2_BOM_sheet{1,2}*.csv`。
所有算术核对在第 4.1 节列出，可重算。*

*本稿经过一次对抗性复核：文中引用的每条本地路径都用 `test -e` 逐条验过，
两张 BOM 的全部求和都用脚本重算过，对标项目的页数、行数、字节数、价格与型号都回到镜像里核对过。
复核中改掉的是事实错误，不是措辞。*

**两处没有本地证据、已从正文删除或改写的说法，记在这里以免被重新写回：**

1. "Asimov 68 页点名 LOCTITE 222"——83 个步骤页里 `grep -ri loctite` 返回 0 行，
   牌号只出现在 `assembly-preparations/assembly-tools.md` 一页。
2. 上一稿曾把 OpenArm 1.0 的整机合计"更正"为 `¥587,586`，**那次更正本身是错的，不要再写回去**。
   `¥587,586` = 机械 478,518 + 电气 84,564 + leader end-effector 24,504，
   既漏掉了最大的一块执行器（¥397,356），又混进了不属于手臂的遥操作主手。
   正确的数是 `¥960,438` = 397,356 + 478,518 + 84,564，即 `<BoMSummary />` 打印的三个
   `*TotalCost()` 之和；三个分量都能用 `src/components/*Table.tsx` 里的
   `unitPrice × quantity` 重算复核（执行器表的 `cost` 字段本身就是行总价，
   代码注释里专门写明了这一点——这正是 V2 的 `UNIT COST` 列该学的做法）。

**以下说法本次无法证伪，引用时请自行加限定：**

- "Asimov 固件不公开 / 训练代码 0 链接"、"OpenArm 在 HF 上有 ACT 权重"——
  这些是关于**镜像之外**的上游仓库的判断，本地快照里既没有也证不了它们不存在。
（Berkeley 的 "仓库 HEAD 本身就是外部贡献（PR #50）" 曾被列为无法核对，其实可以核对：
浅克隆虽只有深度 1，但那一条 commit message 就在本地——
`git -C reference/berkeley-humanoid-lite/repo log -1 --oneline` 输出
`984741a Merge pull request #50 from Chenpeel/fix/isaacsim5-training`。贡献者是 `Chenpeel`，
分支名 `fix/isaacsim5-training` 也印证了"Isaac Sim 5 迁移"。此条现已有本地证据。）
