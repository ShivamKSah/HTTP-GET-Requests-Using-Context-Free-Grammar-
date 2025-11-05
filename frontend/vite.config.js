import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  base: '/HTTP-GET-Requests-Using-Context-Free-Grammar-/',
  plugins: [react()],
})