import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import * as path from "path"

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  const publish = env.PUBLISH === '1'
  const staging = env.STAGING === '1'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        'vue': path.resolve(__dirname, 'node_modules/vue/dist/vue.esm-bundler.js'),
        '~': path.resolve(__dirname, "src"),
      },
    },
    build: {
      rollupOptions: {
        input: {
          main: 'src/main.ts',
        },
        output: {
          entryFileNames: 'js/[name].js',
          assetFileNames: 'css/[name].[ext]'
        }
      }
    },
    define: {
      'process.env': {
        NODE_ENV: staging || publish ? "production" : "development"
      }
    }
  }
})
