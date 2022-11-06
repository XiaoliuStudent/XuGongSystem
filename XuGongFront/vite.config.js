import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

const {resolve} = require('path')
// const { defineConfig } = require('vite')

export default defineConfig(({command, mode, ssrBuild}) => {

    if (command === 'serve') {
        return {
            plugins: [vue()],
            build: {
                rollupOptions: {
                    input: {
                        main: resolve(__dirname, 'index.html'),
                        student: resolve(__dirname, 'student/index.html')
                    }
                }
            },
            server: {
                host: '0.0.0.0',
                port: '8080',
                proxy: {
                    '/api': {
                        target: 'http://127.0.0.1:8085/api/',
                        changeOrigin: true,
                        rewrite: path => path.replace(/^\/api/, '')
                    }
                },
            }
        }
    } else {
        // command === 'build'
        return {
            plugins: [vue()],
            build: {
                rollupOptions: {
                    input: {
                        main: resolve(__dirname, 'index.html'),
                        student: resolve(__dirname, 'student/index.html')
                    }
                }
            },
        }
    }
})
