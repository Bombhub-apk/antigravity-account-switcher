"""
Antigravity IDE Theme, Persian Fonts, Neon Glow & Live Customizer Suite
Permanent installer for Antigravity IDE:
- Embeds Vazirmatn, Estedad, Outfit WOFF2 fonts + Local Vazir/Vazirmatn support
- Floating Draggable HUD Pill (Theme Customizer + Account Switcher) like ChatGPT Enhanced / GPT plugin
- Live Interactive Theme & Neon Customization Modal (Cyberpunk, SynthWave, AMOLED, Midnight, Emerald, Sunset)
- High Neon Glow, Refined Glass & Subtle stroke options
- Full Smart BiDi for Monaco Editor (Persian Markdown lines RTL, Code blocks LTR)
- Universal Persian Typography & RTL for Antigravity Agent Chat & Prose
- Updates product.json SHA-256 base64 checksums to eliminate corrupt installation warnings
- Configures User settings.json with optimal Markdown and Persian defaults
"""

import os
import sys
import json
import base64
import hashlib
import shutil
from pathlib import Path

# Fix console encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HOME = Path.home()
IDE_APP_DIR = Path(os.getenv("LOCALAPPDATA", str(HOME / "AppData" / "Local"))) / "Programs" / "Antigravity IDE" / "resources" / "app"
IDE_USER_SETTINGS = Path(os.getenv("APPDATA", str(HOME / "AppData" / "Roaming"))) / "Antigravity IDE" / "User" / "settings.json"

FONT_SOURCES = [
    Path(__file__).resolve().parent / "assets" / "fonts",
    HOME / ".gemini" / "antigravity" / "bin" / "assets" / "fonts",
]

def find_font_file(filename):
    for d in FONT_SOURCES:
        p = d / filename
        if p.exists():
            return p
    return None

def compute_checksum(file_path):
    content = file_path.read_bytes()
    h = hashlib.sha256(content).digest()
    return base64.b64encode(h).decode('ascii').rstrip('=')

def setup_ide_theme():
    print("=" * 60)
    print("⚡️ Setting up Antigravity IDE Live Theme, Neon Glow & Font Suite")
    print("=" * 60)

    if not IDE_APP_DIR.exists():
        print(f"❌ Antigravity IDE not found at: {IDE_APP_DIR}")
        return False

    out_dir = IDE_APP_DIR / "out"
    wb_dir = out_dir / "vs" / "workbench"
    fonts_dest_1 = wb_dir / "fonts"
    fonts_dest_2 = out_dir / "fonts"

    fonts_dest_1.mkdir(parents=True, exist_ok=True)
    fonts_dest_2.mkdir(parents=True, exist_ok=True)

    # 1. Locate and copy font files
    font_files = {
        "Vazirmatn": "Vazirmatn[wght].woff2",
        "Estedad": "Estedad[wght].woff2",
        "Outfit": "Outfit[wght].woff2"
    }

    font_b64 = {}
    for name, filename in font_files.items():
        src = find_font_file(filename)
        if src and src.exists():
            shutil.copy2(src, fonts_dest_1 / filename)
            shutil.copy2(src, fonts_dest_2 / filename)
            raw = src.read_bytes()
            font_b64[name] = base64.b64encode(raw).decode('ascii')
            print(f"✓ Copied {filename} ({len(raw)} bytes)")
        else:
            print(f"⚠️ Font file not found: {filename}")
            font_b64[name] = ""

    vazir_b64 = font_b64.get("Vazirmatn", "")
    estedad_b64 = font_b64.get("Estedad", "")
    outfit_b64 = font_b64.get("Outfit", "")

    # 2. Build antigravity-custom-theme.css (Base foundational styles)
    theme_css = f"""/* Antigravity IDE Permanent Modern Theme & Persian Typography Suite */
/* Generated automatically by setup_ide_theme.py */

/* --- 1. Embedded Web Fonts --- */
@font-face {{
  font-family: 'Outfit';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('./fonts/Outfit[wght].woff2') format('woff2'),
       url('../../../fonts/Outfit[wght].woff2') format('woff2'),
       url('data:font/woff2;base64,{outfit_b64}') format('woff2');
}}

@font-face {{
  font-family: 'Vazirmatn';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('./fonts/Vazirmatn[wght].woff2') format('woff2'),
       url('../../../fonts/Vazirmatn[wght].woff2') format('woff2'),
       url('data:font/woff2;base64,{vazir_b64}') format('woff2');
}}

@font-face {{
  font-family: 'Estedad';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('./fonts/Estedad[wght].woff2') format('woff2'),
       url('../../../fonts/Estedad[wght].woff2') format('woff2'),
       url('data:font/woff2;base64,{estedad_b64}') format('woff2');
}}

/* --- 2. Universal IDE Typography & Chrome Styling --- */
:root {{
  --vscode-font-family: 'Outfit', 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
  --cpe-font: 'Outfit', 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', sans-serif;
  --cpe-accent: #00f0ff;
  --cpe-accent-glow: 0 0 18px rgba(0, 240, 255, 0.55);
  --cpe-accent-soft: rgba(0, 240, 255, 0.15);
  --cpe-border: rgba(0, 240, 255, 0.32);
}}

body,
.monaco-workbench,
.monaco-shell,
.part,
.part.titlebar,
.part.sidebar,
.part.activitybar,
.part.statusbar,
.monaco-list,
.monaco-tree,
.action-label,
.label-name,
.quick-input-widget,
.monaco-inputbox input,
.monaco-select-box,
.interactive-session,
.chat-widget,
.rendered-markdown,
.font-sans,
[class*="font-sans"],
[class*="chat"],
[class*="agent"],
[class*="sidebar"],
[class*="jetski"] {{
  font-family: 'Outfit', 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}}

/* --- 3. Persian BiDi in Chat, Prose & Markdown Previews --- */
.rendered-markdown p,
.rendered-markdown li,
.rendered-markdown h1,
.rendered-markdown h2,
.rendered-markdown h3,
.rendered-markdown h4,
.rendered-markdown h5,
.rendered-markdown h6,
.rendered-markdown blockquote,
.chat-item p,
.chat-response-text,
[class*="chat-message"] p,
[class*="chat-turn"] p,
[class*="prose"] p,
[class*="prose"] li,
[class*="prose"] h1,
[class*="prose"] h2,
[class*="prose"] h3,
[class*="markdown"] p,
[class*="markdown"] li,
.bidi-auto {{
  unicode-bidi: plaintext !important;
  text-align: start !important;
  line-height: 1.85 !important;
  letter-spacing: -0.01em !important;
}}

/* Direct RTL class for Persian elements */
[dir="rtl"],
.rtl,
.bidi-rtl,
:lang(fa),
:lang(ar) {{
  direction: rtl !important;
  text-align: right !important;
  font-family: 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', sans-serif !important;
}}

[dir="ltr"],
.ltr,
.bidi-ltr {{
  direction: ltr !important;
  text-align: left !important;
}}

/* Chat Textareas & Inputs */
textarea,
input,
[contenteditable="true"],
[class*="composer"],
[class*="chat-input"] {{
  font-family: 'Outfit', 'Vazirmatn', 'Estedad', sans-serif !important;
  unicode-bidi: plaintext !important;
}}

/* --- 4. Monaco Editor Persian & Markdown BiDi Engine --- */
/* Markdown & Plaintext editor font */
.monaco-editor[data-mode-id="markdown"],
.monaco-editor[data-mode-id="plaintext"],
.editor-instance[aria-label*=".md"],
.editor-instance[aria-label*=".markdown"],
.monaco-editor[data-uri*=".md"],
.monaco-editor[data-uri*=".markdown"] {{
  font-family: 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', 'Outfit', sans-serif !important;
}}

.monaco-editor[data-mode-id="markdown"] .view-line,
.monaco-editor[data-mode-id="plaintext"] .view-line,
.editor-instance[aria-label*=".md"] .view-line,
.editor-instance[aria-label*=".markdown"] .view-line,
.monaco-editor[data-uri*=".md"] .view-line,
.monaco-editor[data-uri*=".markdown"] .view-line {{
  font-family: 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', 'Outfit', sans-serif !important;
  line-height: 1.85 !important;
}}

/* In markdown editors, allow tokens inside lines to resolve BiDi cleanly */
.editor-instance[aria-label*=".md"] .view-line > span,
.editor-instance[aria-label*=".markdown"] .view-line > span,
.monaco-editor[data-uri*=".md"] .view-line > span,
.monaco-editor[data-mode-id="markdown"] .view-line > span {{
  unicode-bidi: plaintext !important;
}}

/* Persian lines in Monaco Editor (automatically flagged by runtime enhancer) */
.monaco-editor .view-line.bidi-rtl-line,
.editor-instance[aria-label*=".md"] .view-line.bidi-rtl-line,
.editor-instance[aria-label*=".markdown"] .view-line.bidi-rtl-line,
.monaco-editor[data-uri*=".md"] .view-line.bidi-rtl-line {{
  direction: rtl !important;
  text-align: right !important;
  width: calc(100% - 24px) !important;
  font-family: 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', sans-serif !important;
}}

.monaco-editor .view-line.bidi-rtl-line > span,
.editor-instance[aria-label*=".md"] .view-line.bidi-rtl-line > span,
.editor-instance[aria-label*=".markdown"] .view-line.bidi-rtl-line > span,
.monaco-editor[data-uri*=".md"] .view-line.bidi-rtl-line > span {{
  direction: rtl !important;
  unicode-bidi: plaintext !important;
  font-family: 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', sans-serif !important;
}}

/* English / Code lines inside markdown or code files stay strictly LTR */
.monaco-editor .view-line.bidi-ltr-line,
.editor-instance[aria-label*=".md"] .view-line.bidi-ltr-line,
.monaco-editor .view-line:has([class*="fenced"]),
.monaco-editor .view-line:has([class*="code-block"]) {{
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: isolate !important;
}}

/* Selection highlight in RTL lines */
.editor-instance[aria-label*=".md"] .selected-text[style*="left:0"],
.monaco-editor .view-line.bidi-rtl-line ~ .selected-text[style*="left:0"] {{
  right: 0 !important;
  left: auto !important;
}}

/* --- 5. Strict Code Blocks, Terminals & Formulas (100% LTR & Monospace) --- */
.terminal,
.terminal *,
.xterm,
.xterm *,
pre,
code,
kbd,
samp,
.monaco-tokenized-source,
[class*="code-block"],
.rendered-markdown pre,
.rendered-markdown code,
pre *,
code * {{
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: isolate !important;
  font-family: Consolas, 'Cascadia Code', 'Courier New', monospace !important;
}}

.katex,
.katex *,
.katex-display,
.katex-html,
math,
math * {{
  direction: ltr !important;
  text-align: left !important;
  unicode-bidi: isolate !important;
}}

.katex-display {{
  text-align: center !important;
}}

/* Slim Sleek Scrollbars */
.monaco-scrollable-element > .scrollbar > .slider {{
  border-radius: 8px !important;
  background: rgba(255, 255, 255, 0.15) !important;
  transition: background 0.15s ease !important;
}}

.monaco-scrollable-element > .scrollbar > .slider:hover {{
  background: rgba(0, 240, 255, 0.45) !important;
}}
"""

    custom_theme_path = wb_dir / "antigravity-custom-theme.css"
    custom_theme_path.write_text(theme_css, encoding="utf-8")
    print(f"✓ Created {custom_theme_path.name} ({len(theme_css)} chars)")

    # 3. Create antigravity-ide-enhancer.js (Full Theme Customizer, Neon Glow, HUD & BiDi Engine)
    enhancer_js = """// Antigravity IDE Runtime BiDi, Theme Customizer & Neon Suite
// Fully integrated with Custom Themes (Cyberpunk, Synthwave, AMOLED, etc.), Fonts, HUD Pill & Modal
(() => {
  if (window.__agy_ide_enhancer_loaded) return;
  window.__agy_ide_enhancer_loaded = true;

  const STORAGE_KEY = 'agy_ide_theme_settings';
  const PERSIAN_REGEX = /[\\u0600-\\u06FF\\u0750-\\u077F\\uFB50-\\uFDFF\\uFE70-\\uFEFF]/;

  // 1. Color Palettes & Themes
  const THEMES = {
    cyber: {
      name: '⚡️ سایبرپانک نئون (Cyberpunk Neon)',
      accent: '#00f0ff',
      accentGlow: '0 0 18px rgba(0, 240, 255, 0.55)',
      accentSoft: 'rgba(0, 240, 255, 0.15)',
      border: 'rgba(0, 240, 255, 0.32)',
      bg: '#080c14',
      bgGradient: 'radial-gradient(ellipse at 50% 0%, #101c33 0%, #060910 75%)',
      sidebar: '#05080f',
      card: '#0f1728',
      cardBorder: 'rgba(0, 240, 255, 0.25)',
      composerBg: 'rgba(15, 23, 42, 0.95)',
      text: '#f1f5f9'
    },
    synthwave: {
      name: '💜 سینت‌ویو ۸۴ (SynthWave Neon)',
      accent: '#ff007f',
      accentSecondary: '#00f0ff',
      accentGlow: '0 0 20px rgba(255, 0, 127, 0.6)',
      accentSoft: 'rgba(255, 0, 127, 0.16)',
      border: 'rgba(255, 0, 127, 0.35)',
      bg: '#0d071a',
      bgGradient: 'radial-gradient(ellipse at 50% 0%, #250f42 0%, #080312 75%)',
      sidebar: '#080312',
      card: '#1a0d30',
      cardBorder: 'rgba(255, 0, 127, 0.28)',
      composerBg: 'rgba(24, 13, 46, 0.95)',
      text: '#fff0f8'
    },
    amoled: {
      name: '🖤 آمولد بلک و شیشه‌ای (Pure AMOLED & Glass)',
      accent: '#38bdf8',
      accentGlow: '0 0 14px rgba(56, 189, 248, 0.4)',
      accentSoft: 'rgba(255, 255, 255, 0.08)',
      border: 'rgba(255, 255, 255, 0.18)',
      bg: '#000000',
      bgGradient: '#000000',
      sidebar: '#040404',
      card: '#0d0d0d',
      cardBorder: 'rgba(255, 255, 255, 0.15)',
      composerBg: '#080808',
      text: '#ffffff'
    },
    midnight: {
      name: '🌌 میدنایت ایندیگو (Midnight Indigo)',
      accent: '#818cf8',
      accentGlow: '0 0 18px rgba(129, 140, 248, 0.5)',
      accentSoft: 'rgba(99, 102, 241, 0.16)',
      border: 'rgba(99, 102, 241, 0.28)',
      bg: '#0a0e1a',
      bgGradient: 'radial-gradient(ellipse at 50% 0%, #17203b 0%, #070a13 75%)',
      sidebar: '#060912',
      card: '#12182c',
      cardBorder: 'rgba(99, 102, 241, 0.25)',
      composerBg: 'rgba(18, 24, 44, 0.95)',
      text: '#f8fafc'
    },
    emerald: {
      name: '🟢 ماتریکس زمردی (Emerald Matrix)',
      accent: '#10b981',
      accentGlow: '0 0 18px rgba(16, 185, 129, 0.5)',
      accentSoft: 'rgba(16, 185, 129, 0.16)',
      border: 'rgba(16, 185, 129, 0.28)',
      bg: '#06100a',
      bgGradient: 'radial-gradient(ellipse at 50% 0%, #0e291a 0%, #040a06 75%)',
      sidebar: '#030805',
      card: '#0c2014',
      cardBorder: 'rgba(16, 185, 129, 0.25)',
      composerBg: 'rgba(10, 26, 17, 0.95)',
      text: '#ecfdf5'
    },
    sunset: {
      name: '🌅 سان‌ست ویپرویو (Sunset Vaporwave)',
      accent: '#f59e0b',
      accentGlow: '0 0 18px rgba(245, 158, 11, 0.5)',
      accentSoft: 'rgba(245, 158, 11, 0.16)',
      border: 'rgba(245, 158, 11, 0.28)',
      bg: '#140c06',
      bgGradient: 'radial-gradient(ellipse at 50% 0%, #2e1709 0%, #0c0703 75%)',
      sidebar: '#0a0502',
      card: '#24140b',
      cardBorder: 'rgba(245, 158, 11, 0.25)',
      composerBg: 'rgba(32, 18, 9, 0.95)',
      text: '#fffbeb'
    },
    clean_dark: {
      name: '⚪️ دارک اسلیت مدرن (Modern Dark Slate)',
      accent: '#38bdf8',
      accentGlow: '0 0 12px rgba(56, 189, 248, 0.35)',
      accentSoft: 'rgba(56, 189, 248, 0.12)',
      border: 'rgba(255, 255, 255, 0.14)',
      bg: '#111318',
      bgGradient: 'radial-gradient(ellipse at 50% 0%, #1a1e26 0%, #0e1014 70%)',
      sidebar: '#0c0e12',
      card: '#181b22',
      cardBorder: 'rgba(255, 255, 255, 0.12)',
      composerBg: 'rgba(24, 27, 34, 0.94)',
      text: '#f8fafc'
    }
  };

  const DEFAULT_SETTINGS = {
    theme: 'cyber',
    fontFa: 'Vazirmatn',
    fontEn: 'Outfit',
    strokeMode: 'glow',
    fontSize: 14.5,
    rtlAuto: true
  };

  function loadSettings() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      return { ...DEFAULT_SETTINGS, ...saved };
    } catch (e) {
      return DEFAULT_SETTINGS;
    }
  }

  function saveSettings(patch) {
    const current = loadSettings();
    const updated = { ...current, ...patch };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    } catch (e) {}
    applyThemeAndFont();
    return updated;
  }

  // 2. Dynamic Style Injection Engine
  let dynamicStyleEl = document.getElementById('agy-dynamic-theme-style');
  if (!dynamicStyleEl) {
    dynamicStyleEl = document.createElement('style');
    dynamicStyleEl.id = 'agy-dynamic-theme-style';
    (document.head || document.documentElement).appendChild(dynamicStyleEl);
  }

  function applyThemeAndFont() {
    const s = loadSettings();
    const t = THEMES[s.theme] || THEMES.cyber;

    const fontEnPart = (s.fontEn && s.fontEn !== 'system') ? `'${s.fontEn}', ` : '';
    const fontFaPart = (s.fontFa && s.fontFa !== 'system') ? `'${s.fontFa}', ` : "'Vazirmatn', ";
    const combinedFont = `${fontEnPart}${fontFaPart}-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`;

    const glowShadow = s.strokeMode === 'glow' ? t.accentGlow : (s.strokeMode === 'refined' ? `0 0 10px ${t.accentSoft}` : 'none');
    const glowBorder = s.strokeMode === 'glow' ? t.accent : t.border;

    dynamicStyleEl.textContent = `
      :root {
        --cpe-font: ${combinedFont};
        --cpe-font-size: ${s.fontSize}px;
        --cpe-accent: ${t.accent};
        --cpe-accent-glow: ${t.accentGlow};
        --cpe-border: ${t.border};
        --vscode-editor-background: ${t.bg} !important;
        --vscode-sideBar-background: ${t.sidebar} !important;
        --vscode-activityBar-background: ${t.sidebar} !important;
        --vscode-titleBar-activeBackground: ${t.sidebar} !important;
        --vscode-statusBar-background: ${t.sidebar} !important;
        --vscode-tab-activeBackground: ${t.card} !important;
        --vscode-tab-inactiveBackground: ${t.sidebar} !important;
        --vscode-focusBorder: ${t.accent} !important;
        --vscode-button-background: ${t.accent} !important;
        --vscode-button-foreground: #000000 !important;
        --vscode-button-hoverBackground: ${t.accent} !important;
      }

      /* Universal Font Override */
      body,
      .monaco-workbench,
      .monaco-shell,
      .part,
      .part.titlebar,
      .part.sidebar,
      .part.activitybar,
      .part.statusbar,
      .action-label,
      .label-name,
      .quick-input-widget,
      .font-sans,
      [class*="font-sans"],
      [class*="chat"],
      [class*="agent"],
      [class*="jetski"] {
        font-family: var(--cpe-font) !important;
      }

      /* 1. Workbench Deep Theming & Neon Gradients */
      .monaco-workbench {
        background: ${t.bg} !important;
        background-image: ${t.bgGradient} !important;
      }

      .monaco-workbench .part.editor {
        background: ${t.bg} !important;
        background-image: ${t.bgGradient} !important;
      }

      .monaco-workbench .part.sidebar,
      .monaco-workbench .part.activitybar,
      .monaco-workbench .part.titlebar,
      .monaco-workbench .part.statusbar {
        background-color: ${t.sidebar} !important;
      }

      .monaco-workbench .part.sidebar {
        border-right: 1px solid ${t.border} !important;
      }

      .monaco-workbench .part.titlebar {
        border-bottom: 1px solid ${t.border} !important;
      }

      .monaco-workbench .part.statusbar {
        border-top: 1px solid ${t.border} !important;
      }

      /* 2. Welcome Screen / Getting Started Glow (Open Folder, etc.) */
      .gettingStartedContainer,
      .gettingStartedSlideDetails,
      .welcome-page {
        background: transparent !important;
      }

      .monaco-button,
      .monaco-text-button,
      button.getting-started-action {
        background: ${t.accent} !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: 1px solid ${t.accent} !important;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4), ${glowShadow} !important;
        transition: all 0.2s ease !important;
      }

      .monaco-button:hover,
      .monaco-text-button:hover {
        box-shadow: 0 6px 26px rgba(0, 0, 0, 0.6), ${t.accentGlow} !important;
        transform: translateY(-1px) !important;
      }

      .monaco-button.secondary,
      .monaco-text-button.secondary {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid ${t.border} !important;
        border-radius: 12px !important;
      }

      .monaco-button.secondary:hover {
        border-color: ${t.accent} !important;
        color: ${t.accent} !important;
        box-shadow: ${t.accentGlow} !important;
      }

      .getting-started-category,
      .welcome-card,
      [class*="workspace-item"],
      [class*="extension-card"] {
        background: ${t.card} !important;
        border: 1px solid ${t.cardBorder} !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
      }

      /* 3. Editor Tabs with Neon Glow */
      .tabs-container .tab {
        border-radius: 10px 10px 0 0 !important;
        border: 1px solid transparent !important;
        transition: all 0.18s ease !important;
      }

      .tabs-container .tab.active {
        background: ${t.card} !important;
        border: 1px solid ${t.cardBorder} !important;
        border-bottom: 2px solid ${t.accent} !important;
        box-shadow: 0 -2px 14px rgba(0, 0, 0, 0.4), ${glowShadow} !important;
      }

      /* 4. Monaco Editor & Selection Glow */
      .monaco-editor,
      .monaco-editor-background {
        background: ${t.bg} !important;
      }

      .monaco-editor .cursor {
        background-color: ${t.accent} !important;
        box-shadow: 0 0 10px ${t.accent} !important;
      }

      ::selection {
        background: ${t.accent}40 !important;
        color: #ffffff !important;
      }

      /* 5. Agent Chat Panel (Jetski) Theming */
      .jetski-root,
      [class*="jetski"] {
        background: ${t.bg} !important;
      }

      div[class*="chat-input-container"],
      div[class*="_ComposerLayoutRoot_"],
      div[class*="composer-container"] {
        background: ${t.composerBg} !important;
        border: 1px solid ${glowBorder} !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), ${glowShadow} !important;
        backdrop-filter: blur(20px) !important;
      }

      div[class*="chat-input-container"]:focus-within,
      div[class*="_ComposerLayoutRoot_"]:focus-within {
        border-color: ${t.accent} !important;
        box-shadow: 0 0 0 1.5px ${t.accent}, 0 8px 36px rgba(0, 0, 0, 0.6), ${t.accentGlow} !important;
      }

      [data-message-author-role="user"] > div:first-child {
        background: ${t.card} !important;
        border: 1px solid ${t.cardBorder} !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
      }

      /* Quick Input / Command Palette */
      .quick-input-widget {
        border-radius: 16px !important;
        background: ${t.composerBg} !important;
        backdrop-filter: blur(28px) saturate(180%) !important;
        border: 1px solid ${t.border} !important;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.7), ${t.accentGlow} !important;
      }

      .quick-input-filter .monaco-inputbox {
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid ${t.border} !important;
      }

      .quick-input-filter .monaco-inputbox.synthetic-focus {
        border-color: ${t.accent} !important;
        box-shadow: ${t.accentGlow} !important;
      }

      /* 6. Floating Action HUD Pill */
      #agy-hud-pill {
        position: fixed;
        top: 8px;
        right: 140px;
        z-index: 999999;
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid ${t.border};
        border-radius: 9999px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), ${t.accentGlow};
        user-select: none;
        font-family: var(--cpe-font);
        transition: transform 0.15s ease, box-shadow 0.2s ease;
        cursor: grab;
      }

      #agy-hud-pill:hover {
        border-color: ${t.accent};
        box-shadow: 0 10px 36px rgba(0, 0, 0, 0.75), ${t.accentGlow};
      }

      #agy-hud-pill:active {
        cursor: grabbing;
      }

      .agy-hud-btn {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 9999px;
        color: #f1f5f9;
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.16s ease;
        font-family: inherit;
      }

      .agy-hud-btn:hover {
        background: ${t.accentSoft};
        color: ${t.accent};
        border-color: ${t.accent};
        transform: scale(1.04);
      }

      /* Modal Dialog */
      .agy-modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        z-index: 1000000;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s ease;
        font-family: var(--cpe-font);
        direction: rtl;
      }

      .agy-modal-overlay.agy-open {
        opacity: 1;
        pointer-events: auto;
      }

      .agy-modal-sheet {
        width: 540px;
        max-width: 94vw;
        max-height: 88vh;
        overflow-y: auto;
        background: #0f172a;
        border: 1px solid ${t.border};
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), ${t.accentGlow};
        color: #f8fafc;
        transform: scale(0.96);
        transition: transform 0.2s ease;
      }

      .agy-modal-overlay.agy-open .agy-modal-sheet {
        transform: scale(1);
      }

      #agy-toast {
        position: fixed;
        bottom: 32px;
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid ${t.border};
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), ${t.accentGlow};
        color: #f8fafc;
        padding: 9px 20px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
        z-index: 1000002;
        opacity: 0;
        pointer-events: none;
        transition: all 0.25s ease;
        font-family: var(--cpe-font);
        direction: rtl;
      }

      #agy-toast.agy-toast-show {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
      }
    `;
  }

  // 3. Process Monaco Editor Lines (Smart BiDi)
  function processMonacoLine(line) {
    if (!line || line.nodeType !== 1) return;
    if (!line.classList || !line.classList.contains('view-line')) return;
    const text = line.textContent || '';
    if (!text.trim()) return;

    if (PERSIAN_REGEX.test(text)) {
      if (!line.classList.contains('bidi-rtl-line')) {
        line.classList.add('bidi-rtl-line');
        line.classList.remove('bidi-ltr-line');
        line.setAttribute('dir', 'rtl');
        line.style.setProperty('direction', 'rtl', 'important');
        line.style.setProperty('text-align', 'right', 'important');
        line.style.setProperty('width', 'calc(100% - 24px)', 'important');
        line.style.setProperty('font-family', "'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', sans-serif", 'important');
      }
    } else {
      if (!line.classList.contains('bidi-ltr-line')) {
        line.classList.add('bidi-ltr-line');
        line.classList.remove('bidi-rtl-line');
        line.setAttribute('dir', 'ltr');
        line.style.removeProperty('direction');
        line.style.removeProperty('text-align');
        line.style.removeProperty('width');
        line.style.removeProperty('font-family');
      }
    }
  }

  // 4. Process Chat & Markdown elements
  function processElement(el) {
    if (!el || el.nodeType !== 1) return;
    const tag = el.tagName.toLowerCase();
    if (tag === 'pre' || tag === 'code' || tag === 'script' || tag === 'style') return;
    if (el.classList && (el.classList.contains('terminal') || el.classList.contains('katex') || el.classList.contains('xterm'))) return;

    if (el.classList && el.classList.contains('view-line')) {
      processMonacoLine(el);
      return;
    }

    if (['p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'div', 'span', 'textarea'].includes(tag)) {
      const text = el.innerText || el.textContent || '';
      if (text.length > 1 && PERSIAN_REGEX.test(text)) {
        if (!el.classList.contains('bidi-rtl')) {
          el.classList.add('bidi-rtl');
          el.setAttribute('dir', 'rtl');
          el.style.setProperty('direction', 'rtl', 'important');
          el.style.setProperty('text-align', 'right', 'important');
          el.style.setProperty('font-family', "'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', sans-serif", 'important');
        }
      }
    }
  }

  function scanAll(root = document.body) {
    if (!root) return;
    const lines = root.querySelectorAll('.view-lines .view-line');
    for (let i = 0; i < lines.length; i++) {
      processMonacoLine(lines[i]);
    }

    const blocks = root.querySelectorAll('.rendered-markdown p, .rendered-markdown li, [class*="chat"] p, [class*="message"] p, [class*="turn"] p, .prose p, .prose li');
    for (let i = 0; i < blocks.length; i++) {
      processElement(blocks[i]);
    }
  }

  // 5. Toast System
  function showToast(msg) {
    let t = document.getElementById('agy-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'agy-toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add('agy-toast-show');
    setTimeout(() => {
      t.classList.remove('agy-toast-show');
    }, 2800);
  }

  // 6. Modal Factory
  function createModal(id, title, bodyHtml) {
    let m = document.getElementById(id);
    if (m) m.remove();

    m = document.createElement('div');
    m.id = id;
    m.className = 'agy-modal-overlay';
    m.innerHTML = `
      <div class="agy-modal-sheet">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.12); padding-bottom: 14px;">
          <h3 style="margin: 0; font-size: 16px; font-weight: 700; color: #fff;">${title}</h3>
          <button class="agy-modal-close" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center;">✕</button>
        </div>
        <div class="agy-modal-body">
          ${bodyHtml}
        </div>
      </div>
    `;

    document.body.appendChild(m);

    m.querySelector('.agy-modal-close').onclick = () => m.classList.remove('agy-open');
    m.onclick = (e) => {
      if (e.target === m) m.classList.remove('agy-open');
    };
    return m;
  }

  // 7. Theme & Neon Customizer Modal
  function openThemeModal() {
    const s = loadSettings();

    const themesList = [
      { id: 'cyber', label: '⚡️ سایبرپانک نئون (Cyan Neon - فیروزه‌ای درخشان)' },
      { id: 'synthwave', label: '💜 سینت‌ویو ۸۴ (SynthWave - سرخابی نئونی و بنفش)' },
      { id: 'amoled', label: '🖤 آمولد بلک و شیشه‌ای (Pure AMOLED & Glass)' },
      { id: 'midnight', label: '🌌 میدنایت ایندیگو (Midnight Indigo - سرمه‌ای نیلی)' },
      { id: 'emerald', label: '🟢 ماتریکس زمردی (Emerald Matrix - سبز نئونی)' },
      { id: 'sunset', label: '🌅 سان‌ست ویپرویو (Sunset Vaporwave - طلایی و کهربایی)' },
      { id: 'clean_dark', label: '⚪️ دارک اسلیت مدرن (Modern Dark Slate)' }
    ];

    const fontsFa = [
      { id: 'Vazirmatn', label: 'وزیرمتن (Vazirmatn - استاندارد و مدرن)' },
      { id: 'Estedad', label: 'استعداد (Estedad - هندسی و پویا)' },
      { id: 'Vazir', label: 'وزیر کلاسیک (Vazir)' },
      { id: 'system', label: 'فونت پیش‌فرض سیستم' }
    ];

    const fontsEn = [
      { id: 'Outfit', label: 'Outfit (مدرن و تمیز - توصیه شده)' },
      { id: 'JetBrains Mono', label: 'JetBrains Mono (تک‌فاصله برنامه‌نویسی)' },
      { id: 'Consolas', label: 'Consolas (کلاسیک ویندوز)' },
      { id: 'Cascadia Code', label: 'Cascadia Code' }
    ];

    const strokeModes = [
      { id: 'glow', label: '🌟 درخشش نئونی کامل و خیره‌کننده (High Neon Glow)' },
      { id: 'refined', label: '💎 کادربندی شیشه‌ای و نئون ملایم (Refined Glass Glow)' },
      { id: 'subtle', label: '▫️ حالت مینیمال و خطی (Subtle 1px)' }
    ];

    const html = `
      <div style="margin-bottom: 14px;">
        <label style="display: block; font-size: 12px; color: #94a3b8; margin-bottom: 6px;">🎨 انتخاب پالت رنگ و تم Antigravity:</label>
        <select id="agy-sel-theme" style="width: 100%; padding: 10px; border-radius: 10px; background: #1e293b; color: #fff; border: 1px solid rgba(255,255,255,0.18); font-family: inherit;">
          ${themesList.map(t => `<option value="${t.id}" ${s.theme === t.id ? 'selected' : ''}>${t.label}</option>`).join('')}
        </select>
      </div>

      <div style="margin-bottom: 14px;">
        <label style="display: block; font-size: 12px; color: #94a3b8; margin-bottom: 6px;">💫 شدت روشنایی نئون و کادر (Neon Glow Effect):</label>
        <select id="agy-sel-stroke" style="width: 100%; padding: 10px; border-radius: 10px; background: #1e293b; color: #fff; border: 1px solid rgba(255,255,255,0.18); font-family: inherit;">
          ${strokeModes.map(m => `<option value="${m.id}" ${s.strokeMode === m.id ? 'selected' : ''}>${m.label}</option>`).join('')}
        </select>
      </div>

      <div style="margin-bottom: 14px;">
        <label style="display: block; font-size: 12px; color: #94a3b8; margin-bottom: 6px;">✍️ انتخاب فونت فارسی (آفلاین WOFF2):</label>
        <select id="agy-sel-font-fa" style="width: 100%; padding: 10px; border-radius: 10px; background: #1e293b; color: #fff; border: 1px solid rgba(255,255,255,0.18); font-family: inherit;">
          ${fontsFa.map(f => `<option value="${f.id}" ${s.fontFa === f.id ? 'selected' : ''}>${f.label}</option>`).join('')}
        </select>
      </div>

      <div style="margin-bottom: 14px;">
        <label style="display: block; font-size: 12px; color: #94a3b8; margin-bottom: 6px;">🔤 انتخاب فونت انگلیسی و رابط کاربری:</label>
        <select id="agy-sel-font-en" style="width: 100%; padding: 10px; border-radius: 10px; background: #1e293b; color: #fff; border: 1px solid rgba(255,255,255,0.18); font-family: inherit;">
          ${fontsEn.map(f => `<option value="${f.id}" ${s.fontEn === f.id ? 'selected' : ''}>${f.label}</option>`).join('')}
        </select>
      </div>

      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; margin-bottom: 6px;">
          <span>📏 اندازه فونت (Font Size):</span>
          <span id="agy-val-font-size" style="color: #00f0ff; font-weight: 700;">${s.fontSize}px</span>
        </div>
        <input type="range" id="agy-rng-font-size" min="13" max="18" step="0.5" value="${s.fontSize}" style="width: 100%; accent-color: #00f0ff; cursor: pointer;">
      </div>

      <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 12px; margin-bottom: 20px;">
        <span style="font-size: 13px;">↔️ راست‌چین‌سازی خودکار متن فارسی (Smart BiDi):</span>
        <input type="checkbox" id="agy-chk-rtl" ${s.rtlAuto ? 'checked' : ''} style="width: 18px; height: 18px; cursor: pointer; accent-color: #00f0ff;">
      </div>

      <button id="agy-btn-save-theme" style="width: 100%; padding: 12px; background: #00f0ff; color: #000; font-weight: 700; border: none; border-radius: 12px; cursor: pointer; font-size: 14px; font-family: inherit; box-shadow: 0 0 16px rgba(0, 240, 255, 0.45); transition: all 0.2s ease;">
        ذخیره و اعمال فوری
      </button>
    `;

    const modal = createModal('agy-modal-theme', '🎨 تنظیمات تم رنگی، نئون و فونت Antigravity IDE', html);
    modal.classList.add('agy-open');

    const rng = document.getElementById('agy-rng-font-size');
    const valLbl = document.getElementById('agy-val-font-size');
    if (rng && valLbl) {
      rng.oninput = () => { valLbl.textContent = `${rng.value}px`; };
    }

    document.getElementById('agy-btn-save-theme').onclick = () => {
      const theme = document.getElementById('agy-sel-theme').value;
      const strokeMode = document.getElementById('agy-sel-stroke').value;
      const fontFa = document.getElementById('agy-sel-font-fa').value;
      const fontEn = document.getElementById('agy-sel-font-en').value;
      const fontSize = parseFloat(document.getElementById('agy-rng-font-size').value);
      const rtlAuto = document.getElementById('agy-chk-rtl').checked;

      saveSettings({ theme, strokeMode, fontFa, fontEn, fontSize, rtlAuto });
      modal.classList.remove('agy-open');
      showToast('🎨 تم و جلوه‌های نئون با موفقیت اعمال شدند');
    };
  }

  // 8. Accounts Management Modal
  async function openAccountsModal() {
    const modal = createModal('agy-modal-account', '🔐 مدیریت حساب‌ها و سوییچر Antigravity', `
      <div style="padding: 12px 14px; background: rgba(0, 240, 255, 0.08); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 14px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #00f0ff; box-shadow: 0 0 10px #00f0ff;"></span>
          <span style="font-size: 12.5px; color: #cbd5e1;">وضعیت سوییچر خودکار:</span>
        </div>
        <span style="font-size: 12px; font-weight: 700; color: #00f0ff;">فعال و آماده</span>
      </div>

      <div style="font-size: 12.5px; color: #94a3b8; line-height: 1.7; margin-bottom: 16px;">
        برای جابه‌جایی سریع بین توکن‌ها، تخصیص سهمیه هوشمند و مدیریت اکانت‌ها می‌توانید پنل مدیریت را باز کنید:
      </div>

      <div style="display: flex; flex-direction: column; gap: 10px;">
        <button id="agy-btn-launch-gui" style="padding: 12px; background: #00f0ff; color: #000; border: none; border-radius: 12px; font-weight: 700; font-size: 13px; cursor: pointer; font-family: inherit; box-shadow: 0 0 14px rgba(0, 240, 255, 0.35);">
          🚀 باز کردن پنل گرافیکی سوییچر اکانت (GUI)
        </button>
      </div>
    `);
    modal.classList.add('agy-open');

    document.getElementById('agy-btn-launch-gui').onclick = () => {
      window.open('http://127.0.0.1:39285', '_blank');
      showToast('🚀 پنل سوییچر باز شد');
      modal.classList.remove('agy-open');
    };
  }

  // 9. Floating Draggable Action HUD Pill
  function renderHUD() {
    if (window !== window.top) return; // Only show on top workbench window

    let hud = document.getElementById('agy-hud-pill');
    if (hud) hud.remove();

    hud = document.createElement('div');
    hud.id = 'agy-hud-pill';

    hud.innerHTML = `
      <span id="agy-hud-drag-handle" style="cursor: grab; display: flex; align-items: center; gap: 5px; padding: 2px 4px; user-select: none;" title="برای جابه‌جایی نوار، اینجا را بگیرید و بکشید">
        <span style="font-size: 12px; color: rgba(255,255,255,0.45); font-family: monospace;">⠿</span>
        <span style="width: 7px; height: 7px; border-radius: 50%; background: #00f0ff; box-shadow: 0 0 8px #00f0ff;"></span>
        <span style="font-size: 11px; font-weight: 700; color: #00f0ff; letter-spacing: 0.5px;">AGY Pro</span>
      </span>
      <button class="agy-hud-btn" id="agy-btn-theme" title="تنظیمات تم رنگی، درخشش نئون و فونت‌ها">
        🎨 <span>تم و نئون</span>
      </button>
      <button class="agy-hud-btn" id="agy-btn-accounts" title="مدیریت و سوئیچ بین اکانت‌ها">
        🔄 <span>اکانت‌ها</span>
      </button>
    `;

    document.body.appendChild(hud);

    // Restore saved position
    try {
      const savedPos = JSON.parse(localStorage.getItem('agy_hud_pill_pos') || 'null');
      if (savedPos && typeof savedPos.x === 'number') {
        const maxX = Math.max(10, window.innerWidth - 320);
        const maxY = Math.max(10, window.innerHeight - 50);
        hud.style.left = `${Math.min(Math.max(10, savedPos.x), maxX)}px`;
        hud.style.top = `${Math.min(Math.max(6, savedPos.y), maxY)}px`;
        hud.style.right = 'auto';
      }
    } catch(e) {}

    // Dragging Logic
    let isDragging = false;
    let startX = 0, startY = 0;
    let initialLeft = 0, initialTop = 0;

    hud.addEventListener('mousedown', (e) => {
      if (e.target.closest('button') || e.target.closest('.agy-hud-btn')) return;
      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      const rect = hud.getBoundingClientRect();
      initialLeft = rect.left;
      initialTop = rect.top;

      hud.style.transition = 'none';
      hud.style.cursor = 'grabbing';
      document.body.style.userSelect = 'none';

      const onMouseMove = (ev) => {
        if (!isDragging) return;
        const dx = ev.clientX - startX;
        const dy = ev.clientY - startY;

        let newX = initialLeft + dx;
        let newY = initialTop + dy;

        const maxX = window.innerWidth - hud.offsetWidth - 10;
        const maxY = window.innerHeight - hud.offsetHeight - 10;
        hud.style.left = `${Math.max(10, Math.min(newX, maxX))}px`;
        hud.style.top = `${Math.max(6, Math.min(newY, maxY))}px`;
        hud.style.right = 'auto';
      };

      const onMouseUp = () => {
        if (!isDragging) return;
        isDragging = false;
        hud.style.transition = 'box-shadow 0.2s ease';
        hud.style.cursor = 'grab';
        document.body.style.userSelect = '';
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);

        const finalRect = hud.getBoundingClientRect();
        try {
          localStorage.setItem('agy_hud_pill_pos', JSON.stringify({ x: finalRect.left, y: finalRect.top }));
        } catch(e) {}
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });

    // Buttons
    document.getElementById('agy-btn-theme').onclick = () => openThemeModal();
    document.getElementById('agy-btn-accounts').onclick = () => openAccountsModal();
  }

  // 10. Initialization & Observers
  applyThemeAndFont();

  const observer = new MutationObserver(mutations => {
    for (const m of mutations) {
      if (m.target && m.target.nodeType === 1 && m.target.classList && m.target.classList.contains('view-line')) {
        processMonacoLine(m.target);
      }
      for (const node of m.addedNodes) {
        if (node.nodeType === 1) {
          if (node.classList && node.classList.contains('view-line')) {
            processMonacoLine(node);
          } else {
            const nestedLines = node.querySelectorAll ? node.querySelectorAll('.view-line') : [];
            for (let i = 0; i < nestedLines.length; i++) {
              processMonacoLine(nestedLines[i]);
            }
          }
          processElement(node);
        }
      }
    }
  });

  const startAll = () => {
    applyThemeAndFont();
    renderHUD();
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    scanAll(document.body);
    setInterval(() => {
      scanAll(document.body);
    }, 300);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startAll, { once: true });
  } else {
    startAll();
  }
})();
"""
    enhancer_path = wb_dir / "antigravity-ide-enhancer.js"
    enhancer_path.write_text(enhancer_js, encoding="utf-8")
    print(f"✓ Created {enhancer_path.name}")

    # 4. Patch workbench.desktop.main.css
    wb_css_path = wb_dir / "workbench.desktop.main.css"
    if wb_css_path.exists():
        wb_css_content = wb_css_path.read_text(encoding="utf-8")
        import_stmt = "@import url('./antigravity-custom-theme.css');\n"
        if import_stmt not in wb_css_content:
            bak = wb_css_path.with_suffix(".css.bak")
            if not bak.exists():
                shutil.copy2(wb_css_path, bak)
            wb_css_path.write_text(import_stmt + wb_css_content, encoding="utf-8")
            print("✓ Injected theme import into workbench.desktop.main.css")
        else:
            print("✓ workbench.desktop.main.css already includes custom theme import")

    # 5. Patch jetskiMain.tailwind.css
    jetski_css_path = out_dir / "jetskiMain.tailwind.css"
    if jetski_css_path.exists():
        jetski_css = jetski_css_path.read_text(encoding="utf-8")
        import_stmt_jetski = "@import url('./vs/workbench/antigravity-custom-theme.css');\n"
        if import_stmt_jetski not in jetski_css:
            bak = jetski_css_path.with_suffix(".css.bak")
            if not bak.exists():
                shutil.copy2(jetski_css_path, bak)
            jetski_css_path.write_text(import_stmt_jetski + jetski_css, encoding="utf-8")
            print("✓ Injected theme import into jetskiMain.tailwind.css")
        else:
            print("✓ jetskiMain.tailwind.css already includes custom theme import")

    # 6. Patch workbench.html & workbench-jetski-agent.html
    html_files = [
        out_dir / "vs" / "code" / "electron-browser" / "workbench" / "workbench.html",
        out_dir / "vs" / "code" / "electron-browser" / "workbench" / "workbench-jetski-agent.html"
    ]

    for html_path in html_files:
        if not html_path.exists():
            continue
        content = html_path.read_text(encoding="utf-8")
        bak = html_path.with_suffix(".html.bak")
        if not bak.exists():
            shutil.copy2(html_path, bak)

        # 6a. Update CSP to permit data: and fonts.jsdelivr
        if "font-src" in content and "data:" not in content.split("font-src")[1].split(";")[0]:
            content = content.replace("font-src\n\t\t\t\t\t'self'", "font-src\n\t\t\t\t\t'self'\n\t\t\t\t\tdata:\n\t\t\t\t\thttps://cdn.jsdelivr.net")

        # 6b. Add link to stylesheet if not present
        link_tag = '\t<link rel="stylesheet" href="../../../workbench/antigravity-custom-theme.css">\n'
        if "antigravity-custom-theme.css" not in content:
            content = content.replace("</head>", f"{link_tag}</head>")

        # 6c. Add script tag if not present
        script_tag = '<script src="../../../workbench/antigravity-ide-enhancer.js" type="module"></script>\n'
        if "antigravity-ide-enhancer.js" not in content:
            content = content.replace("</html>", f"{script_tag}</html>")

        html_path.write_text(content, encoding="utf-8")
        print(f"✓ Patched {html_path.name}")

    # 7. Update product.json Checksums
    prod_file = IDE_APP_DIR / "product.json"
    if prod_file.exists():
        with open(prod_file, "r", encoding="utf-8") as f:
            prod_data = json.load(f)

        checksums = prod_data.get("checksums", {})
        tracked_keys = [
            "vs/workbench/workbench.desktop.main.css",
            "vs/code/electron-browser/workbench/workbench.html",
            "vs/code/electron-browser/workbench/workbench-jetski-agent.html",
            "jetskiMain.tailwind.css"
        ]

        updated_count = 0
        for rel in tracked_keys:
            target = out_dir / rel
            if target.exists():
                new_sum = compute_checksum(target)
                if checksums.get(rel) != new_sum:
                    checksums[rel] = new_sum
                    updated_count += 1

        prod_data["checksums"] = checksums
        bak_prod = prod_file.with_suffix(".json.bak")
        if not bak_prod.exists():
            shutil.copy2(prod_file, bak_prod)

        with open(prod_file, "w", encoding="utf-8") as f:
            json.dump(prod_data, f, indent=4)
        print(f"✓ Updated product.json checksums ({updated_count} hashes updated) - ZERO corruption warnings!")

    # 8. Update User settings.json with optimal font and markdown configurations
    if IDE_USER_SETTINGS.parent.exists():
        settings = {}
        if IDE_USER_SETTINGS.exists():
            try:
                with open(IDE_USER_SETTINGS, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            except Exception:
                settings = {}

        # Universal Editor settings
        settings["editor.fontFamily"] = "Consolas, 'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', 'JetBrains Mono', monospace"
        settings["editor.fontLigatures"] = True
        settings["editor.fontSize"] = 14.5
        settings["editor.lineHeight"] = 1.65
        settings["editor.unicodeHighlight.nonBasicASCII"] = False

        # Dedicated Markdown settings
        settings["[markdown]"] = {
            "editor.fontFamily": "'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', 'Outfit', sans-serif",
            "editor.fontSize": 15.5,
            "editor.lineHeight": 28,
            "editor.wordWrap": "on",
            "editor.quickSuggestions": {
                "comments": "off",
                "strings": "off",
                "other": "off"
            }
        }

        # Dedicated Plaintext settings
        settings["[plaintext]"] = {
            "editor.fontFamily": "'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', 'Outfit', sans-serif",
            "editor.fontSize": 15.5,
            "editor.lineHeight": 28,
            "editor.wordWrap": "on"
        }

        # Built-in Markdown Preview
        settings["markdown.preview.fontFamily"] = "'Vazirmatn', 'Vazirmatn UI', 'Vazir', 'Estedad', 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        settings["markdown.preview.fontSize"] = 15.5
        settings["markdown.preview.lineHeight"] = 1.85

        # Chat & Terminal settings
        settings["chat.editor.fontFamily"] = "'Outfit', 'Vazirmatn', 'Estedad', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        settings["chat.editor.fontSize"] = 14.5
        settings["terminal.integrated.fontFamily"] = "Consolas, 'Cascadia Code', monospace"
        settings["terminal.integrated.fontSize"] = 13.5

        IDE_USER_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
        with open(IDE_USER_SETTINGS, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        print("✓ Updated Antigravity IDE User settings.json with optimal font & Markdown configurations")

    print("=" * 60)
    print("✨ SUCCESS: Antigravity IDE design, Persian fonts, Neon Glow & Customizer suite PERMANENTLY installed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    setup_ide_theme()
