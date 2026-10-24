<div align="center">
  <h1>Yoho Standard README</h1>
  <p><strong>清晰的介绍，用心的设计，中英双语。</strong></p>
  <p><a href="README.md">English</a> · 简体中文</p>
  <p>
    <a href="#快速开始">快速开始</a> ·
    <a href="#设计选择">选择风格</a> ·
    <a href="#辅助工具">辅助工具</a>
  </p>
  <p><img src="docs/assets/readme/cover-zh-CN.svg" alt="概念插图：文档设计方案与中英文两个版本" width="880"></p>
</div>

一个用于 Codex 的技能，帮助开发者把仓库介绍写得更易理解、更方便上手。它先调查项目，再请你选择视觉方向，随后完成内容对应的英文与简体中文 README。

- **先确认事实。** 功能、命令和视觉素材均以目标仓库为依据。
- **由你选择风格。** 从五类风格中直接选择、让技能代为推荐，或要求三份视觉预览进行比较。
- **交付完整双语。** 完成 `README.md` 和 `README.zh-CN.md`，保持事实、示例与限制对应。

## 快速开始

### 1. 安装技能

使用支持本地技能的 Codex，选择以下任一方式安装。

**方式 A · 通过 `npx` 安装**

需要 Node.js 22.20 或更高版本、带有 `npx` 的 npm，以及 Git。在需要使用该技能的项目目录中运行：

```sh
npx skills add Yohoia/yoho-standard-readme --agent codex
```

默认仅安装到当前项目；添加 `--global` 可让该技能在不同项目中使用。更多安装选项与 Agent 支持情况见 [Skills CLI 文档（英文）](https://skills.sh/docs/cli)。

**方式 B · 将 GitHub 链接交给 Agent 安装**

向能够访问 GitHub 并安装本地技能的 Agent 发送仓库链接和安装请求：

```text
Install the yoho-standard-readme skill for Codex from:
https://github.com/Yohoia/yoho-standard-readme
The skill is at the repository root. Keep SKILL.md, agents/, references/,
and scripts/ together in the installed skill directory.
```

### 2. 在目标项目中使用

Codex 加载该技能后，打开要编写文档的仓库，发送：

```text
Use $yoho-standard-readme to redesign this project's README.
Inspect the project, then ask me to choose a visual style before editing.
Show three visual previews only if I ask to compare styles.
Complete README.md and README.zh-CN.md after the choice.
```

技能先检查项目与可用素材，再询问风格选择。你选定后，它会完成两份 README、补充必要资料，并验证结果。两版文档在顶部附近互相链接，命令保持可复制，技术内容保持对应。

## 设计选择

### 五类风格

这些是视觉方向，不是固定页面模板。技能会结合项目读者和首次使用任务，调整构图与章节顺序。

| 风格 | 首屏重点 |
| --- | --- |
| **居中品牌 Hero** | 文字标题或已有 Logo、标语、有效入口与简短介绍 |
| **工程速览** | 真实命令或 API 调用，以及预期结果 |
| **产品演示** | 产品总览主图，以及展示真实任务或功能的少量截图 |
| **品牌叙事** | 克制的封面、项目解决的问题与实现思路 |
| **流程导览** | 易读的流程图或架构图，以及首次使用路径 |

可以直接选一种风格，也可以让技能代为推荐。需要比较时，要求制作三份首屏预览；它们会采用不同的构图、叙事重点和章节安排。选择前不会改动现有 README。居中品牌 Hero 的开场之后，正文与代码恢复左对齐。

### 素材与徽章

技能复用经过确认的项目 Logo；没有 Logo 时，只显示项目名称文字。图解与生成插图围绕项目实际内容制作，概念插图会明确标注，不用于替代真实界面或性能证据。

产品演示包含专门的截图流程：选择一张主图和少量展示不同功能或任务的截图，复用已核实的素材或运行产品后截取，并搭配简短说明。其他风格也可按需在正文中加入截图展示。数量由实际内容与证据决定；没有真实界面或可视化输出的项目优先采用其他合适方向。产品截图与 README 排版预览分别验证。

如果有可用的徽章工具，技能会自动加入经过确认的主要技术栈徽章。动态状态徽章取决于是否有实用且持续维护的数据源；提供方直接调用方式集中在徽章目录中，呈现方式遵循所选视觉风格。

本仓库封面为概念插图，没有独立 Logo，也没有 CI、覆盖率、发布或许可徽章数据源。

构图、徽章工具与验证规则见[风格与素材说明（英文）](references/visuals.md)。

### 统一的内容骨架

最终 README 覆盖**项目标识、项目介绍、主要功能、快速开始、实际用法、文档与限制、许可状态**。可以合并章节或调整顺序，但安装、前置条件、必要配置与首次成功运行的结果都应便于查找。

[内容指南（英文）](references/content.md)说明了如何将骨架用于库、CLI、应用、服务、技能和研究项目。保留已有翻译、法律声明、署名与有效文档；仅在对读者有帮助时增加深入资料。

## 工作流程

1. **调查。** 阅读目标项目的指令、源码、配置、示例、文档与素材，记录哪些陈述经过执行、获得源码支持，哪些仍未确认。
2. **选择。** 修改正式文件前，通过已有选择、直接指定或委托推荐确定视觉方向。用户要求比较时，提供三份首屏预览。
3. **写作。** 完成英文与中文版，保持事实、前置条件、命令、参数与限制对应，正式发布的素材只采用选定方向。
4. **验证。** 检查结构、实际用法、双语对应，以及桌面和手机在亮暗主题下的呈现，列明已完成的检查与具体缺口。

渲染和图像生成是可选能力。无法渲染用户要求的预览时，技能提供可检查的 Markdown，并标注“未渲染”。已有素材、简单 SVG 或 Markdown 都可用于实现选定设计。

## 辅助工具

技能指令协调改写流程，脚本辅助检查；它们不是独立的 README 生成程序。

### 结构审计

需要 **Python 3**，仅使用标准库。在本技能的本地仓库中运行：

```sh
python3 scripts/audit_readme.py --repo /path/to/project
```

默认检查 `README.md` 和 `README.zh-CN.md`。检查单份文档或首屏候选时：

```sh
python3 scripts/audit_readme.py \
  --repo /path/to/project --single path/to/document.md
```

JSON 报告覆盖本地链接与锚点、语言互链、图片说明、部分不兼容 HTML、存在风险的 SVG 依赖，以及可执行示例的差异。退出码 `0`：没有结构错误；`1`：存在结构错误；`2`：参数或读取失败。警告仍需单独复核。审计器不会执行示例、检查远程 URL、确认事实或判断翻译质量。

### 本地视觉预览

需要 **Node.js、`marked`、`sanitize-html`、Playwright 和可用的 Chromium 浏览器**。使用已有工具，或将额外依赖安装到独立工具目录；仓库未提供用于安装这些依赖的包清单。

```sh
node scripts/preview_readme.mjs \
  --repo /path/to/project \
  --out /path/to/project/.scratch/readme-review \
  --module-root /path/to/tooling/node_modules \
  --browser /path/to/chromium \
  README.md README.zh-CN.md
```

多个依赖目录可重复传入 `--module-root`。环境已能解析依赖或 Playwright 浏览器时，省略对应的 `--module-root` 或 `--browser`。默认每份文档生成四张首屏 PNG：900px 桌面与 360px 手机，各含亮色、暗色，并共享一份 `index.html` 与 `report.json`。添加 `--full-page` 可生成四种视图的完整页面截图；使用独立输出目录保留两种模式的产物。

退出码 `0`：可以进入视觉审阅；`1`：发现缺图、页面溢出或空内容；`2`：运行失败。远程图片被阻止加载并列为未验证，Mermaid 不会被渲染。截图近似 GitHub 的 GFM 呈现，仍需查看实际图片及首屏后的正文。

完整命令与检查边界见[验证指南（英文）](references/validation.md)。

## 文档导览

| 路径 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 主流程与必要决策关口 |
| [agents/openai.yaml](agents/openai.yaml) | Codex 界面元数据与默认提示词 |
| [references/content.md](references/content.md) | 内容骨架、证据与双语决策 |
| [references/visuals.md](references/visuals.md) | 风格选择、预览、素材与徽章规则 |
| [references/badges.md](references/badges.md) | Shields、Badgen、GitHub Actions 与动态 SVG 的直接调用配方 |
| [references/validation.md](references/validation.md) | 辅助工具用法与验收边界 |
| [docs/verification.md](docs/verification.md) | 已记录的测试与隔离流程试用 |
| [scripts/package_skill.py](scripts/package_skill.py) | 构建并验证自包含的技能运行包 |
| [tests/test_audit_readme.py](tests/test_audit_readme.py) | 审计器 CLI 回归测试 |
| [tests/test_preview_readme.mjs](tests/test_preview_readme.mjs) | 预览 CLI 与可选 Chromium 集成测试 |
| [tests/test_package_skill.py](tests/test_package_skill.py) | 运行包 CLI 与引用完整性测试 |

以上参考资料与验证记录均为英文。

### 验证与开发

从本仓库构建经过验证的运行包：

```sh
python3 scripts/package_skill.py
```

命令会创建唯一的系统临时目录，报告版本、输出路径、源文件哈希与包内文档审计结果。它会核对 `SKILL.md` 与 `agents/openai.yaml` 中的语义化版本是否一致，不一致时拒绝打包。可以用 `--out /existing/parent/new-package` 指定新的或空的输出目录。发布运行包前会核对复制内容与本地引用，已有非空目录会保留。运行文件清单集中维护在打包脚本中；测试、scratch 产物与仅供开发使用的文档留在源码仓库。

在仓库根目录执行审计器与预览 CLI 测试，以及预览工具语法检查：

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_preview_readme.mjs
node --check scripts/preview_readme.mjs
```

预览测试默认跳过 Chromium 用例；通过 `YOHO_PREVIEW_MODULE_ROOTS` 指定已有渲染依赖目录后运行，需要浏览器路径时再设置 `YOHO_PREVIEW_BROWSER`。[验证记录（英文）](docs/verification.md)包含完整测试命令、审计器 CLI 覆盖范围，以及覆盖 CLI、带翻译迁移的库、渲染不可用、文档与素材缺陷修复的隔离试用。修改技能决策时，还应在隔离目标项目中试用并检查实际产物；辅助工具测试不覆盖完整 README 改写流程。

记录中的工具包括 Python 3.12.10、Marked 17.0.5、sanitize-html 2.18.1、Playwright 1.62.1 和已安装的 Chromium 浏览器。辅助脚本未声明最低 Python/Node 版本支持策略，这些检查不能证明适用于所有项目或环境。

本地预览不验证 GitHub 线上渲染、Camo 代理或 Mermaid 运行时。图像生成、远程图片与 URL 检查，以及新 Codex 会话中的技能发现，不属于已有验收通过项。

## 致谢

内容骨架参考了 [Best-README-Template](https://github.com/othneildrew/Best-README-Template)。[awesome-readme](https://github.com/matiassingers/awesome-readme)提供更多呈现案例与工具。参考资料用于结构与设计，项目陈述以目标仓库为依据。

## 许可

本仓库目前没有许可证文件或许可声明。本 README 不赋予任何许可。
