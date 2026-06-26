import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'systems.alexicon.yipnet',
  appName: 'yipnet',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  },
};

export default config;
