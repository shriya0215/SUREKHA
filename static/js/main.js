// ── AUTO TOTAL FOR RECEIPT ────────────────────────────────────────────────────
function calcReceiptTotal() {
  const inputs = document.querySelectorAll('.receipt-amount-input');
  let total = 0;
  inputs.forEach(inp => { total += parseFloat(inp.value || 0); });
  const el = document.getElementById('receipt-total');
  if (el) el.textContent = '₹ ' + total.toFixed(2);
  const hidEl = document.getElementById('receipt-total-hidden');
  if (hidEl) hidEl.value = total.toFixed(2);
}

document.addEventListener('DOMContentLoaded', () => {
  // Attach listeners to all receipt amount inputs
  document.querySelectorAll('.receipt-amount-input').forEach(inp => {
    inp.addEventListener('input', calcReceiptTotal);
  });

  // ── BILLING MODE TOGGLE ───────────────────────────────────────────────────
  const autoBtn = document.getElementById('mode-auto');
  const manualBtn = document.getElementById('mode-manual');
  const modeInput = document.getElementById('billing-mode');
  const manualTable = document.getElementById('manual-table');

  if (autoBtn && manualBtn) {
    autoBtn.addEventListener('click', () => {
      autoBtn.classList.add('active');
      manualBtn.classList.remove('active');
      modeInput.value = 'Auto';
      if (manualTable) manualTable.style.display = 'none';
    });
    manualBtn.addEventListener('click', () => {
      manualBtn.classList.add('active');
      autoBtn.classList.remove('active');
      modeInput.value = 'Manual';
      if (manualTable) manualTable.style.display = '';
    });
  }

  // ── BILLING CYCLE TOGGLE ─────────────────────────────────────────────────
  const monthlyBtn = document.getElementById('cycle-monthly');
  const quarterlyBtn = document.getElementById('cycle-quarterly');
  const cycleInput = document.getElementById('billing-cycle-input');

  if (monthlyBtn && quarterlyBtn) {
    monthlyBtn.addEventListener('click', () => {
      monthlyBtn.classList.add('active');
      quarterlyBtn.classList.remove('active');
      if (cycleInput) cycleInput.value = 'Monthly';
    });
    quarterlyBtn.addEventListener('click', () => {
      quarterlyBtn.classList.add('active');
      monthlyBtn.classList.remove('active');
      if (cycleInput) cycleInput.value = 'Quarterly';
    });
  }

  // ── MEETING AGENDA POINT BUILDER ─────────────────────────────────────────
  const addPointBtn = document.getElementById('add-agenda-point');
  const pointsContainer = document.getElementById('agenda-points-container');
  if (addPointBtn && pointsContainer) {
    let count = pointsContainer.querySelectorAll('.agenda-point-row').length || 1;
    addPointBtn.addEventListener('click', () => {
      count++;
      const row = document.createElement('div');
      row.className = 'agenda-point-row';
      row.style.cssText = 'display:flex;gap:10px;align-items:center;margin-bottom:10px;';
      row.innerHTML = `
        <span style="min-width:24px;font-weight:700;color:#1a237e;">${count}.</span>
        <input type="text" name="agenda_point" class="form-control"
          placeholder="Agenda Point ${count}"
          style="flex:1;padding:10px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-family:Poppins,sans-serif;font-size:13px;">
        <button type="button" onclick="this.parentElement.remove()"
          style="background:#fee2e2;border:none;color:#dc2626;border-radius:6px;padding:6px 10px;cursor:pointer;">✕</button>
      `;
      pointsContainer.appendChild(row);
    });
  }

  // ── CASH/BANK TAB SWITCH ─────────────────────────────────────────────────
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // ── AUTO CLOSE FLASH MESSAGES ────────────────────────────────────────────
  setTimeout(() => {
    document.querySelectorAll('.flash').forEach(el => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    });
  }, 3500);

  // ── CONFIRM DELETE ────────────────────────────────────────────────────────
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (!confirm('Are you sure you want to delete this?')) {
        e.preventDefault();
      }
    });
  });
});

// ── PRINT FUNCTION ────────────────────────────────────────────────────────────
function printPage() { window.print(); }
