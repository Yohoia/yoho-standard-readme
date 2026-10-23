# Yoho-Standard-README

[English](README.md) · 简体中文

![概念插图：文档设计方案与中英文两个版本](docs/assets/readme/cover-zh-CN.svg)

**让你的仓库，有一份值得阅读的项目介绍。**

一个用于 Codex 的技能，将真实的项目内容、经过设计的视觉呈现，以及技术内容对应的中英双语 README 结合起来。它会先调查仓库和现有素材，再请你选择视觉方向，随后完成文档。

[快速开始](#快速开始) · [工作流程](#工作流程) · [辅助工具](#辅助工具) · [验证记录](#验证记录)

## 先选视觉方向

检查仓库和现有素材后，选择一种 README 风格。如果你还没想好或希望比较布局，可以要求制作三份真实首屏预览，每份采用不同的构图、叙事重点和章节安排。选定方向后，技能会完成英文 `README.md`、简体中文 `README.zh-CN.md`，以及必要的支持资料。

选择期间，已有 README 会保留。你选定后，技能直接继续写作和验证。两版文档的事实、前提、命令、参数和限制保持对应，文字表达分别符合各自语言习惯。

### 五类风格参考

可以直接选择一种风格。技能会结合项目说明合适的方向；需要比较时，再要求制作三份预览。

| 风格 | 首屏重点 |
| --- | --- |
| **居中品牌 Hero** | 已有 Logo（可选）→ 标题 → Slogan → 有依据的徽章/标签 → 有用的入口链接 → 简介或真实演示 |
| 工程速览 | 明确任务、可复制的命令或 API 调用，以及预期输出 |
| 产品演示 | 真实界面或输出截图，以及用户操作流程 |
| 品牌叙事 | 克制的封面、项目解决的问题与实现思路 |
| 流程导览 | 易读的流程图或架构图，以及首次使用路径 |

简介可以根据项目内容放在徽章之前。居中品牌 Hero 之后的技术正文恢复左对齐，方便阅读。仓库没有 Logo 时，Hero 只显示项目名称文字。额外的 SVG 图解或生成插图应根据项目实际内容制作。

### 徽章工具与呈现方式

可按数据源选择 Shields.io（`flat`、`flat-square` 或 `for-the-badge`）、Badgen（classic 或 flat），或 GitHub Actions 原生工作流徽章。可以比较同一条真实内容的样例，让技能推荐适合当前风格的呈现方式，也可以不使用徽章。描述性标签来自项目事实，变化中的状态来自实时数据源。详见[风格与素材规则（英文）](references/visuals.md)中的工具选择与验证要求。

## 按项目组织内容

阅读路径围绕开发者首先需要理解和尝试的任务展开。

| 项目类型 | 合适的开场 | 按需深入的内容 |
| --- | --- | --- |
| 库或 SDK | 一个公开 API 调用及其结果 | 安装、错误、兼容性、参考文档 |
| CLI | 一条真实命令及其输出 | 参数、配置、输入输出行为 |
| 应用 | 真实界面和用户任务 | 本地启动、环境、持久化、部署 |
| 服务 | 一次请求响应及其系统角色 | 依赖、配置、鉴权、限制 |
| 技能或开发工具 | 改善的任务与实际产物 | 安装、调用、流程、工具要求 |
| 研究或数据项目 | 研究问题与可复现的结果 | 数据访问、方法、假设、可复现性 |

### 统一的内容骨架

最终 README 覆盖七类核心信息：**Hero/项目标识、项目介绍、主要功能、快速开始、实际用法、文档与限制、许可状态**。可以按项目合并章节、调整顺序。快速开始包含前置条件、安装或访问方式、必要配置，以及首次成功运行的结果。

[可调整的内容模板（英文）](references/content.md)参考了 [Best-README-Template](https://github.com/othneildrew/Best-README-Template)。技术栈、路线图、贡献、支持渠道与致谢按事实添加；必要声明和署名始终保留。[awesome-readme](https://github.com/matiassingers/awesome-readme)用于查找更多呈现案例与工具。参考资料提供结构与设计灵感，项目陈述仍以目标仓库为依据。

保留已有翻译、法律声明、署名和有用文档；只有对读者有帮助时，才增加深入资料和视觉素材。

## 快速开始

### 1. 安装到 Codex

需要支持本地技能的 Codex，以及本仓库的本地副本。克隆仓库需要使用有访问权限的账号。

```sh
git clone https://github.com/Yohoia/yoho-standard-readme.git
cd yoho-standard-readme
```

在仓库根目录执行以下 POSIX shell 命令，将运行文件复制到个人技能目录；同样可用于更新已有安装：

```sh
readme_skill_dir="${CODEX_HOME:-$HOME/.codex}/skills/yoho-standard-readme"
mkdir -p "$readme_skill_dir/agents" "$readme_skill_dir/references" "$readme_skill_dir/scripts"
cp SKILL.md "$readme_skill_dir/SKILL.md"
cp agents/openai.yaml "$readme_skill_dir/agents/openai.yaml"
cp references/*.md "$readme_skill_dir/references/"
cp scripts/audit_readme.py scripts/preview_readme.mjs "$readme_skill_dir/scripts/"
```

默认安装到 `~/.codex/skills/yoho-standard-readme`；设置了 `CODEX_HOME` 时会使用对应位置。安装包含七个文件：技能入口、界面元数据、三份参考资料和两份脚本。没有 POSIX shell 时，也可以按相同目录结构手动复制这些文件。

### 2. 在目标项目中调用

Codex 加载该技能后，打开要编写文档的仓库，发送：

```text
Use $yoho-standard-readme to redesign this project's README.
Inspect the project, then ask me to choose a visual style before editing.
Show three visual previews only if I ask to compare styles.
Complete README.md and README.zh-CN.md after the choice.
```

技能先检查项目和素材，再询问风格选择。你可以直接选择一种、要求制作三份预览进行比较，或让技能推荐方向。只在缺少影响正确性的必要事实时补充询问。

## 工作流程

1. **调查事实与素材。** 阅读源码、配置、示例、已有文档及相关项目指令，并盘点 Logo、截图、图解和徽章数据源。保留区分实际执行、源码支持和未确认事项的证据记录。
2. **选择风格。** 修改 README 或正式素材前，让用户直接选一种风格、委托技能推荐，或要求比较三份预览。若制作预览，等用户选定后再写正式文档。只有徽章能展示有用且可验证的项目信息时，才询问徽章呈现方式。
3. **完成双语。** 写完整介绍、首次使用路径、限制和有效链接。使用已有 Logo；没有 Logo 时只显示项目名称，并按需制作符合项目内容的图解或插图。
4. **验证。** 检查结构、实际用法、双语对应关系、徽章数据来源和视觉呈现，并简洁列明已完成的检查与具体缺口。

渲染和图像生成是可选能力。用户要求预览而无法渲染时，仍提供可检查的 Markdown 方案，并明确标注“未渲染”。已有素材、简单 SVG 或 Markdown 都可以支撑最终设计。概念插图不会被用来证明真实界面、功能或性能。

## 项目中会得到什么

```text
your-project/
├── README.md                    English entry point
├── README.zh-CN.md              Simplified Chinese edition
├── docs/                       Existing or necessary deeper material
└── .scratch/readme-previews/    Candidate sources and review assets
```

上图是示意结构：技能沿用目标项目已有的 scratch、文档和素材约定。两份 README 在顶部附近互相链接。核心说明和命令保留为可复制的 Markdown；正式素材只采用选定方向。保留其他语言版本，并相应更新语言切换和受影响的文档引用。

## 辅助工具

技能指令协调改写流程，附带脚本负责具体检查；它们不是独立的 README 生成程序。

### 结构审计

使用 Python 3 标准库，无须安装 pip 包。在本技能的本地仓库中运行：

```sh
python3 scripts/audit_readme.py --repo /path/to/project
```

默认检查 `README.md` 和 `README.zh-CN.md`。检查单份文档或首屏候选时：

```sh
python3 scripts/audit_readme.py \
  --repo /path/to/project --single path/to/document.md
```

JSON 报告覆盖本地链接与锚点、语言互链、图片说明、部分不兼容 HTML、存在风险的 SVG 依赖，以及可执行示例的差异。退出码 `0` 表示没有结构错误，`1` 表示存在结构错误，`2` 表示参数或读取失败。警告仍需复核；退出码为 `0` 不能证明事实准确或翻译质量。

### 本地视觉预览

需要 Node.js、`marked`、`sanitize-html`、Playwright 和可用的 Chromium 浏览器。优先使用已有工具，额外依赖放在独立工具目录中。

```sh
node scripts/preview_readme.mjs \
  --repo /path/to/project \
  --out /path/to/project/.scratch/readme-review \
  --module-root /path/to/tooling/node_modules \
  --browser /path/to/chromium \
  README.md README.zh-CN.md
```

`--module-root` 可以重复传入。环境已能解析依赖或 Playwright 浏览器时，可以省略对应的 `--module-root` 或 `--browser`。每份输入生成四张首屏 PNG：900px 桌面和 360px 手机，各含亮色、暗色，并输出 `index.html` 与 `report.json`。

退出码 `0` 表示可以进入视觉审阅，`1` 表示发现缺图、页面溢出或空内容，`2` 表示运行失败。远程素材被阻止加载并列为未验证，Mermaid 不会被渲染。截图近似 GitHub 的 GFM 呈现，仍需实际查看图片及首屏后的正文。

完整检查边界见[辅助工具用法与验收说明（英文）](references/validation.md)。

## 验证记录

[验证记录（英文）](docs/verification.md)包含 26 项审计器 CLI 测试和有代表性的隔离流程试用：CLI、带翻译迁移的库、渲染不可用的环境，以及文档和素材缺陷修复。

这些检查记录已观察到的行为，不能证明适用于所有项目类型或运行环境。记录中的工具包括 Python 3.12.10、Marked 17.0.5、sanitize-html 2.18.1、Playwright 1.62.1 和已安装的 Chromium 浏览器；本项目未声明最低 Python/Node 版本支持策略。

本地预览不等于检查了 GitHub 线上渲染、Camo 代理或 Mermaid 运行时。图像生成、远程图片/链接检查，以及新 Codex 会话中的技能发现，不属于已有验收通过项。结构报告不能证明项目陈述、执行使用命令或判断双语文案质量。

## 仓库导览

| 路径 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 主流程与风格选择关口 |
| [agents/openai.yaml](agents/openai.yaml) | Codex 界面元数据与默认提示词 |
| [references/content.md](references/content.md) | 内容结构、证据与双语决策 |
| [references/visuals.md](references/visuals.md) | 风格差异、GitHub 兼容视觉与素材选择 |
| [references/validation.md](references/validation.md) | 辅助命令与验收边界 |
| [scripts/](scripts/) | 结构审计器与可选预览工具 |
| [tests/test_audit_readme.py](tests/test_audit_readme.py) | 审计器进程级回归测试 |

## 开发与许可

在仓库根目录执行审计器行为测试和预览工具语法检查：

```sh
python3 -m unittest discover -s tests -v
node --check scripts/preview_readme.mjs
```

修改技能决策时，还应在隔离目标项目中试用并检查实际产物。现有测试针对审计器，不是覆盖完整 README 改写的自动化回归套件。

本仓库目前没有许可证文件或许可声明。本 README 不赋予任何许可。
