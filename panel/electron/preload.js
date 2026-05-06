const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onTelemetryUpdate: (callback) => {
    const listener = (_event, value) => callback(value);
    ipcRenderer.on('telemetry-update', listener);
    return () => ipcRenderer.removeListener('telemetry-update', listener);
  }
});
