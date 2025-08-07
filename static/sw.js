const CACHE_NAME = 'prompt-manager-v1.0.0';
const STATIC_CACHE = 'static-v1.0.0';
const DYNAMIC_CACHE = 'dynamic-v1.0.0';

// 캐시할 정적 파일들
const STATIC_FILES = [
  '/',
  '/css/global.css',
  '/css/layout.css',
  '/css/components.css',
  '/css/animations.css',
  '/static/manifest.json',
  '/static/icons/icon.svg',
  '/static/pwa.css',
  '/static/pwa.js'
];

// 설치 시 정적 파일들 캐시
self.addEventListener('install', event => {
  console.log('Service Worker 설치 중...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('정적 파일들 캐시 중...');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker 설치 완료');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Service Worker 설치 실패:', error);
      })
  );
});

// 활성화 시 이전 캐시 정리
self.addEventListener('activate', event => {
  console.log('Service Worker 활성화 중...');
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('이전 캐시 삭제:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker 활성화 완료');
        return self.clients.claim();
      })
  );
});

// 네트워크 요청 가로채기
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // API 요청은 네트워크 우선, 실패 시 캐시
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // 성공한 응답을 동적 캐시에 저장
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(DYNAMIC_CACHE)
              .then(cache => cache.put(request, responseClone));
          }
          return response;
        })
        .catch(() => {
          // 네트워크 실패 시 캐시에서 찾기
          return caches.match(request);
        })
    );
    return;
  }

  // 정적 파일은 캐시 우선, 실패 시 네트워크
  if (request.method === 'GET') {
    event.respondWith(
      caches.match(request)
        .then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }

          return fetch(request)
            .then(response => {
              // 성공한 응답을 동적 캐시에 저장
              if (response.ok) {
                const responseClone = response.clone();
                caches.open(DYNAMIC_CACHE)
                  .then(cache => cache.put(request, responseClone));
              }
              return response;
            });
        })
    );
  }
});

// 백그라운드 동기화 (선택사항)
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    console.log('백그라운드 동기화 실행');
    event.waitUntil(doBackgroundSync());
  }
});

// 백그라운드 동기화 함수
async function doBackgroundSync() {
  try {
    // 오프라인 중 저장된 데이터가 있다면 서버에 동기화
    console.log('백그라운드 동기화 완료');
  } catch (error) {
    console.error('백그라운드 동기화 실패:', error);
  }
}

// 푸시 알림 처리 (선택사항)
self.addEventListener('push', event => {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body || '새로운 프롬프트가 등록되었습니다.',
      icon: '/static/icons/icon-192x192.png',
      badge: '/static/icons/icon-72x72.png',
      vibrate: [100, 50, 100],
      data: {
        dateOfArrival: Date.now(),
        primaryKey: 1
      },
      actions: [
        {
          action: 'explore',
          title: '확인하기',
          icon: '/static/icons/icon-72x72.png'
        },
        {
          action: 'close',
          title: '닫기',
          icon: '/static/icons/icon-72x72.png'
        }
      ]
    };

    event.waitUntil(
      self.registration.showNotification(data.title || '프롬프트 관리자', options)
    );
  }
});

// 알림 클릭 처리
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});
