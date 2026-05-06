import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  onTelemetryUpdate: (callback) => ipcRenderer.on('telemetry-update', (_event, value) => callback(value))
});
