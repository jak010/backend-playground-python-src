// firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.7.1/firebase-app.js";
import {
  getMessaging,
  getToken,
  onMessage,
  isSupported
} from "https://www.gstatic.com/firebasejs/11.7.1/firebase-messaging.js";

// Firebase 설정
const firebaseConfig = {
    apiKey           : "",
    authDomain       : "",
    projectId        : "",
    storageBucket    : "",
    messagingSenderId: "",
    appId            : ""
};

const app = initializeApp(firebaseConfig);

export async function initMessaging() {
  const supported = await isSupported();
  if (!supported) {
    alert("이 브라우저는 FCM을 지원하지 않습니다.");
    console.warn("이 브라우저는 FCM을 지원하지 않습니다.");
    return;
  }

  // 알림 권한 요청

  const messaging = getMessaging(app);

  try {
    // Service Worker 등록
    const registration = await navigator.serviceWorker.register("/firebase-messaging-sw.js");
    console.log("Service Worker 등록 성공:", registration);

    // 구성 정보 출력 (디버깅 용도)
    console.log("SW Scope:", registration.scope);
    console.log("SW Active:", registration.active);
    console.log("SW Installing:", registration.installing);
    console.log("SW Waiting:", registration.waiting);
    console.log("SW PushManager:", registration.pushManager);

    // FCM 토큰 요청
    const token = await getToken(messaging, {
      vapidKey: "",
      serviceWorkerRegistration: registration
    });

    console.log("FCM 토큰:", token);
    document.getElementById("token-container").textContent = token;

  } catch (err) {
    console.error("FCM 토큰 가져오기 실패:", err);
  }

  // 포그라운드 수신 처리
  onMessage(messaging, (payload) => {
    console.log("포그라운드 메시지 수신:", payload);
    const { title, body, icon } = payload.notification;
    // TODO: 알림 표시 구현 가능
  });
}


initMessaging();