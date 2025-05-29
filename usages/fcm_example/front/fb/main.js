import { initMessaging } from './firebase-config.js';

if ('serviceWorker' in navigator) {
   window.initMessaging = initMessaging;
  initMessaging();
}