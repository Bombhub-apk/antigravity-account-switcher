/* ==========================================================================
   Antigravity Switcher & Migration Suite - Interactive Application Controller
   Author: Ethan Carter (https://github.com/Bombhub-apk/antigravity-account-switcher)
   Includes: Granular Project Selection, Scheduled Tasks Isolation, and Live Quota
   ========================================================================== */

let currentLang = 'en';
let state = {
  activeAccount: null,
  savedAccounts: {},
  conversations: [],
  projects: [],
  tasks: [],
  activeModalTab: 'projects',
  migration: {
    sourceAccount: null,
    targetAccount: null,
    mode: 'copy',
    structure: 'separate',
    dualSync: false,
    selectedIds: new Set(),
    selectedProjectId: ''
  }
};

// Initializer
document.addEventListener('DOMContentLoaded', () => {
  detectInitialLanguage();
  initApplication();
  startCountdownTicker();
});

function detectInitialLanguage() {
  const saved = localStorage.getItem('agy_switcher_lang');
  if (saved && translations[saved]) {
    currentLang = saved;
  } else {
    currentLang = 'en'; // Default English
  }
  const langSelect = document.getElementById('langSelect');
  if (langSelect) langSelect.value = currentLang;
  applyTranslations();
}

function changeLanguage(lang) {
  if (!translations[lang]) return;
  currentLang = lang;
  localStorage.setItem('agy_switcher_lang', lang);
  applyTranslations();
  renderAll();
  if (document.getElementById('migrationModal')?.classList.contains('active')) {
    renderProjectList();
    renderTaskList();
    renderConversationPicker();
  }
}

function applyTranslations() {
  const tObj = translations[currentLang] || translations.en;
  document.documentElement.lang = currentLang;
  document.documentElement.dir = tObj.dir;
  document.body.style.fontFamily = tObj.font;

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (tObj[key]) {
      el.innerText = tObj[key];
    }
  });

  const searchInput = document.getElementById('convSearchInput');
  if (searchInput && tObj.searchPlaceholder) {
    searchInput.placeholder = tObj.searchPlaceholder;
  }
}

function t(key) {
  return (translations[currentLang] && translations[currentLang][key]) || (translations.en && translations.en[key]) || key;
}

// Data Fetching & Sync
async function initApplication() {
  try {
    if (window.INITIAL_PAYLOAD) {
      handlePayload(window.INITIAL_PAYLOAD);
      return;
    }

    const res = await fetch('/api/state').then(r => r.json()).catch(() => null);
    if (res) {
      handlePayload(res);
      return;
    }

    loadFallbackData();
  } catch (err) {
    loadFallbackData();
  }
}

function handlePayload(data) {
  state.activeAccount = data.activeAccount;
  state.savedAccounts = data.savedAccounts || {};
  state.conversations = data.conversations || [];
  state.projects = data.projects || [];
  state.tasks = data.tasks || [];
  state.runningInstances = data.runningInstances || [];
  state.runningAccounts = data.runningAccounts || {};
  renderAll();
}

function getSecondaryAccountEmail() {
  const keys = Object.keys(state.savedAccounts || {});
  const activeEmail = state.activeAccount ? state.activeAccount.email : null;
  const secondary = keys.find(k => k !== activeEmail);
  return secondary || 'secondary@example.com';
}

function getPrimaryAccountEmail() {
  const keys = Object.keys(state.savedAccounts || {});
  return (state.activeAccount && state.activeAccount.email) || keys[0] || 'primary@example.com';
}

function isAccount2(accountStr) {
  if (!accountStr) return false;
  const lower = String(accountStr).toLowerCase();
  const secondary = getSecondaryAccountEmail().toLowerCase();
  return lower.includes('instance2') || lower.includes('instance_2') || lower === secondary || (state.activeAccount && state.activeAccount.instanceId === 'instance_2');
}

function loadFallbackData() {
  state.activeAccount = {
    email: "developer@example.com",
    name: "Developer",
    avatar: "https://lh3.googleusercontent.com/a/default-user=s96-c",
    tier: "Google AI Pro",
    tier_code: "pro",
    session: {
      name: "Gemini 3.8 Flash High",
      used_pct: 34.1,
      remaining_pct: 65.9,
      resets_in: "57 min",
      reset_time: "07:27 PM",
      reset_secs: 3421,
      reset_iso: new Date(Date.now() + 57 * 60 * 1000).toISOString()
    },
    pools: [
      { name: "Gemini 3.8 Flash High", used_pct: 34.1, remaining_pct: 65.9, resets_in: "57 min", reset_secs: 3421 },
      { name: "Gemini 3.1 Pro", used_pct: 34.1, remaining_pct: 65.9, resets_in: "57 min", reset_secs: 3421 },
      { name: "Claude Sonnet 4.6", used_pct: 0.0, remaining_pct: 100.0, resets_in: "4 hr 59 min", reset_secs: 17900 },
      { name: "GPT-OSS 120B", used_pct: 0.0, remaining_pct: 100.0, resets_in: "4 hr 59 min", reset_secs: 17900 }
    ]
  };

  state.savedAccounts = {
    "developer@example.com": {
      email: "developer@example.com",
      label: "Developer (Primary)",
      tier: "Google AI Pro",
      tier_code: "pro",
      remaining_pct: 65.9,
      saved_at: "2026-09-10 18:00"
    },
    "secondary@example.com": {
      email: "secondary@example.com",
      label: "Collaborator (Secondary)",
      tier: "Google AI Pro",
      tier_code: "pro",
      remaining_pct: 100.0,
      saved_at: "2026-09-19 14:00"
    }
  };

  state.projects = [
    {
      id: "38a862ea-ade2-428a-b094-ff969a0e51c1",
      name: "gravity switch account",
      path: "C:\\Workspace\\gravity-switch-account",
      assigned_accounts: ["developer@example.com", "secondary@example.com"],
      conversation_count: 7,
      is_instance1_enabled: true,
      is_instance2_enabled: true,
      is_shared: true
    },
    {
      id: "e167f592-94ff-4339-ab32-d7bed0159a57",
      name: "SEO Automation Agent",
      path: "C:\\Workspace\\seo-automation-agent",
      assigned_accounts: ["developer@example.com"],
      conversation_count: 5,
      is_instance1_enabled: true,
      is_instance2_enabled: false,
      is_shared: false
    }
  ];

  state.tasks = [
    {
      name: "DailySEOAgent",
      owner_account: "developer@example.com",
      status: "Ready",
      enabled: true,
      isolated_from_account2: true,
      allowed_instances: ["instance_1"],
      next_run: "20/09/2026 12:30:00",
      description: "Daily SEO Agent Runner (12:30 PM)"
    },
    {
      name: "AntigravityQuotaMonitor",
      owner_account: "shared",
      status: "Ready",
      enabled: true,
      isolated_from_account2: false,
      allowed_instances: ["instance_1", "instance_2"],
      next_run: "N/A",
      description: "Real-time Multi-Instance Quota Auto-Sync Daemon"
    }
  ];

  renderAll();
}

// Native Bridge Call
function callNative(action, payload = {}) {
  const req = { action, payload, timestamp: Date.now() };

  if (window.chrome && window.chrome.webview) {
    window.chrome.webview.postMessage(req);
    return;
  }

  if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.nativeBridge) {
    window.webkit.messageHandlers.nativeBridge.postMessage(req);
    return;
  }

  fetch('/api/' + action, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).catch(() => {
    console.log("Native bridge called:", action, payload);
  });
}

// Main Render Dispatcher
function renderAll() {
  renderActiveAccount();
  renderDualInstanceControls();
  renderSavedAccounts();
}

function renderDualInstanceControls() {
  const select = document.getElementById('dualTargetAccountSelect');
  if (!select) return;
  select.innerHTML = '';

  const activeEmail = (state.activeAccount && state.activeAccount.email) || '';
  const entries = Object.entries(state.savedAccounts || {});
  const secondaries = entries.filter(([k, acc]) => (acc.email || k) !== activeEmail);

  const btn = document.getElementById('launchDualBtn');

  if (secondaries.length === 0) {
    const opt = document.createElement('option');
    opt.value = '';
    opt.innerText = t('noSavedAccounts');
    select.appendChild(opt);
    if (btn) btn.disabled = true;
    return;
  }

  if (btn) btn.disabled = false;

  secondaries.forEach(([k, acc]) => {
    const opt = document.createElement('option');
    opt.value = k;
    opt.innerText = `${acc.label || acc.email || k} (${acc.tier || 'PRO'})`;
    select.appendChild(opt);
  });
}

async function executeLaunchDual(accountKey) {
  let target = accountKey;
  if (!target) {
    const select = document.getElementById('dualTargetAccountSelect');
    target = select ? select.value : '';
  }
  if (!target) {
    alert(t('noSavedAccounts'));
    return;
  }

  const btn = document.getElementById('launchDualBtn');
  const originalText = btn ? btn.innerHTML : '';
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span>⏳</span> <span>${t('dualLaunching')}</span>`;
  }

  try {
    const res = await fetch('/api/launch_dual', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ accountKey: target })
    }).then(r => r.json());

    if (res && res.success) {
      alert(res.msg || t('dualLaunched'));
    } else {
      alert((res && res.error) || 'Failed to launch secondary instance');
    }
  } catch (e) {
    alert('Failed to connect to launcher service');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }
  }
}

function renderActiveAccount() {
  const acc = state.activeAccount;
  if (!acc) {
    document.getElementById('userName').innerText = t('noSavedAccounts');
    document.getElementById('userEmail').innerText = "";
    return;
  }

  document.getElementById('userName').innerText = acc.name || acc.email.split('@')[0];
  document.getElementById('userEmail').innerText = acc.email;

  const avatarImg = document.getElementById('userAvatar');
  const avatarPlaceholder = document.getElementById('userAvatarPlaceholder');
  if (acc.avatar) {
    avatarImg.src = acc.avatar;
    avatarImg.style.display = 'block';
    avatarPlaceholder.style.display = 'none';
  } else {
    avatarImg.style.display = 'none';
    avatarPlaceholder.style.display = 'flex';
    avatarPlaceholder.innerText = (acc.email[0] || 'A').toUpperCase();
  }

  const tierEl = document.getElementById('tierBadge');
  const tierCode = acc.tier_code || 'pro';
  tierEl.className = `tier-badge ${tierCode}`;
  tierEl.innerText = acc.tier || t('tierPro');

  const sess = acc.session || {};
  const used = sess.used_pct || 0;
  const rem = sess.remaining_pct !== undefined ? sess.remaining_pct : (100 - used);
  
  const fillEl = document.getElementById('quotaProgressFill');
  fillEl.style.width = Math.min(100, Math.max(0, used)) + '%';
  fillEl.className = 'liquid-progress-fill';
  if (used > 85) fillEl.classList.add('critical');
  else if (used > 60) fillEl.classList.add('warning');

  document.getElementById('quotaUsedText').innerText = `${used}% ${t('used')}`;
  document.getElementById('quotaRemainingText').innerText = `${rem}% ${t('remaining')}`;
  
  const countdownText = sess.resets_in && sess.resets_in !== 'N/A' 
    ? `⏱ ${t('resetsIn')} ${sess.resets_in}` 
    : t('noActiveLimit');
  document.getElementById('quotaCountdown').innerText = countdownText;

  const grid = document.getElementById('modelsGrid');
  grid.innerHTML = '';
  (acc.pools || []).forEach(p => {
    const chip = document.createElement('div');
    chip.className = 'model-chip';
    const pUsed = p.used_pct || 0;
    const pRem = p.remaining_pct !== undefined ? p.remaining_pct : (100 - pUsed);
    
    chip.innerHTML = `
      <div class="model-chip-name">${p.name}</div>
      <div class="model-bar">
        <div class="model-bar-fill" style="width: ${pUsed}%;"></div>
      </div>
      <div class="model-chip-status">
        <span style="color:var(--text-muted);">${pUsed}% ${t('used')}</span>
        <span style="color:var(--accent-cyan); font-weight:600;">${pRem}% ${t('remaining')}</span>
      </div>
    `;
    grid.appendChild(chip);
  });
}

function renderSavedAccounts() {
  const container = document.getElementById('savedAccountsList');
  container.innerHTML = '';

  const accounts = Object.entries(state.savedAccounts);
  document.getElementById('accountsCountBadge').innerText = accounts.length;

  if (accounts.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 24px; color:var(--text-muted); font-size:13px;">
        ${t('noSavedAccounts')}
      </div>
    `;
    return;
  }

  accounts.forEach(([key, acc]) => {
    const isActive = state.activeAccount && state.activeAccount.email === acc.email;
    const card = document.createElement('div');
    card.className = 'account-item-card';

    const tierCode = acc.tier_code || 'pro';
    const remPct = acc.remaining_pct !== undefined ? `${acc.remaining_pct}%` : '100%';

    card.innerHTML = `
      <div class="account-info">
        <div class="account-avatar-small">
          ${(acc.email[0] || 'G').toUpperCase()}
        </div>
        <div class="account-labels">
          <h4>
            <span>${acc.label || acc.email}</span>
            <span class="tier-badge ${tierCode}" style="font-size:9px; padding:2px 6px;">${acc.tier || 'PRO'}</span>
            ${isActive ? `<span class="tier-badge pro" style="font-size:9px; padding:2px 6px;">● ${t('activeBadge')}</span>` : ''}
          </h4>
          <p>${acc.email} • <span style="color:var(--accent-cyan); font-weight:600;">${remPct} ${t('remaining')}</span></p>
        </div>
      </div>

      <div class="account-actions">
        ${!isActive ? `
          <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px;" onclick="switchToAccount('${key}')">
            <span>⚡️</span>
            <span>${t('switchNow')}</span>
          </button>
          ${(() => {
            const runningAccs = Object.values(state.runningAccounts || {});
            const isRunning = runningAccs.includes(key) || (acc.email && runningAccs.includes(acc.email));
            return `
              <button class="btn btn-glass" style="padding: 6px 10px; font-size: 12px; background:${isRunning ? 'rgba(16,185,129,0.15)' : 'rgba(59,130,246,0.12)'}; border:1px solid ${isRunning ? 'rgba(16,185,129,0.4)' : 'rgba(59,130,246,0.3)'}; color:${isRunning ? '#34d399' : '#93c5fd'};" title="${isRunning ? (t('focusWindow') || 'Focus running window') : t('launchDualTitle')}" onclick="executeLaunchDual('${key}')">
                <span>${isRunning ? '🪟' : '⚡️ Window'}</span>
              </button>
            `;
          })()}
        ` : ''}

        <button class="btn btn-ghost-danger" style="padding: 6px 8px; font-size: 12px;" title="Delete" onclick="deleteAccount('${key}')">
          <span>🗑</span>
        </button>
      </div>
    `;

    container.appendChild(card);
  });
}

function switchToAccount(key) {
  callNative('switch', { accountKey: key });
  alert(`${t('switching')} ${key}\n${t('restartNotice')}`);
}

function saveCurrentAccount() {
  callNative('save', {});
  alert(t('accountSaved'));
}

function logoutAndAddNew() {
  callNative('logout', {});
}

function refreshLiveData() {
  callNative('refresh', {});
  initApplication();
}

function deleteAccount(key) {
  if (confirm(t('deleteConfirm'))) {
    callNative('delete', { accountKey: key });
    delete state.savedAccounts[key];
    renderSavedAccounts();
  }
}

// ==============================================================================
// MODAL & MIGRATION HUB LOGIC
// ==============================================================================

async function openMigrationModal(sourceAccountKey) {
  state.migration.sourceAccount = sourceAccountKey || (state.activeAccount ? state.activeAccount.email : null);
  
  const targetSelect = document.getElementById('modalTargetAccountSelect');
  if (targetSelect) {
    targetSelect.innerHTML = '';
    Object.keys(state.savedAccounts).forEach(key => {
      if (key !== state.migration.sourceAccount) {
        const opt = document.createElement('option');
        opt.value = key;
        opt.innerText = key;
        targetSelect.appendChild(opt);
      }
    });

    if (targetSelect.options.length === 0) {
      const opt = document.createElement('option');
      opt.value = "";
      opt.innerText = "Add another account first to migrate data";
      targetSelect.appendChild(opt);
    }
  }

  // Fetch updated projects, tasks, and conversations
  await Promise.all([
    fetchProjectsList(),
    fetchTasksList(),
    fetchConversationsList()
  ]);

  populateProjectFilterDropdown();
  switchModalTab(state.activeModalTab || 'projects');

  const modal = document.getElementById('migrationModal');
  if (modal) modal.classList.add('active');
}

function closeMigrationModal() {
  const modal = document.getElementById('migrationModal');
  if (modal) modal.classList.remove('active');
}

function switchModalTab(tabName) {
  state.activeModalTab = tabName;

  const btnProjects = document.getElementById('modalTabProjectsBtn');
  const btnTasks = document.getElementById('modalTabTasksBtn');
  const btnConvs = document.getElementById('modalTabConversationsBtn');

  if (btnProjects) btnProjects.className = `modal-tab-btn ${tabName === 'projects' ? 'active' : ''}`;
  if (btnTasks) btnTasks.className = `modal-tab-btn ${tabName === 'tasks' ? 'active' : ''}`;
  if (btnConvs) btnConvs.className = `modal-tab-btn ${tabName === 'conversations' ? 'active' : ''}`;

  const paneP = document.getElementById('paneProjects');
  const paneT = document.getElementById('paneTasks');
  const paneC = document.getElementById('paneConversations');
  const startBtn = document.getElementById('startMigrationBtn');

  if (paneP) paneP.style.display = (tabName === 'projects') ? 'flex' : 'none';
  if (paneT) paneT.style.display = (tabName === 'tasks') ? 'flex' : 'none';
  if (paneC) paneC.style.display = (tabName === 'conversations') ? 'flex' : 'none';

  if (startBtn) {
    startBtn.style.display = (tabName === 'conversations') ? 'inline-flex' : 'none';
  }

  if (tabName === 'projects') renderProjectList();
  else if (tabName === 'tasks') renderTaskList();
  else if (tabName === 'conversations') renderConversationPicker();
}

// 1. Projects Rendering & Actions
async function fetchProjectsList() {
  try {
    const res = await fetch('/api/projects').then(r => r.json()).catch(() => null);
    if (res && Array.isArray(res)) {
      state.projects = res;
    }
  } catch (e) {}
}

function renderProjectList() {
  const container = document.getElementById('projectCardList');
  if (!container) return;
  container.innerHTML = '';

  if (!state.projects || state.projects.length === 0) {
    container.innerHTML = `<div style="padding:20px;text-align:center;color:var(--text-muted);font-size:12px;">No projects found</div>`;
    return;
  }

  state.projects.forEach(p => {
    const card = document.createElement('div');
    card.className = 'project-item-card';

    const isShared = p.is_shared;
    const isInst2 = p.is_instance2_enabled;
    const badgeClass = isShared ? 'badge-shared' : (isInst2 ? 'badge-account1' : 'badge-account1');
    const badgeText = isShared ? t('sharedBadge') : (isInst2 ? t('account2OnlyBadge') : t('account1OnlyBadge'));

    card.innerHTML = `
      <div class="project-info-main">
        <div class="project-title-row">
          <span class="project-title-text">${p.name || p.id}</span>
          <span class="badge-tag ${badgeClass}">${badgeText}</span>
          <span class="badge-tag" style="background:rgba(255,255,255,0.06);color:var(--text-muted);">
            💬 ${p.conversation_count}
          </span>
        </div>
        <div class="project-path-text" title="${p.path}">${p.path || 'No folder path'}</div>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <label class="ios-switch" title="${t('assignToAccount2')}">
          <input type="checkbox" ${isInst2 ? 'checked' : ''} onchange="toggleProjectAssignment('${p.id}', this.checked)" />
          <span class="ios-slider"></span>
        </label>
        <button class="btn btn-glass" style="padding:5px 10px; font-size:11px;" onclick="syncProjectExplicit('${p.id}')" title="${t('syncProjectNow')}">
          <span>⇄ ${t('syncProjectNow')}</span>
        </button>
        <button class="btn btn-glass" style="padding:5px 8px; font-size:11px; color:#f87171; border-color:rgba(239,68,68,0.25);" onclick="unlinkProjectExplicit('${p.id}')" title="${t('removeFromAccount2')}">
          <span>✕</span>
        </button>
      </div>
    `;
    container.appendChild(card);
  });
}

async function unlinkProjectExplicit(projectId) {
  const targetAcc = getSecondaryAccountEmail();
  try {
    const res = await fetch('/api/project_unlink', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectId: projectId,
        account: targetAcc
      })
    }).then(r => r.json());

    if (res && res.success) {
      await fetchProjectsList();
      renderProjectList();
    }
  } catch (e) {
    alert('Failed to unlink project');
  }
}

async function toggleProjectAssignment(projectId, enableInInstance2) {
  const targetAcc = getSecondaryAccountEmail();
  try {
    if (enableInInstance2) {
      await fetch('/api/project_sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId: projectId,
          targetAccount: targetAcc,
          includeConversations: false
        })
      });
    } else {
      await fetch('/api/project_unlink', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          projectId: projectId,
          account: targetAcc
        })
      });
    }
    await fetchProjectsList();
    renderProjectList();
  } catch (e) {
    alert('Failed to update project profile assignment');
  }
}

async function syncProjectExplicit(projectId) {
  const targetAcc = getSecondaryAccountEmail();
  try {
    const res = await fetch('/api/project_sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        projectId: projectId,
        targetAccount: targetAcc,
        includeConversations: true
      })
    }).then(r => r.json());

    if (res && res.success) {
      alert(t('migrationSuccess'));
      await fetchProjectsList();
      renderProjectList();
    }
  } catch (e) {
    alert('Error syncing project');
  }
}

function filterProjects(query) {
  const q = query.toLowerCase().trim();
  document.querySelectorAll('#projectCardList .project-item-card').forEach(card => {
    const text = card.innerText.toLowerCase();
    card.style.display = text.includes(q) ? 'flex' : 'none';
  });
}

// 2. Tasks Rendering & Isolation Actions
async function fetchTasksList() {
  try {
    const res = await fetch('/api/tasks').then(r => r.json()).catch(() => null);
    if (res && Array.isArray(res)) {
      state.tasks = res;
    }
  } catch (e) {}
}

function renderTaskList() {
  const container = document.getElementById('taskCardList');
  if (!container) return;
  container.innerHTML = '';

  if (!state.tasks || state.tasks.length === 0) {
    container.innerHTML = `<div style="padding:20px;text-align:center;color:var(--text-muted);font-size:12px;">No scheduled tasks found</div>`;
    return;
  }

  state.tasks.forEach(task => {
    const card = document.createElement('div');
    card.className = 'task-item-card';

    const isIsolated = task.isolated_from_account2;
    const isEnabled = task.enabled;
    const isAcc2 = isAccount2(state.activeAccount && state.activeAccount.email);
    const isOwnerAcc1 = !task.owner_account || !isAccount2(task.owner_account);
    const isLocked = isAcc2 && isIsolated && isOwnerAcc1;

    const isoBadgeClass = isLocked ? 'badge-disabled' : (isIsolated ? 'badge-isolated' : 'badge-shared');
    const isoBadgeText = isLocked ? (t('taskLockedBadge') || '🔒 Locked') : (isIsolated ? t('taskIsolatedBadge') : t('taskSharedBadge'));

    card.innerHTML = `
      <div class="task-info-main">
        <div class="task-title-row">
          <span class="task-title-text">${task.name}</span>
          <span class="badge-tag ${isoBadgeClass}">${isoBadgeText}</span>
          <span class="badge-tag ${isEnabled ? 'badge-shared' : 'badge-disabled'}">
            ${isEnabled ? t('taskEnabled') : t('taskDisabled')}
          </span>
        </div>
        <div class="task-desc-text">${task.description || task.name} • ⏱ Next: ${task.next_run || 'N/A'}</div>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <button class="btn btn-glass" ${isLocked ? 'disabled' : ''} style="padding:5px 10px; font-size:11px; ${isLocked ? 'opacity:0.4;cursor:not-allowed;' : ''} border-color:${isIsolated ? 'rgba(245,158,11,0.4)' : 'rgba(255,255,255,0.1)'}" onclick="${isLocked ? `alert('${t('taskPermissionDenied')}')` : `toggleTaskIsolationExplicit('${task.name}', ${!isIsolated})`}">
          <span>${isIsolated ? '🛡 ' + t('unisolateTaskBtn') : '🔒 ' + t('isolateTaskBtn')}</span>
        </button>
        <label class="ios-switch" title="Toggle Task State" style="${isLocked ? 'opacity:0.4;cursor:not-allowed;' : ''}">
          <input type="checkbox" ${isLocked ? 'disabled' : ''} ${isEnabled ? 'checked' : ''} onchange="${isLocked ? `alert('${t('taskPermissionDenied')}')` : `toggleTaskActiveState('${task.name}', this.checked)`}" />
          <span class="ios-slider"></span>
        </label>
      </div>
    `;
    container.appendChild(card);
  });
}

async function toggleTaskIsolationExplicit(taskName, isolate) {
  try {
    const res = await fetch('/api/task_isolate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        taskName: taskName,
        ownerAccount: getPrimaryAccountEmail(),
        isolateFromAccount2: isolate,
        account: state.activeAccount ? state.activeAccount.email : getPrimaryAccountEmail()
      })
    }).then(r => r.json());

    if (res && res.success) {
      await fetchTasksList();
      renderTaskList();
    } else {
      alert((res && res.error) || t('taskPermissionDenied'));
      await fetchTasksList();
      renderTaskList();
    }
  } catch (e) {
    alert('Failed to update task isolation');
  }
}

async function toggleTaskActiveState(taskName, enable) {
  try {
    const res = await fetch('/api/task_toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        taskName: taskName,
        enable: enable,
        account: state.activeAccount ? state.activeAccount.email : getPrimaryAccountEmail()
      })
    }).then(r => r.json());

    if (res && res.success) {
      await fetchTasksList();
      renderTaskList();
    } else {
      alert((res && res.error) || t('taskPermissionDenied'));
      await fetchTasksList();
      renderTaskList();
    }
  } catch (e) {
    alert('Failed to toggle task state');
  }
}

// 3. Conversations & Migration
async function fetchConversationsList() {
  try {
    const res = await fetch('/api/conversations').then(r => r.json()).catch(() => null);
    if (res && Array.isArray(res)) {
      state.conversations = res;
    }
  } catch (err) {}
}

function populateProjectFilterDropdown() {
  const sel = document.getElementById('convProjectFilterSelect');
  if (!sel) return;
  sel.innerHTML = `<option value="" data-i18n="allProjects">${t('allProjects')}</option>`;
  
  const projectsSeen = new Map();
  state.conversations.forEach(c => {
    if (c.project_id && !projectsSeen.has(c.project_id)) {
      projectsSeen.set(c.project_id, c.project_name || c.project_id);
    }
  });

  projectsSeen.forEach((name, pid) => {
    const opt = document.createElement('option');
    opt.value = pid;
    opt.innerText = name;
    sel.appendChild(opt);
  });
}

function onFilterProjectChange(projectId) {
  state.migration.selectedProjectId = projectId;
  renderConversationPicker();
}

function renderConversationPicker() {
  const container = document.getElementById('conversationPickerList');
  if (!container) return;
  container.innerHTML = '';

  let filtered = state.conversations;
  if (state.migration.selectedProjectId) {
    filtered = filtered.filter(c => c.project_id === state.migration.selectedProjectId);
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div style="padding:16px; text-align:center; color:var(--text-muted); font-size:12px;">No conversations match filter</div>`;
    return;
  }

  filtered.forEach(c => {
    const isChecked = state.migration.selectedIds.has(c.id);
    const item = document.createElement('label');
    item.className = 'conv-item';
    item.innerHTML = `
      <input type="checkbox" value="${c.id}" ${isChecked ? 'checked' : ''} onchange="toggleConversationSelection('${c.id}', this.checked)" />
      <div style="display:flex; flex-direction:column; flex:1; min-width:0;">
        <span class="conv-title">${c.title || c.id}</span>
        <span style="font-size:10.5px; color:var(--text-dim);">${c.project_name || 'Outside of Project'}</span>
      </div>
      <span class="conv-date">${c.size_kb} KB • ${c.last_modified}</span>
    `;
    container.appendChild(item);
  });
}

function toggleConversationSelection(id, checked) {
  if (checked) state.migration.selectedIds.add(id);
  else state.migration.selectedIds.delete(id);
}

function toggleSelectAllConversations(selectAll) {
  state.migration.selectedIds.clear();
  if (selectAll) {
    let list = state.conversations;
    if (state.migration.selectedProjectId) {
      list = list.filter(c => c.project_id === state.migration.selectedProjectId);
    }
    list.forEach(c => state.migration.selectedIds.add(c.id));
  }
  renderConversationPicker();
}

function filterConversations(query) {
  const q = query.toLowerCase().trim();
  document.querySelectorAll('#conversationPickerList .conv-item').forEach(item => {
    const text = item.innerText.toLowerCase();
    item.style.display = text.includes(q) ? 'flex' : 'none';
  });
}

function selectMigrationMode(mode) {
  state.migration.mode = mode;
  document.getElementById('modeCopyCard').className = `radio-card ${mode === 'copy' ? 'selected' : ''}`;
  document.getElementById('modeCutCard').className = `radio-card ${mode === 'move' ? 'selected' : ''}`;
}

function selectStructureMode(struct) {
  state.migration.structure = struct;
  document.getElementById('structSeparateCard').className = `radio-card ${struct === 'separate' ? 'selected' : ''}`;
  document.getElementById('structMergeCard').className = `radio-card ${struct === 'merge' ? 'selected' : ''}`;
}

async function executeMigration() {
  const target = document.getElementById('modalTargetAccountSelect').value;
  if (!target) {
    alert("Please select a target account.");
    return;
  }

  const selectedList = Array.from(state.migration.selectedIds);
  if (selectedList.length === 0) {
    alert(t('selectConversations'));
    return;
  }

  const btn = document.getElementById('startMigrationBtn');
  btn.disabled = true;
  btn.innerText = t('migrating');

  const payload = {
    sourceAccount: state.migration.sourceAccount,
    targetAccount: target,
    conversationIds: selectedList,
    mode: state.migration.mode,
    structure: state.migration.structure,
    dualSync: document.getElementById('dualSyncCheckbox').checked,
    projectId: state.migration.selectedProjectId || null
  };

  callNative('migrate', payload);

  setTimeout(() => {
    btn.disabled = false;
    btn.innerText = t('startMigration');
    alert(t('migrationSuccess'));
    closeMigrationModal();
  }, 1200);
}

// Countdown Ticker
function startCountdownTicker() {
  setInterval(() => {
    if (!state.activeAccount || !state.activeAccount.session) return;
    const sess = state.activeAccount.session;
    if (!sess.reset_iso) return;

    const diff = Math.floor((new Date(sess.reset_iso).getTime() - Date.now()) / 1000);
    if (diff > 0) {
      const h = Math.floor(diff / 3600);
      const m = Math.floor((diff % 3600) / 60);
      const s = diff % 60;
      let str = "";
      if (h > 0) str += `${h}h `;
      str += `${m}m ${s}s`;
      document.getElementById('quotaCountdown').innerText = `⏱ ${t('resetsIn')} ${str}`;
    } else {
      document.getElementById('quotaCountdown').innerText = t('noActiveLimit');
    }
  }, 1000);
}
