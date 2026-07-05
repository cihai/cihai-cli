/* cihai install widget state. */
(function () {
  "use strict";

  var STORAGE = {
    method: "cihai-cli.install.method",
    cooldownEnabled: "cihai-cli.install.cooldown.enabled",
    cooldownType: "cihai-cli.install.cooldown.type",
    cooldownDays: "cihai-cli.install.cooldown.days",
  };
  var DEFAULT_METHOD = "uvx";
  var DEFAULT_COOLDOWN_DAYS = 7;
  var VALID_COOLDOWN_TYPES = { days: true, bypass: true };

  document.addEventListener("click", onClick);
  document.addEventListener("change", onChange);
  document.addEventListener("input", onInput);
  document.addEventListener("keydown", onKeydown);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applySavedState);
  } else {
    applySavedState();
  }
  document.addEventListener("gp-sphinx:navigated", applySavedState);

  function applySavedState() {
    var method = localStorage.getItem(STORAGE.method) || DEFAULT_METHOD;
    var enabled = readCooldownEnabled();
    var type = readCooldownType();
    var days = readCooldownDays();
    syncHtmlState(method, enabled, type, days);
    document.querySelectorAll(".cihai-install").forEach(function (widget) {
      selectMethod(widget, method, false);
      applyCooldown(widget, enabled, type, days);
      showInstallView(widget);
    });
  }

  function onClick(event) {
    var tab = event.target.closest(".cihai-install__tab");
    if (tab) {
      var widget = tab.closest(".cihai-install");
      if (!widget) return;
      selectAllMethods(tab.dataset.tabValue, true);
      showInstallView(widget);
      return;
    }

    var action = event.target.closest("[data-action]");
    if (!action) return;
    var actionWidget = action.closest(".cihai-install");
    if (!actionWidget) return;
    if (action.dataset.action === "cooldown-open") {
      showSettingsView(actionWidget);
      event.preventDefault();
    } else if (action.dataset.action === "cooldown-back") {
      showInstallView(actionWidget);
      event.preventDefault();
    }
  }

  function onChange(event) {
    var action = event.target.closest("[data-action]");
    if (!action) return;
    var widget = action.closest(".cihai-install");
    if (!widget) return;

    if (action.dataset.action === "cooldown-toggle") {
      localStorage.setItem(STORAGE.cooldownEnabled, action.checked ? "1" : "0");
      applyAllCooldowns();
      return;
    }
    if (action.dataset.action === "cooldown-mode") {
      if (!VALID_COOLDOWN_TYPES[action.value]) return;
      localStorage.setItem(STORAGE.cooldownType, action.value);
      localStorage.setItem(STORAGE.cooldownEnabled, "1");
      applyAllCooldowns();
      return;
    }
    if (action.dataset.action === "cooldown-days") {
      var days = clampDays(parseInt(action.value, 10));
      localStorage.setItem(STORAGE.cooldownDays, String(days));
      localStorage.setItem(STORAGE.cooldownType, "days");
      localStorage.setItem(STORAGE.cooldownEnabled, "1");
      applyAllCooldowns();
    }
  }

  function onInput(event) {
    var input = event.target.closest('[data-action="cooldown-days"]');
    if (!input) return;
    var value = parseInt(input.value, 10);
    if (isNaN(value) || value < 1) return;
    updateCooldownSlots(clampDays(value));
  }

  function onKeydown(event) {
    var tab = event.target.closest(".cihai-install__tab");
    if (!tab) return;
    var widget = tab.closest(".cihai-install");
    if (!widget) return;

    var tabs = Array.prototype.slice.call(widget.querySelectorAll(".cihai-install__tab"));
    var current = tabs.indexOf(tab);
    var next = current;
    switch (event.key) {
      case "ArrowRight":
      case "ArrowDown":
        next = (current + 1) % tabs.length;
        break;
      case "ArrowLeft":
      case "ArrowUp":
        next = (current - 1 + tabs.length) % tabs.length;
        break;
      case "Home":
        next = 0;
        break;
      case "End":
        next = tabs.length - 1;
        break;
      default:
        return;
    }
    event.preventDefault();
    tabs[next].focus();
    selectAllMethods(tabs[next].dataset.tabValue, true);
  }

  function selectAllMethods(method, persist) {
    document.querySelectorAll(".cihai-install").forEach(function (widget) {
      selectMethod(widget, method, false);
    });
    if (persist) {
      localStorage.setItem(STORAGE.method, method);
      document.documentElement.setAttribute("data-cihai-install-method", method);
    }
  }

  function selectMethod(widget, method, persist) {
    var tabs = widget.querySelectorAll(".cihai-install__tab");
    var hasMatch = false;
    tabs.forEach(function (tab) {
      var selected = tab.dataset.tabValue === method;
      if (selected) hasMatch = true;
      tab.setAttribute("aria-selected", selected ? "true" : "false");
      tab.setAttribute("tabindex", selected ? "0" : "-1");
    });
    if (!hasMatch) return;
    if (persist) localStorage.setItem(STORAGE.method, method);
    document.documentElement.setAttribute("data-cihai-install-method", method);
    updatePanels(widget);
  }

  function updatePanels(widget) {
    var selectedTab = widget.querySelector('.cihai-install__tab[aria-selected="true"]');
    var method = selectedTab ? selectedTab.dataset.tabValue : DEFAULT_METHOD;
    var cooldown = readCooldownEnabled() ? readCooldownType() : "off";
    widget.querySelectorAll(".cihai-install__panel").forEach(function (panel) {
      var visible = panel.dataset.method === method && panel.dataset.cooldown === cooldown;
      panel.hidden = !visible;
    });
  }

  function applyAllCooldowns() {
    var enabled = readCooldownEnabled();
    var type = readCooldownType();
    var days = readCooldownDays();
    syncHtmlState(localStorage.getItem(STORAGE.method) || DEFAULT_METHOD, enabled, type, days);
    document.querySelectorAll(".cihai-install").forEach(function (widget) {
      applyCooldown(widget, enabled, type, days);
    });
  }

  function applyCooldown(widget, enabled, type, days) {
    var toggle = widget.querySelector('[data-action="cooldown-toggle"]');
    if (toggle) toggle.checked = enabled;
    widget.querySelectorAll('[data-action="cooldown-mode"]').forEach(function (radio) {
      radio.checked = radio.value === type;
    });
    var daysInput = widget.querySelector('[data-action="cooldown-days"]');
    if (daysInput && document.activeElement !== daysInput) {
      daysInput.value = String(days);
    }
    updateCooldownSlots(days);
    updatePanels(widget);
  }

  function showSettingsView(widget) {
    var install = widget.querySelector(".cihai-install__body--install");
    var settings = widget.querySelector(".cihai-install__body--settings");
    if (install) install.hidden = true;
    if (settings) settings.hidden = false;
  }

  function showInstallView(widget) {
    var install = widget.querySelector(".cihai-install__body--install");
    var settings = widget.querySelector(".cihai-install__body--settings");
    if (install) install.hidden = false;
    if (settings) settings.hidden = true;
  }

  function readCooldownEnabled() {
    return localStorage.getItem(STORAGE.cooldownEnabled) === "1";
  }

  function readCooldownType() {
    var type = localStorage.getItem(STORAGE.cooldownType);
    return VALID_COOLDOWN_TYPES[type] ? type : "days";
  }

  function readCooldownDays() {
    return clampDays(parseInt(localStorage.getItem(STORAGE.cooldownDays), 10));
  }

  function clampDays(value) {
    if (isNaN(value)) return DEFAULT_COOLDOWN_DAYS;
    if (value < 1) return 1;
    if (value > 365) return 365;
    return value;
  }

  function updateCooldownSlots(days) {
    document.documentElement.setAttribute("data-cihai-install-cooldown-days", String(days));
    document.querySelectorAll(".cihai-install [data-cooldown-duration-slot]").forEach(function (slot) {
      slot.textContent = "P" + days + "D";
    });
  }

  function syncHtmlState(method, enabled, type, days) {
    document.documentElement.setAttribute("data-cihai-install-method", method);
    document.documentElement.setAttribute("data-cihai-install-cooldown-enabled", enabled ? "1" : "0");
    document.documentElement.setAttribute("data-cihai-install-cooldown-type", type);
    document.documentElement.setAttribute("data-cihai-install-cooldown-days", String(days));
  }
})();
