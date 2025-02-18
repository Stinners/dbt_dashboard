import { defineConfig } from 'vite';
import solidPlugin from 'vite-plugin-solid';

export default defineConfig({
  plugins: [solidPlugin()],
  server: {
    port: 3000,
    proxy: {
        '/api/': {
            target: "http://localhost:8000",
            rewriteWsOrigin: true
        }
    }
  },
  build: {
    target: 'esnext',
  },
});
