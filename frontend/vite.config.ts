import path from "node:path"
import { TanStackRouterVite } from "@tanstack/router-vite-plugin"
import react from "@vitejs/plugin-react-swc"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  plugins: [react(), TanStackRouterVite()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
            // Return mock data for auth endpoints when backend is down
            if (req.url === '/api/login/access-token' && req.method === 'POST') {
              res.writeHead(200, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({
                access_token: 'mock-token-for-development',
                token_type: 'bearer'
              }));
            } else if (req.url === '/api/users/me' && req.method === 'GET') {
              res.writeHead(200, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({
                email: 'demo@redpanda.ai',
                is_active: true,
                is_superuser: false,
                full_name: 'Demo User',
                id: 'demo-user-id'
              }));
            } else {
              res.writeHead(503, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ 
                detail: 'Backend service unavailable. Please start the backend server.' 
              }));
            }
          });
        }
      }
    }
  }
})
