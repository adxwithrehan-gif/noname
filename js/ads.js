// AdSense Unit Injector
const AD_CONFIG = {
  client_id: "ca-pub-XXXXXXXXXXXXXXXX", // Replace with your AdSense Publisher ID
  header_slot: "1234567890",
  article_slot: "0987654321",
  footer_slot: "1122334455"
};

function initializeAds() {
  injectAd('ad-header', AD_CONFIG.header_slot);
  injectAd('ad-article', AD_CONFIG.article_slot);
  injectAd('ad-footer', AD_CONFIG.footer_slot);
}

function injectAd(containerId, slotId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = `
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="${AD_CONFIG.client_id}"
         data-ad-slot="${slotId}"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
  `;
  try {
    (adsbygoogle = window.adsbygoogle || []).push({});
  } catch (e) {}
}

document.addEventListener("DOMContentLoaded", initializeAds);
