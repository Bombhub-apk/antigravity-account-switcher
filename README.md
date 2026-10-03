# Antigravity Account Switcher & Project Migration Suite ⚡️

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11%20%7C%20macOS%20%7C%20Linux-brightgreen.svg)]()
[![Antigravity](https://img.shields.io/badge/Antigravity-2.0%2B-cyan.svg)]()
[![ChatGPT Desktop](https://img.shields.io/badge/ChatGPT%20Desktop-Codex%20Pro-00f0ff.svg)]()
[![UI Design](https://img.shields.io/badge/Design-iOS%20Liquid%20Glass-purple.svg)]()
[![Languages](https://img.shields.io/badge/Languages-EN%20%7C%20ES%20%7C%20FA%20%7C%20ZH-orange.svg)]()
[![Organization](https://img.shields.io/badge/Organization-mad--helpers-blueviolet.svg)](https://github.com/mad-helpers)

> **Super-fast 1-click Google Account Switcher, Concurrent Dual-Instance Runner, Real-Time Quota HUD, and AI Project & Chat Migration Suite for Google Antigravity & ChatGPT Desktop / Codex.**  
> Crafted with Apple iOS Liquid Glass aesthetics, fluid 60fps spring physics, and multi-language support (English, Spanish, Persian, Chinese).

<p align="center">
  <a href="assets/teaser.mp4">
    <img src="assets/teaser.gif" alt="Antigravity Account Switcher Launch Teaser" width="100%" style="border-radius: 16px; box-shadow: 0 16px 48px rgba(0,0,0,0.7), 0 0 40px rgba(0, 240, 255, 0.25);" />
  </a>
</p>
<p align="center">
  <em>⚡️ <b>Watch the Official Launch Teaser</b>: 1-Click Identity Swap, Concurrent Dual IDE Instances & Scheduled Task Isolation. (<a href="assets/teaser.mp4">HD Video with Sound</a>)</em>
</p>


---

## 🌟 Quick Navigation / Navegación Rápida

- [English (🇬🇧 Overview & Features)](#-english)
- [ChatGPT Desktop & Codex Suite (🤖 UI & Auth Center)](#-chatgpt-desktop--openai-codex-suite)
- [Español (🇪🇸 Descripción y Características)](#-español)
- [فارسی (🇮🇷 مستندات جامع فارسی)](README_FA.md)
- [简体中文 (🇨🇳 概述与使用指南)](#-简体中文)
- [Installation & Quick Start](#-installation)
- [CLI Reference](#-cli-commands)
- [Architecture & Mechanics](#-architecture--how-it-works)

---

## 🚀 Installation

### 🪟 Windows 10 & 11 (PowerShell)
Open PowerShell as your standard user and run:
```powershell
irm https://raw.githubusercontent.com/mad-helpers/antigravity-account-switcher/master/install.ps1 | iex
```
*Creates `Antigravity Switcher` shortcuts on your Desktop & Start Menu, installs background sync daemons, and registers `agy-switch` in your PATH.*

### 🍏 macOS (Apple Silicon M1/M2/M3/M4 & Intel)
Open Terminal and run:
```bash
curl -fsSL https://raw.githubusercontent.com/mad-helpers/antigravity-account-switcher/master/install.sh | bash
```
*Builds and installs `AntigravitySwitcher.app` in `/Applications` and `~/Desktop`, and links `agy-switch` into your PATH.*

---

## 🇬🇧 English

### Overview
Switching between multiple Google accounts on **Google Antigravity** can be tedious and disruptive because session credentials are bound inside **Windows Credential Manager** (`service: "gemini"`, `account: "antigravity"`) or **macOS Keychain**.

**Antigravity Account Switcher & Migration Suite** by **[mad-helpers](https://github.com/mad-helpers)** (co-owned by **[Madgod-xyz](https://github.com/Madgod-xyz)** & **[Bombhub-apk](https://github.com/Bombhub-apk)**) is a high-performance native cross-platform solution (GUI, in-editor HUD pill, and CLI). It allows you to swap identities in under 3 seconds **or** run two completely isolated Antigravity instances side-by-side on the same machine with independent credentials, tasks, and project access.

### ✨ Key Features

1. ⚡️ **Dual-Instance Concurrent Multi-Window**:
   - Open a 2nd Antigravity window with a secondary Google account (`--user-data-dir="%APPDATA%\Antigravity-Instance2"`).
   - Work simultaneously on different projects or split workflows between personal and corporate accounts without logging out.
   - Separate DevTools debugging ports and state isolation.

2. 🔄 **Seamless In-Place Single-Window Switching**:
   - Swap identities in under 3 seconds directly within your active window.
   - Preserves active workspace paths and reloads credentials smoothly.

3. ⏱ **Scheduled Tasks & Cron Isolation**:
   - Tasks and scheduled automations created in Account 1 are isolated from Account 2.
   - Prevents accidental execution, modification, or deletion across accounts.
   - Clear permission enforcement with interactive visual status badges (`🔒 Locked`, `🛡️ Isolated`, `🌐 Shared`).

4. 📁 **Granular Project & Conversation Sync Hub**:
   - **Selective Workspace Sharing**: Choose exactly which projects and folders appear in Instance 2. Unselected projects will not bleed into the second instance.
   - **Safe Copy vs. Cut**: Clone projects to continue with fresh model quotas in the target account, or move and clean up the source.
   - **Transcript & Brain Migration**: Safely migrates local SQLite histories and agent brain artifacts without corrupting internal indices.

5. 📊 **In-Editor HUD Pill & Real-Time Quota Monitor**:
   - Injected live pill inside the Antigravity model bar displaying current account name and tier badge (`PRO`, `ULTRA`, `FREE`).
   - Live reset countdowns and percentage gauges for:
     - `Gemini 3.8 Flash High`
     - `Gemini 3.1 Pro`
     - `Claude Sonnet 4.6`
     - `GPT-OSS 120B`

6. 🍏 **iOS Liquid Glass Aesthetic**:
   - Frosted acrylic glass styling (`backdrop-filter: blur(40px)`), refined specular lighting, and fluid 60fps spring animations.

7. 🔒 **Privacy & Zero-Knowledge Credential Security**:
   - 100% local and offline. Never transmits tokens or credentials to external servers.
   - All OAuth tokens remain securely stored inside your operating system's native credential vault.

8. 💳 **Per-Project Quota Payer Allocation**:
   - Explicitly designate which account pays for prompts in each project.
   - Live credential switching immediately routes language server requests to the designated account.

9. 🤖 **Model Context Protocol (MCP) Server & Agent Skill**:
   - Zero-dependency local stdio MCP server (`mcp_server.py`) exposing live quota queries, identity swaps, and project bindings to AI agents.
   - Built-in Antigravity Agent Skill (`antigravity-account-suite`) enabling coding agents to automatically rotate accounts upon encountering rate limits (`429 / RESOURCE_EXHAUSTED`).

10. ⌨️ **Global Terminal CLI Utilities (`agy-quota` & `agy-switch`)**:
    - Real-time colored progress meters, per-model reset countdowns, JSON output for automation, and scriptable credential control directly from PowerShell and Bash.

---

## 🤖 ChatGPT Desktop & OpenAI Codex Suite

A dedicated, comprehensive companion enhancement suite tailored for the official **ChatGPT Desktop** app and the **OpenAI Codex** ecosystem:

### 1. 🧭 Draggable In-App Floating Action HUD Pill
- A sleek, glassmorphic floating action bar docked dynamically to the top right of ChatGPT Desktop.
- Free-form drag and drop anywhere across your screen with automatic coordinate persistence in `localStorage`.
- Quick-access controls:
  - `➕ New Chat`: Opens an instant conversation canvas (`Ctrl+Shift+O`).
  - `🔄 Accounts`: Opens the profile management and 1-click account switching drawer.
  - `🔐 Login`: Direct entry point for OpenAI OAuth, isolated instances, API keys, and sign-outs.
  - `🎨 Themes & Fonts`: Fine-tunes offline typography, color palettes, and single-card borders.

### 2. 🔐 Authentication & Profile Center
- **🌐 Browser OAuth Login (`codex login`)**: Seamlessly launches your system's default browser to authenticate against OpenAI's official identity provider and syncs credentials into Codex daemon with zero manual copy-pasting.
- **🚀 Concurrent Dual-Instance (`Instance 2`)**: Launches an isolated ChatGPT window with independent `--user-data-dir` for working on secondary or team accounts simultaneously.
- **🔑 Developer API Key Login (`codex login --with-api-key`)**: Authenticate directly with an OpenAI API key (`sk-...`).
- **🚪 Safe Session Sign-Out (`/api/chatgpt/logout`)**: Safely removes stored credentials and resets session state without damaging app installations.

### 3. 🔲 Refined Single-Card Composer Box
- Solves the visual clutter and nested border stacking issues in default ChatGPT Desktop builds.
- Refactored layout styling provides a unified single-card composer frame with smooth 20px curvature, refined 1px border hierarchy, and a subtle glowing focus ring.

### 4. ✍️ Offline Base64 Typography (Zero CDN / Zero CSP Dependencies)
- Fully embedded offline WOFF2 fonts:
  - **Latin / English**: **Outfit** (modern geometric Apple-inspired aesthetic), Inter, and JetBrains Mono.
  - **Persian / Arabic (RTL)**: **Vazirmatn** and **Estedad** with crisp rendering.
- **Intelligent BiDi Text Processor**: Automatic RTL alignment on Persian text blocks while strictly preserving LTR direction for code blocks (`<pre>`, `<code>`) and KaTeX math formulas (`.katex`).

### 5. 🎨 Curated Design Palettes
- ⚡️ **Cyberpunk Neon**: `#00f0ff` cyan accent with crystal obsidian background.
- 🖤 **Pure AMOLED**: Deep true-black `#000000` with subtle glass borders.
- 🌌 **Midnight Indigo**: Indigo `#818cf8` glow with atmospheric depth.
- 🟢 **Emerald Matrix**: Vivid `#10b981` cyber-green.
- ⚪️ **Modern Dark Slate**: Clean `#38bdf8` slate with minimal contrast.

---

### 💡 Quota Architecture: Single-Window vs. Concurrent Multi-Window Best Practices

#### 1. Single-Window Mode (100% Granular Freedom)
- In single-window mode, there are no competing processes for the OS credential store (`gemini:antigravity`).
- You can freely assign and switch the Quota Payer of any project with a single click in the in-editor switcher modal.
- The daemon instantly activates that account's token in Windows Credential Manager without restarting the editor, and the very next prompt is guaranteed to deduct from that account.

#### 2. Concurrent Multi-Window Mode (Clean Window-to-Project Binding)
- **OS Credential Architecture**: Windows maintains a single global credential target (`gemini:antigravity`) per OS user profile.
- **Cross-Wiring Race Condition Risk**: If Window 1 (Account A) is running a project configured to consume Account B, and Window 2 (Account B) is running a project configured to consume Account A, sending prompts concurrently at the exact same millisecond can trigger a race condition where one window temporarily overwrites the other's token.
- **Recommended Best Practice (Window Matching Rule)**:
  - Open projects intended to burn **Account A's quota** inside **Window 1 (Account A)**.
  - Open projects intended to burn **Account B's quota** inside **Window 2 (Account B)**.
  - Use the **Selective Project Sync** checklist to ensure projects only appear in their designated window. This enables you to run both windows side-by-side and prompt simultaneously with 0ms latency and zero cross-account conflicts.

#### 3. Scheduled Tasks & Background Scripts (100% Isolated)
- Background runners, cron jobs, and scheduled tasks are executed using `run_guarded_task`.
- The account token is injected directly into process environment variables (`process.env.GEMINI_CLI_OAUTH_TOKEN`) rather than modifying the OS credential vault.
- As a result, arbitrary background tasks across any number of accounts execute completely concurrently with zero risk of conflict.

---

## 🇪🇸 Español

### Descripción General
Cambiar entre múltiples cuentas de Google en **Google Antigravity** suele ser un proceso complejo debido a que las credenciales de sesión están almacenadas en el **Administrador de Credenciales de Windows** (`service: "gemini"`, `account: "antigravity"`) o en el **Llavero de macOS**.

La **Suite de Cambio de Cuenta y Migración para Antigravity** desarrollada por **[mad-helpers](https://github.com/mad-helpers)** (co-propiedad de **[Madgod-xyz](https://github.com/Madgod-xyz)** & **[Bombhub-apk](https://github.com/Bombhub-apk)**) es una solución nativa multiplataforma de alto rendimiento (GUI de escritorio, píldora HUD integrada en el editor y CLI). Permite alternar identidades en menos de 3 segundos **o** ejecutar dos ventanas de Antigravity simultáneamente de manera independiente con cuentas, tareas y proyectos completamente aislados.

### ✨ Características Principales

1. ⚡️ **Ejecución Concurrente de Dos Instancias (Doble Ventana)**:
   - Inicia una segunda ventana de Antigravity con tu cuenta secundaria (`--user-data-dir="%APPDATA%\Antigravity-Instance2"`).
   - Trabaja en paralelo en proyectos personales y profesionales sin necesidad de cerrar sesión ni interrumpir tu flujo de trabajo.
   - Puertos de depuración DevTools independientes y entornos de ejecución aislados.

2. 🔄 **Cambio Rápido en la Misma Ventana**:
   - Alterna entre cuentas en menos de 3 segundos dentro de la misma ventana activa.
   - Mantiene abiertos tus archivos y espacios de trabajo actuales.

3. ⏱ **Aislamiento de Tareas Programadas y Automatizaciones**:
   - Las tareas programadas y cron jobs creados en la Cuenta 1 no se ejecutarán ni interferirán con la Cuenta 2.
   - Evita la activación accidental de tareas entre perfiles con control de permisos y etiquetas visuales (`🔒 Bloqueada`, `🛡️ Aislada`, `🌐 Compartida`).

4. 📁 **Centro Granular de Sincronización y Migración**:
   - **Selección Selectiva de Proyectos**: Elige con precisión qué proyectos y carpetas están disponibles para la segunda cuenta. Los proyectos no seleccionados permanecen invisibles en la Instancia 2.
   - **Copia Segura o Traslado**: Clona conversaciones de IA para continuar programando con cuotas renovadas, o traslada todo el historial limpiando el origen.
   - **Migración de Transcripciones y Memoria Local**: Mueve el historial SQLite y los artefactos del agente sin dañar los datos.

5. 📊 **Píldora HUD Integrada y Monitor de Cuotas en Vivo**:
   - Píldora interactiva integrada en la barra de selección de modelos de Antigravity que muestra el nombre de la cuenta y la insignia del plan (`PRO`, `ULTRA`, `FREE`).
   - Medidores de cuota y temporizadores de reinicio en tiempo real para:
     - `Gemini 3.8 Flash High`
     - `Gemini 3.1 Pro`
     - `Claude Sonnet 4.6`
     - `GPT-OSS 120B`

6. 🍏 **Diseño Estilo iOS Liquid Glass**:
   - Interfaz con efecto de cristal esmerilado (`backdrop-filter: blur(40px)`), reflejos translúcidos y animaciones fluidas a 60 fps.

7. 🔒 **Privacidad Total y Cero Fuga de Credenciales**:
   - Ejecución 100% local y sin servidores externos.
   - Todas las credenciales se almacenan directamente en los módulos de seguridad protegidos de Windows y macOS.

---

## 🇮🇷 فارسی

### معرفی و قابلیت‌ها
این سوئیت جامع توسعه داده شده توسط سازمان **[mad-helpers](https://github.com/mad-helpers)** (مالکیت مشترک **[Madgod-xyz](https://github.com/Madgod-xyz)** و **[Bombhub-apk](https://github.com/Bombhub-apk)**)، راه‌حلی فوق‌العاده سریع و نیتیو برای سوئیچ هویت‌ها، اجرای همزمان دو پنجره مجزا و انتقال هوشمند پروژه‌ها و مکالمات ایجنت در **Google Antigravity** است.

### 🌟 قابلیت‌های کلیدی:
* ⚡️ **اجرای همزمان دو یا چند پنجره مجزا (Concurrent Multi-Window)** با جیمیل‌های کاملاً تفکیک‌شده و پوشه‌های مستقل داده (`Antigravity-Instance2`، `Antigravity-Instance3` و...).
* 🔄 **سوئیچ تک‌پنجره‌ای زیر ۳ ثانیه** بدون بستن یا از دست رفتن فایل‌های در حال ویرایش.
* 💳 **تعیین حساب کسر سهمیه به تفکیک پروژه (Per-Project Quota Payer)**: قابلیت انتخاب این که پرامپت‌های هر پروژه دقیقاً از سهمیه کدام اکانت کسر شوند.
* ⏱ **ایزوله‌سازی وظایف زمان‌بندی شده (Scheduled Tasks Isolation)**: اجرای مستقل تسک‌ها و کران‌جاب‌ها با متغیرهای محیطی ایزوله بدون کوچک‌ترین تداخل در مخزن کلید سیستم‌عامل.
* 📁 **مرکز گزینش و همگام‌سازی پروژه‌ها (Granular Project Sync Hub)**: انتخاب چک‌باکسی پروژه‌های مجاز برای اکانت دوم بدون قاطی شدن فایل‌های ناخواسته.
* 📊 **نشانگر شناور درون‌برنامه‌ای (In-Editor HUD Pill)** در نوار انتخاب مدل با نمایش رتبه (`PRO` / `ULTRA`) و مصرف لحظه‌ای سهمیه‌ها (تفکیک دقیق سهمیه ۵ ساعته و هفتگی).
* 🍏 **طراحی فوق‌العاده زیبای شیشه‌ای اپل (iOS Liquid Glass)** با انیمیشن‌های نرم ۶۰ فریم و پشتیبانی کامل راست‌چین (RTL).
* 🤖 **سرور محلی پروتکل زمینه مدل (MCP Server)** بدون نیاز به وابستگی خارجی (`mcp_server.py`) برای اتصال مستقیم ابزارهای سوئیچ اکانت و بررسی سهمیه به ایجنت‌های هوش مصنوعی.
* ⌨️ **دستورات جهانی خط فرمان (`agy-quota` و `agy-switch`)**: نمایش نمودارهای گرافیکی درصد سهمیه‌ها، زمان بازنشانی مدل‌ها و خروجی ساختاریافته JSON جهت اتوماسیون کامل.

---

### 💡 راهنمای معماری سهمیه‌ها: حالت تک‌پنجره در برابر چندپنجره‌ی همزمان

#### ۱. حالت تک‌پنجره (Single-Window - آزادی عمل ۱۰۰٪)
* در حالت تک‌پنجره، هیچ پروسه‌ی موازی دیگری برای مخزن توکن ویندوز (`gemini:antigravity`) رقابت نمی‌کند.
* **تغییر آنی کسر سهمیه**: در هر پروژه‌ای که باشید، کافی است در تب پروژه‌ها روی حساب مد نظرتان در بخش **«💳 کسر سهمیه از (Quota Payer)»** کلیک کنید. سیستم بلافاصله توکن همان حساب را در مخزن فعال می‌کند و از همان ثانیه، پرامپت بعدی ایجنت دقیقاً از سهمیه همان حساب کسر می‌شود.
* نشانگر وضعیت در پایین صفحه در لحظه نام اکانت و درصد باقیمانده سهمیه را بروزرسانی می‌کند.

#### ۲. حالت چندپنجره‌ی همزمان (Multi-Window Concurrency & Best Practice)
* **زیر کاپوت سیستم‌عامل**: ویندوز برای هر کاربر سیستم‌عامل یک مخزن واحد کلید دارد. هر پنجره ادیتور دارای پروسه مستقل زبانی است، اما مخزن کلید ویندوز بین پروسه‌ها مشترک است.
* **خطر تداخل ضربدری (Cross-Wiring Race Condition)**: اگر در پنجره ۱ (اکانت بمب‌هاب) پروژه‌ای باز کنید که روی سهمیه مدگاد تنظیم شده باشد، و همزمان در پنجره ۲ (اکانت مدگاد) پروژه‌ای باز کنید که روی سهمیه بمب‌هاب تنظیم شده باشد، در صورت **ارسال همزمان پرامپت در یک صدم ثانیه مشترک**، این دو پنجره برای تغییر توکن مخزن ویندوز با هم رقابت می‌کنند و ممکن است پرامپت از اکانت اشتباه کسر شود.
* **راهکار اصولی و پیشنهادی (قانون تطابق پروژه با پنجره)**:
  * پروژه‌های مربوط به سهمیه **اکانت ۱** را در **پنجره ۱** باز کنید.
  * پروژه‌های مربوط به سهمیه **اکانت ۲** را در **پنجره ۲** باز کنید.
  * با استفاده از قابلیت **«سینک انتخابی»** می‌توانید تعیین کنید هر پروژه فقط در پنجره اکانت خودش در دسترس باشد. در این حالت می‌توانید **هر دو پنجره را کنار هم بگذارید و به صورت کاملاً همزمان پرامپت بفرستید** بدون اینکه ۱ میلی‌ثانیه تداخل یا خطایی رخ دهد.

#### ۳. تسک‌های زمان‌بندی‌شده و اسکریپت‌های پس‌زمینه (۱۰۰٪ ایزوله)
* تسک‌های خودکار روزانه و اسکریپت‌های ایجنت با متد `run_guarded_task` اجرا می‌شوند.
* این متد توکن مخصوص اکانتِ تعیین‌شده برای آن تسک را مستقیماً داخل متغیرهای محیطی خود پروسه (`process.env.GEMINI_CLI_OAUTH_TOKEN`) تزریق می‌کند و کاری به مخزن ویندوز ندارد.
* بنابراین حتی اگر چندین تسک متعلق به چندین اکانت مختلف به طور همزمان اجرا شوند، کوچک‌ترین تداخلی ایجاد نخواهد شد.

---

### ⌨️ راهنمای دستورات خط فرمان (CLI)

ابزارهای خط فرمان به صورت سراسری در مسیر `%USERPROFILE%\.gemini\bin` (در ویندوز) و `/usr/local/bin` (در مک/لینوکس) نصب و ثبت شده‌اند:

#### ۱. ابزار نمایش سهمیه (`agy-quota`)
```bash
agy-quota                      # 📊 نمایش لحظه‌ای سهمیه نشست ۵ ساعته و هفتگی با نوارهای رنگی
agy-quota --status-json        # 🤖 دریافت وضعیت کامل سهمیه‌ها در قالب JSON جهت اتوماسیون
agy-quota --list               # 📋 فهرست تمام حساب‌های ثبت‌شده به همراه وضعیت فعال/غیرفعال
```

#### ۲. ابزار مدیریت حساب‌ها و پروژه‌ها (`agy-switch`)
```bash
agy-switch                                      # 🖥 اجرای محیط گرافیکی شیشه‌ای (Liquid Glass GUI)
agy-switch --usage                              # 📊 داشبورد متنی محدودیت‌های مدل‌ها در ترمینال
agy-switch --list                               # 📋 مشاهده تمام اکانت‌های ذخیره‌شده و اکانت فعال
agy-switch --switch <email>                     # ⚡️ تغییر آنی اکانت در Credential Manager سیستم‌عامل
agy-switch --switch <email> --no-restart        # 🔄 سوئیچ سریع توکن بدون راه‌اندازی مجدد ادیتور
agy-switch --set-project-quota <proj> <email>   # 💳 تعیین حساب کسر سهمیه برای یک پروژه مشخص
agy-switch --launch-instance <slot_or_email>    # 🚀 اجرای پنجره مجزا برای حساب (مانند instance_2)
agy-switch --status-json                        # 🤖 خروجی جامع ساختاریافته برای ایجنت‌های هوش مصنوعی
agy-switch --save                               # 💾 ذخیره نشست فعال فعلی در فایل manifest
agy-switch --logout                             # ➕ خروج از حساب فعال جهت لاگین با اکانت جدید
agy-switch --help                               # ℹ️ راهنمای کامل دستورات و پارامترها
```

---

### 🤖 سرور محلی پروتکل زمینه مدل (MCP Server)

این سوئیت شامل یک سرور بومی و سبک استدیو MCP بدون وابستگی خارجی (`mcp_server.py`) است که به ایجنت‌های هوش مصنوعی (Google Antigravity, Claude Code, Gemini CLI, Cursor, VS Code) اجازه می‌دهد به سادگی و به شکل مستقل وضعیت سهمیه‌ها را بررسی کنند و بین هویت‌ها جابه‌جا شوند.

#### ابزارهای ثبت‌شده در MCP:
| نام ابزار | توضیحات | پارامترها |
| :--- | :--- | :--- |
| `get_quota_status` | دریافت سهمیه زنده، تایمر ۵ ساعته، سهمیه هفتگی و مصرف مدل‌ها | `account` (اختیاری: ایمیل یا شناسه)، `include_all` (بولین اختیاری) |
| `switch_account` | سوئیچ توکن فعال در Credential Manager / Keychain | `account` (ایمیل یا نام مستعار اجباری)، `no_restart` (بولین اختیاری) |
| `set_project_quota` | انتساب حساب پرداخت‌کننده سهمیه برای یک فضای کاری | `project` (نام، شناسه یا مسیر پروژه)، `account` (ایمیل یا نام مستعار) |
| `list_saved_accounts` | دریافت لیست همه اکانت‌های ذخیره‌شده با طرح اشتراک و سهمیه‌ها | بدون پارامتر |

#### نمونه تنظیمات MCP (`settings.json` یا `mcp_config.json`):
```json
{
  "mcpServers": {
    "antigravity-account-suite": {
      "command": "python",
      "args": [
        "C:\\Users\\gerap\\Desktop\\agent-helper\\antigravity-account-switcher\\mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

### 🧠 مهارت اختصاصی ایجنت هوش مصنوعی (`antigravity-account-suite`)

این مهارت در مسیر `~/.gemini/config/skills/antigravity-account-suite/SKILL.md` و همچنین داخل پوشه `skills/` مخزن نصب گردیده است:
- **مدیریت خودکار خطای اتمام سهمیه (Automatic Quota Failover)**: زمانی که ایجنت در حین انجام وظایف با خطای نرخ مصرف (`429 Too Many Requests` یا `RESOURCE_EXHAUSTED`) مواجه می‌شود، به صورت خودکار دستور `agy-switch --status-json` را فراخوانی کرده، حسابی که بیشترین سهمیه باقیمانده را دارد برمی‌گزیند و با دستور `agy-switch --switch <account> --no-restart` بدون متوقف کردن یا مزاحمت برای کاربر، فرآیند کدنویسی را از سر می‌گیرد.
- **ایزوله‌سازی پروژه‌ها**: ایجنت به طور خودکار مطمئن می‌شود که درخواست‌های ارسالی به سرور زبانی از حسابی کسر شوند که برای آن پروژه اختصاص یافته است.

---

## 🇨🇳 简体中文

### 概述与核心特性
由 **[mad-helpers](https://github.com/mad-helpers)**（联合所有者 **[Madgod-xyz](https://github.com/Madgod-xyz)** 与 **[Bombhub-apk](https://github.com/Bombhub-apk)**）精心打造的 Antigravity 账号管理与迁移套件，提供一键极速切号、多实例双开并发、任务隔离及项目资产跨账号同步功能。

* ⚡️ **多开并发实例**：同时运行两个独立的 Antigravity 窗口，各自绑定独立 Google 账号。
* 🔄 **秒级同窗口切换**：3 秒内平滑切换身份，保留当前项目。
* ⏱ **定时任务隔离**：主账号的自动化定时任务不会在第二账号触发，保证环境干净独立。
* 📁 **项目精细化勾选与同步**：按需分配对第二实例可见的项目和 Agent 对话。
* 📊 **编辑器内嵌配额 HUD**：实时显示剩余调用量及重置倒计时。

---

## ⌨️ CLI Commands & Utilities

Global CLI tools are automatically registered in `%USERPROFILE%\.gemini\bin` (Windows) and `/usr/local/bin` (macOS/Linux):

### 1. `agy-quota` — Dedicated Quota HUD
```bash
agy-quota                      # 📊 Display live session & weekly quotas with colored bars
agy-quota --status-json        # 🤖 Machine-readable JSON status for scripts & agents
agy-quota --list               # 📋 List all registered accounts and active status
```

### 2. `agy-switch` — Full Account & Project Suite
```bash
agy-switch                                      # 🖥 Open the iOS Liquid Glass Desktop GUI
agy-switch --usage                              # 📊 Terminal dashboard of live model limits
agy-switch --list                               # 📋 List registered accounts with active status
agy-switch --switch <email>                     # ⚡️ Switch active identity in OS Credential Manager
agy-switch --switch <email> --no-restart        # 🔄 Switch credential without restarting IDE
agy-switch --set-project-quota <proj> <email>   # 💳 Assign designated quota payer for project
agy-switch --launch-instance <slot_or_email>    # 🚀 Launch or focus isolated instance (e.g. instance_2)
agy-switch --status-json                        # 🤖 Full JSON payload (active quota, manifest, instances)
agy-switch --save                               # 💾 Save active session token to manifest
agy-switch --logout                             # ➕ Log out active session to add a new account
agy-switch --help                               # ℹ️ Display help and command syntax
```

---

## 🤖 Model Context Protocol (MCP) Server

The suite includes a lightweight, zero-dependency stdio MCP server (`mcp_server.py`) allowing autonomous coding agents (Google Antigravity, Claude Code, Gemini CLI, Cursor, VS Code) to inspect quotas and manage identities programmatically.

### Registered MCP Tools:
| Tool Name | Description | Parameters |
| :--- | :--- | :--- |
| `get_quota_status` | Returns live quota, 5-hour session reset timer, weekly limit, and per-model stats | `account` (optional string), `include_all` (optional bool) |
| `switch_account` | Switches active token in OS Credential Manager / Keychain | `account` (required string), `no_restart` (optional bool) |
| `set_project_quota` | Configures designated Google account payer for a project | `project` (required string), `account` (required string) |
| `list_saved_accounts` | Lists all registered accounts, tiers, quotas, and active status | None |

### Configuration Snippet:
Add to your IDE or agent config (`settings.json` or `mcp_config.json`):
```json
{
  "mcpServers": {
    "antigravity-account-suite": {
      "command": "python",
      "args": [
        "C:\\Users\\gerap\\Desktop\\agent-helper\\antigravity-account-switcher\\mcp_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## 🧠 Antigravity Agent Skill (`antigravity-account-suite`)

Installed at `~/.gemini/config/skills/antigravity-account-suite/SKILL.md` and in the repository under `skills/`:
- **Automated Quota Failover**: When an autonomous agent encounters `429 Too Many Requests` or `RESOURCE_EXHAUSTED`, it queries `agy-switch --status-json`, picks the account with highest remaining quota, and executes `agy-switch --switch <account> --no-restart` to resume coding without user interruption.
- **Project Isolation**: Automatically verifies that workspace prompts are routed to the project's designated payer account.


---

## 🛠 Architecture & How It Works

```mermaid
graph TD
    A[Google Antigravity Primary Window] -->|Local CDP Port 64591| B[Sync Daemon & HUD Injector]
    C[Google Antigravity Secondary Window] -->|Local CDP Port 54851| B
    
    B -->|Task Isolation & Manifest| D[Task Isolation Engine]
    B -->|Project Sync Rules| E[Migration & Sync Engine]
    
    D -->|Windows SchTasks / Crons| F[Operating System Task Scheduler]
    E -->|Conversations & Brain Folders| G[Local Antigravity Brain DBs]
    
    B -->|Vault Interop: advapi32.dll / security| H[OS Credential Manager / Keychain]
    B -->|Quota & Tier Queries| I[Google CloudCode API]
    
    J[iOS Liquid Glass Web App & In-Editor HUD] -->|IPC & REST API| B
```

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for details.

Developed with precision and care by **[mad-helpers](https://github.com/mad-helpers)** ([Madgod-xyz](https://github.com/Madgod-xyz) & [Bombhub-apk](https://github.com/Bombhub-apk)).
