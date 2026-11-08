chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "aegisTrustScanLink",
    title: "Inspect link with AegisTrust",
    contexts: ["link"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "aegisTrustScanLink" && info.linkUrl) {
    // Open AegisTrust web dashboard pointing to this URL
    const scanUrl = `http://localhost:3000/?url=${encodeURIComponent(info.linkUrl)}`;
    chrome.tabs.create({ url: scanUrl });
  }
});

