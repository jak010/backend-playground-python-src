importScripts('https://www.gstatic.com/firebasejs/11.7.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/11.7.1/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey           : "",
    authDomain       : "",
    projectId        : "",
    storageBucket    : "",
    messagingSenderId: "",
    appId            : ""
});

const messaging = firebase.messaging();

// 🔹 백그라운드 메시지 수신 시 알림 표시
messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] 백그라운드 메시지 수신:', payload);

  const title = payload.notification.title;
  const body = payload.notification.body;
  const url = payload.data.url || '/';

  self.registration.showNotification(title, {
    body: body,
    data: { url: url }
  });
});

// 🔹 클릭 시 URL 이동
self.addEventListener('notificationclick', function(event) {
  event.notification.close();

  const urlToOpen = event.notification.data?.url || '/';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(clientList) {
      for (const client of clientList) {
        if (client.url === urlToOpen && 'focus' in client) {
          return client.focus();
        }
      }
      return clients.openWindow(urlToOpen);
    })
  );
});
