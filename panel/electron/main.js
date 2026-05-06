import { app, BrowserWindow } from 'electron'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

process.env.DIST = path.join(__dirname, '../dist')
process.env.VITE_PUBLIC = app.isPackaged ? process.env.DIST : path.join(process.env.DIST, '../public')

let win
function createWindow() {
  win = new BrowserWindow({
    width: 1440,
    height: 900,
    title: 'ODBARS NEXUS - Yer Kontrol İstasyonu',
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
      nodeIntegration: false,
      contextIsolation: true
    },
  })

  // Dev server
  if (process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL)
  } else {
    // Production build
    win.loadFile(path.join(process.env.DIST, 'index.html'))
  }

  // MOCK TELEMETRY SIMULATOR
  win.webContents.on('did-finish-load', () => {
    setInterval(() => {
      if (!win) return;
      
      const mockData = {
        battery: Math.floor(Math.random() * 5 + 80), // 80-85%
        speed: (Math.random() * 2 + 1).toFixed(1), // 1.0 - 3.0 m/s
        pitch: (Math.random() * 6 - 3).toFixed(1), // -3.0 to +3.0
        roll: (Math.random() * 2 - 1).toFixed(1), // -1.0 to +1.0
        ping: Math.floor(Math.random() * 20 + 10), // 10-30 ms
      };
      
      win.webContents.send('telemetry-update', mockData);
    }, 1000); // Saniyede 1 kez güncelle
  });
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

app.whenReady().then(createWindow)
