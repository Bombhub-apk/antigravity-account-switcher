# Antigravity Account Switcher & Project Migration Suite ⚡️

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11%20%7C%20macOS%20%7C%20Linux-brightgreen.svg)]()
[![Antigravity](https://img.shields.io/badge/Antigravity-2.0%2B-cyan.svg)]()
[![UI Design](https://img.shields.io/badge/Design-iOS%20Liquid%20Glass-purple.svg)]()
[![Languages](https://img.shields.io/badge/Languages-EN%20%7C%20ES%20%7C%20FA%20%7C%20ZH-orange.svg)]()
[![Author](https://img.shields.io/badge/Author-Ethan%20Carter-blueviolet.svg)](https://github.com/Bombhub-apk)

> **Super-fast 1-click Google Account Switcher, Concurrent Dual-Instance Runner, Real-Time Quota HUD, and AI Project & Chat Migration Suite for Google Antigravity.**  
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
- [Español (🇪🇸 Descripción y Características)](#-español)
- [فارسی (🇮🇷 راهنما و مستندات فارسی)](#-فارسی)
- [简体中文 (🇨🇳 概述与使用指南)](#-简体中文)
- [Installation & Quick Start](#-installation)
- [CLI Reference](#-cli-commands)
- [Architecture & Mechanics](#-architecture--how-it-works)

---

## 🚀 Installation

### 🪟 Windows 10 & 11 (PowerShell)
Open PowerShell as your standard user and run:
```powershell
irm https://raw.githubusercontent.com/Bombhub-apk/antigravity-account-switcher/master/install.ps1 | iex
```
*Creates `Antigravity Switcher` shortcuts on your Desktop & Start Menu, installs background sync daemons, and registers `agy-switch` in your PATH.*

### 🍏 macOS (Apple Silicon M1/M2/M3/M4 & Intel)
Open Terminal and run:
```bash
curl -fsSL https://raw.githubusercontent.com/Bombhub-apk/antigravity-account-switcher/master/install.sh | bash
```
*Builds and installs `AntigravitySwitcher.app` in `/Applications` and `~/Desktop`, and links `agy-switch` into your PATH.*

---

## 🇬🇧 English

### Overview
Switching between multiple Google accounts on **Google Antigravity** can be tedious and disruptive because session credentials are bound inside **Windows Credential Manager** (`service: "gemini"`, `account: "antigravity"`) or **macOS Keychain**.

**Antigravity Account Switcher & Migration Suite** by **[Ethan Carter](https://github.com/Bombhub-apk)** is a high-performance native cross-platform solution (GUI, in-editor HUD pill, and CLI). It allows you to swap identities in under 3 seconds **or** run two completely isolated Antigravity instances side-by-side on the same machine with independent credentials, tasks, and project access.

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

---

### 🇪🇸 Español

### Descripción General
Cambiar entre múltiples cuentas de Google en **Google Antigravity** suele ser un proceso complejo debido a que las credenciales de sesión están almacenadas en el **Administrador de Credenciales de Windows** (`service: "gemini"`, `account: "antigravity"`) o en el **Llavero de macOS**.

La **Suite de Cambio de Cuenta y Migración para Antigravity** desarrollada por **[Ethan Carter](https://github.com/Bombhub-apk)** es una solución nativa multiplataforma de alto rendimiento (GUI de escritorio, píldora HUD integrada en el editor y CLI). Permite alternar identidades en menos de 3 segundos **o** ejecutar dos ventanas de Antigravity simultáneamente de manera independiente con cuentas, tareas y proyectos completamente aislados.

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
این سوئیت جامع توسعه داده شده توسط **[Ethan Carter](https://github.com/Bombhub-apk)**، راه‌حلی فوق‌العاده سریع و نیتیو برای سوئیچ هویت‌ها، اجرای همزمان دو پنجره مجزا و انتقال هوشمند پروژه‌ها و مکالمات ایجنت در **Google Antigravity** است.

### 🌟 قابلیت‌های کلیدی:
* ⚡️ **اجرای همزمان دو پنجره مجزا (Dual-Instance Concurrent Runner)** با دو جیمیل کاملاً تفکیک‌شده و پوشه‌های مستقل داده (`Antigravity-Instance2`).
* 🔄 **سوئیچ تک‌پنجره‌ای زیر ۳ ثانیه** بدون بستن یا از دست رفتن فایل‌های در حال ویرایش.
* ⏱ **ایزوله‌سازی وظایف زمان‌بندی شده (Scheduled Tasks Isolation)**: جلوگیری قطعی از اجرای تسک‌های اکانت ۱ در اکانت ۲ همراه با قفل امنیتی دسترسی.
* 📁 **مرکز گزینش و همگام‌سازی پروژه‌ها (Granular Project Sync Hub)**: انتخاب چک‌باکسی پروژه‌های مجاز برای اکانت دوم بدون قاطی شدن فایل‌های ناخواسته.
* 📊 **نشانگر شناور درون‌برنامه‌ای (In-Editor HUD Pill)** در نوار انتخاب مدل با نمایش رتبه (`PRO` / `ULTRA`) و مصرف لحظه‌ای سهمیه‌ها.
* 🍏 **طراحی فوق‌العاده زیبای شیشه‌ای اپل (iOS Liquid Glass)** با انیمیشن‌های نرم ۶۰ فریم و پشتیبانی کامل راست‌چین (RTL).

---

## 🇨🇳 简体中文

### 概述与核心特性
由 **[Ethan Carter](https://github.com/Bombhub-apk)** 精心打造的 Antigravity 账号管理与迁移套件，提供一键极速切号、多实例双开并发、任务隔离及项目资产跨账号同步功能。

* ⚡️ **多开并发实例**：同时运行两个独立的 Antigravity 窗口，各自绑定独立 Google 账号。
* 🔄 **秒级同窗口切换**：3 秒内平滑切换身份，保留当前项目。
* ⏱ **定时任务隔离**：主账号的自动化定时任务不会在第二账号触发，保证环境干净独立。
* 📁 **项目精细化勾选与同步**：按需分配对第二实例可见的项目和 Agent 对话。
* 📊 **编辑器内嵌配额 HUD**：实时显示剩余调用量及重置倒计时。

---

## ⌨️ CLI Commands

```bash
agy-switch                 # 🖥 Open the iOS Liquid Glass Desktop GUI
agy-switch --usage         # 📊 View live model quotas and countdowns in terminal
agy-switch --list          # 📋 List all saved accounts and active session
agy-switch --switch email  # ⚡️ Switch to a specific account immediately
agy-switch --save          # 💾 Save the current active account
agy-switch --logout        # ➕ Logout current account to sign into a new one
agy-switch --migrate       # 🔄 List local project conversations for migration
agy-switch --about         # ℹ️ Display author & version information
```

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

Developed with precision and care by **[Ethan Carter](https://github.com/Bombhub-apk)**.
