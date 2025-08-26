const DEV_API_BASE_URL: string = 'https://e888dd090da4.ngrok-free.app'; // Your local IP
const PROD_API_BASE_URL: string = 'https://your-public-api.com'; // Placeholder for your deployed API

declare const __DEV__: boolean;

export const API_BASE_URL: string = __DEV__ ? DEV_API_BASE_URL : PROD_API_BASE_URL;
export const AR_BASE_URL: string = __DEV__ ? 'https://e888dd090da4.ngrok-free.app/ar' : 'https://your-public-ar-domain.com/ar';
