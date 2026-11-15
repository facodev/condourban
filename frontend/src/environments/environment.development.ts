export const environment = {
  production: false,
  apiUrl: '/api/v1',
  wsUrl: typeof window !== 'undefined'
    ? `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws`
    : 'ws://localhost:8000/ws',
};