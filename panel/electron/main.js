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
      preload: path.join(__dirname, 'preload.js'),
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
  // Daha gerçekçi akış için state tutalım (Random Walk algoritması)
  let mockState = {
    pitch: 0.0,
    roll: 0.0,
    speed: 1.5,
    battery: 84
  };

  win.webContents.on('did-finish-load', () => {
    const telemetryInterval = setInterval(() => {
      if (!win || win.isDestroyed() || win.webContents.isDestroyed()) {
        clearInterval(telemetryInterval);
        return;
      }
      
      // Değerleri küçük adımlarla (smooth) değiştir
      mockState.pitch += (Math.random() * 0.4 - 0.2);
      if (mockState.pitch > 15) mockState.pitch = 15;
      if (mockState.pitch < -15) mockState.pitch = -15;

      mockState.roll += (Math.random() * 0.2 - 0.1);
      if (mockState.roll > 5) mockState.roll = 5;
      if (mockState.roll < -5) mockState.roll = -5;

      mockState.speed += (Math.random() * 0.2 - 0.1);
      if (mockState.speed < 0) mockState.speed = 0.0;
      if (mockState.speed > 5) mockState.speed = 5.0;

      // Batarya çok nadir düşsün (simülasyon)
      if (Math.random() < 0.001) mockState.battery -= 1;

      const mockData = {
        battery: mockState.battery,
        speed: mockState.speed.toFixed(1),
        pitch: mockState.pitch.toFixed(1),
        roll: mockState.roll.toFixed(1),
        ping: Math.floor(Math.random() * 5 + 15), // 15-20ms
      };
      
      try {
        win.webContents.send('telemetry-update', mockData);
      } catch (e) {
        clearInterval(telemetryInterval);
      }
    }, 50); // Saniyede 20 kez (20Hz) ultra hızlı güncelleme
    
    win.on('closed', () => {
      clearInterval(telemetryInterval);
    });
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
