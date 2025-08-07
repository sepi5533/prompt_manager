// PWA 관련 기능들
class PromptManagerPWA {
  constructor() {
    this.deferredPrompt = null;
    this.installButton = null;
    this.isOnline = navigator.onLine;
    this.init();
  }

  init() {
    this.registerServiceWorker();
    this.setupInstallPrompt();
    this.setupOnlineOfflineHandlers();
    this.setupUpdateNotification();
    this.setupOfflineIndicator();
  }

  // Service Worker 등록
  async registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/static/sw.js');
        console.log('Service Worker 등록 성공:', registration);
        
        // 업데이트 확인
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              this.showUpdateNotification();
            }
          });
        });
      } catch (error) {
        console.error('Service Worker 등록 실패:', error);
      }
    }
  }

  // 설치 프롬프트 설정
  setupInstallPrompt() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallButton();
    });

    // 설치 완료 이벤트
    window.addEventListener('appinstalled', () => {
      console.log('PWA가 설치되었습니다.');
      this.hideInstallButton();
      this.deferredPrompt = null;
    });
  }

  // 설치 버튼 표시
  showInstallButton() {
    if (!this.installButton) {
      this.installButton = document.createElement('button');
      this.installButton.id = 'install-button';
      this.installButton.innerHTML = '<i class="fas fa-download"></i> 앱 설치';
      this.installButton.className = 'install-button';
      this.installButton.onclick = () => this.installApp();
      
      const header = document.querySelector('header');
      if (header) {
        header.appendChild(this.installButton);
      }
    }
    this.installButton.style.display = 'block';
  }

  // 설치 버튼 숨기기
  hideInstallButton() {
    if (this.installButton) {
      this.installButton.style.display = 'none';
    }
  }

  // 앱 설치
  async installApp() {
    if (this.deferredPrompt) {
      this.deferredPrompt.prompt();
      const { outcome } = await this.deferredPrompt.userChoice;
      console.log('설치 결과:', outcome);
      this.deferredPrompt = null;
      this.hideInstallButton();
    }
  }

  // 온라인/오프라인 상태 처리
  setupOnlineOfflineHandlers() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.updateOnlineStatus();
      this.syncOfflineData();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.updateOnlineStatus();
    });
  }

  // 온라인 상태 업데이트
  updateOnlineStatus() {
    const statusElement = document.getElementById('online-status');
    if (statusElement) {
      statusElement.textContent = this.isOnline ? '온라인' : '오프라인';
      statusElement.className = this.isOnline ? 'online' : 'offline';
    }
  }

  // 오프라인 데이터 동기화
  async syncOfflineData() {
    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
      try {
        await navigator.serviceWorker.ready;
        await navigator.serviceWorker.sync.register('background-sync');
        console.log('백그라운드 동기화 등록 완료');
      } catch (error) {
        console.error('백그라운드 동기화 등록 실패:', error);
      }
    }
  }

  // 업데이트 알림 표시
  setupUpdateNotification() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        this.showUpdateNotification();
      });
    }
  }

  // 업데이트 알림 표시
  showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'update-notification';
    notification.innerHTML = `
      <div class="update-content">
        <i class="fas fa-sync-alt"></i>
        <span>새로운 업데이트가 있습니다. 새로고침하세요.</span>
        <button onclick="this.parentElement.parentElement.remove()">닫기</button>
        <button onclick="location.reload()">새로고침</button>
      </div>
    `;
    document.body.appendChild(notification);
  }

  // 오프라인 표시기 설정
  setupOfflineIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'offline-indicator';
    indicator.className = 'offline-indicator';
    indicator.innerHTML = '<i class="fas fa-wifi-slash"></i> 오프라인 모드';
    document.body.appendChild(indicator);
    
    this.updateOfflineIndicator();
  }

  // 오프라인 표시기 업데이트
  updateOfflineIndicator() {
    const indicator = document.getElementById('offline-indicator');
    if (indicator) {
      indicator.style.display = this.isOnline ? 'none' : 'block';
    }
  }

  // 푸시 알림 권한 요청
  async requestNotificationPermission() {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        console.log('푸시 알림 권한이 허용되었습니다.');
        return true;
      } else {
        console.log('푸시 알림 권한이 거부되었습니다.');
        return false;
      }
    }
    return false;
  }

  // 푸시 알림 전송 (테스트용)
  async sendTestNotification() {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      try {
        const registration = await navigator.serviceWorker.ready;
        await registration.showNotification('테스트 알림', {
          body: '프롬프트 관리자 PWA가 정상적으로 작동합니다.',
          icon: '/static/icons/icon-192x192.png',
          badge: '/static/icons/icon-72x72.png'
        });
      } catch (error) {
        console.error('알림 전송 실패:', error);
      }
    }
  }
}

// PWA 초기화
document.addEventListener('DOMContentLoaded', () => {
  window.promptManagerPWA = new PromptManagerPWA();
});

// 전역 함수들
window.installPWA = () => {
  if (window.promptManagerPWA) {
    window.promptManagerPWA.installApp();
  }
};

window.requestNotificationPermission = () => {
  if (window.promptManagerPWA) {
    window.promptManagerPWA.requestNotificationPermission();
  }
};

window.sendTestNotification = () => {
  if (window.promptManagerPWA) {
    window.promptManagerPWA.sendTestNotification();
  }
};
