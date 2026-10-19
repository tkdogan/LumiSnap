// Only turn release buttons on when a real HTTPS destination is configured.
for (const platform of ["desktop", "ios"]) {
  const value = window.LUMISNAP_LINKS?.[platform];
  if (!value) continue;
  try {
    const url = new URL(value);
    if (url.protocol !== "https:") continue;
    const button = document.getElementById(`${platform}-download`);
    button.href = url.href;
    button.hidden = false;
    document.getElementById(`${platform}-pending`).hidden = true;
  } catch { /* An invalid release URL leaves the availability message visible. */ }
}
