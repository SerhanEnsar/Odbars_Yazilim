import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Battery, 
  Camera, 
  Crosshair, 
  ShieldAlert, 
  Wifi, 
  Zap, 
  Terminal,
  Play,
  Pause,
  AlertOctagon,
  Settings2,
  ListTodo
} from 'lucide-react';

export default function App() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 p-4 font-sans select-none flex flex-col h-screen overflow-hidden">
      {/* Header */}
      <header className="flex justify-between items-center bg-slate-800 p-3 rounded-xl border border-slate-700 shadow-lg mb-4 shrink-0">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center border border-emerald-500/50">
            <Activity className="text-emerald-400" size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-wider text-slate-100">İKA GCS <span className="text-emerald-400">NEXUS</span></h1>
            <p className="text-xs text-slate-400 uppercase tracking-widest">Taktik Kontrol Arayüzü v1.0</p>
          </div>
        </div>

        <div className="flex space-x-6">
          <div className="flex flex-col items-center">
            <span className="text-xs text-slate-400 mb-1">GÖREV SÜRESİ</span>
            <span className="text-xl font-mono text-amber-400 font-bold">14:23</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-xs text-slate-400 mb-1">SİSTEM ZAMANI</span>
            <span className="text-xl font-mono text-slate-300">{currentTime.toLocaleTimeString('tr-TR', { hour12: false })}</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-700">
            <Wifi className="text-emerald-400" size={18} />
            <span className="text-sm font-mono font-bold text-emerald-400">98%</span>
            <span className="text-xs text-slate-500">12ms ping</span>
          </div>
          <button className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-bold flex items-center space-x-2 transition-all shadow-[0_0_15px_rgba(239,68,68,0.5)] active:scale-95 border-2 border-red-400">
            <AlertOctagon size={20} />
            <span>ACİL DURDURMA</span>
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <div className="flex-1 grid grid-cols-12 gap-4 min-h-0">
        
        {/* Left Column: Mission & Telemetry */}
        <div className="col-span-3 flex flex-col gap-4 overflow-y-auto pr-1">
          
          {/* Active Mode */}
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-bold text-slate-300 uppercase flex items-center gap-2">
                <Settings2 size={16} className="text-blue-400" />
                Sürüş Modu
              </h2>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button className="bg-blue-600/20 border border-blue-500/50 text-blue-400 py-2 rounded-lg font-bold hover:bg-blue-600/30 transition-colors">
                OTONOM
              </button>
              <button className="bg-slate-700 text-slate-400 py-2 rounded-lg font-bold hover:bg-slate-600 transition-colors">
                MANUEL
              </button>
            </div>
          </div>

          {/* Mission TODO List */}
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-md flex-1">
            <h2 className="text-sm font-bold text-slate-300 uppercase mb-3 flex items-center gap-2">
              <ListTodo size={16} className="text-amber-400" />
              Görev Aşamaları
            </h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between bg-emerald-500/10 border border-emerald-500/30 p-2 rounded-lg">
                <span className="text-emerald-400 text-sm font-medium">1. Su Geçişi</span>
                <span className="text-xs bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded">Tamamlandı</span>
              </div>
              <div className="flex items-center justify-between bg-blue-500/10 border border-blue-500/30 p-2 rounded-lg relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500 animate-pulse"></div>
                <span className="text-blue-400 text-sm font-medium pl-2">2. Taşlı / Çakıllı Yol</span>
                <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded animate-pulse">Aktif</span>
              </div>
              <div className="flex items-center justify-between bg-slate-900 border border-slate-700 p-2 rounded-lg opacity-60">
                <span className="text-slate-400 text-sm">3. Yan Eğim</span>
                <span className="text-xs bg-slate-800 text-slate-500 px-2 py-0.5 rounded">Bekliyor</span>
              </div>
              <div className="flex items-center justify-between bg-slate-900 border border-slate-700 p-2 rounded-lg opacity-60">
                <span className="text-slate-400 text-sm">4. Dik Engel</span>
                <span className="text-xs bg-slate-800 text-slate-500 px-2 py-0.5 rounded">Bekliyor</span>
              </div>
            </div>
          </div>

          {/* Telemetry Overview */}
          <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-md">
            <h2 className="text-sm font-bold text-slate-300 uppercase mb-3 flex items-center gap-2">
              <Zap size={16} className="text-yellow-400" />
              Telemetri
            </h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-900 p-3 rounded-lg border border-slate-700">
                <span className="text-xs text-slate-500 block mb-1">PİL DURUMU</span>
                <div className="flex items-center gap-2">
                  <Battery size={18} className="text-emerald-400" />
                  <span className="font-mono text-lg text-emerald-400">84%</span>
                </div>
              </div>
              <div className="bg-slate-900 p-3 rounded-lg border border-slate-700">
                <span className="text-xs text-slate-500 block mb-1">ARAÇ HIZI</span>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-lg text-slate-200">2.4</span>
                  <span className="text-xs text-slate-400">m/s</span>
                </div>
              </div>
              <div className="bg-slate-900 p-3 rounded-lg border border-slate-700">
                <span className="text-xs text-slate-500 block mb-1">PITCH</span>
                <span className="font-mono text-lg text-slate-200">+4.2°</span>
              </div>
              <div className="bg-slate-900 p-3 rounded-lg border border-slate-700">
                <span className="text-xs text-slate-500 block mb-1">ROLL</span>
                <span className="font-mono text-lg text-slate-200">-1.1°</span>
              </div>
            </div>
          </div>

        </div>

        {/* Center & Right Column: Cameras and Target */}
        <div className="col-span-9 flex flex-col gap-4">
          
          {/* Main Camera Feed */}
          <div className="flex-1 bg-slate-800 rounded-xl border border-slate-700 shadow-md relative overflow-hidden flex flex-col">
            <div className="absolute top-3 left-3 z-10 flex items-center gap-2 bg-black/60 px-2 py-1 rounded backdrop-blur-sm border border-slate-600/50">
              <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
              <span className="text-xs font-mono font-bold text-slate-200">CAM 1: İLERİ SÜRÜŞ / AI OVERLAY</span>
            </div>
            
            {/* Dummy Camera Image / Placeholder */}
            <div className="flex-1 bg-slate-950 flex items-center justify-center relative">
              {/* Overlay elements to simulate AI detection */}
              <div className="absolute top-1/2 left-1/3 w-24 h-32 border-2 border-amber-500 bg-amber-500/10 rounded-sm">
                <div className="absolute -top-6 left-0 bg-amber-500 text-black text-[10px] font-bold px-1 rounded-sm">KAYAR ENGEL (82%)</div>
              </div>
              <div className="absolute top-2/3 right-1/4 w-12 h-16 border-2 border-emerald-500 bg-emerald-500/10 rounded-sm">
                <div className="absolute -top-6 left-0 bg-emerald-500 text-black text-[10px] font-bold px-1 rounded-sm">KONİ (95%)</div>
              </div>

              {/* Crosshair effect overlay */}
              <div className="absolute inset-0 pointer-events-none opacity-20" 
                   style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(90deg, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                   }}>
              </div>
              
              <Camera size={48} className="text-slate-700 absolute opacity-20" />
            </div>

            {/* Sub Cameras Row */}
            <div className="h-40 bg-slate-900 border-t border-slate-700 flex">
              <div className="flex-1 border-r border-slate-700 relative group">
                <div className="absolute top-2 left-2 z-10 text-[10px] font-mono bg-black/60 px-1 rounded text-slate-300">CAM 2: GERİ SÜRÜŞ</div>
                <div className="w-full h-full bg-slate-800 flex items-center justify-center">
                  <span className="text-slate-600 text-xs">YAYIN BEKLENİYOR...</span>
                </div>
              </div>
              <div className="flex-1 relative group">
                <div className="absolute top-2 left-2 z-10 text-[10px] font-mono bg-black/60 px-1 rounded text-amber-400 font-bold flex items-center gap-1">
                  <Crosshair size={10} /> CAM 3: NİŞAN
                </div>
                <div className="w-full h-full bg-slate-800 flex items-center justify-center relative">
                  {/* Fake target scope */}
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-50">
                    <div className="w-20 h-20 rounded-full border border-amber-500 relative">
                      <div className="absolute top-1/2 left-0 right-0 h-[1px] bg-amber-500"></div>
                      <div className="absolute left-1/2 top-0 bottom-0 w-[1px] bg-amber-500"></div>
                    </div>
                  </div>
                  <span className="text-slate-600 text-xs">HEDEF ARANIYOR...</span>
                </div>
              </div>
            </div>
          </div>

          {/* Action Log & Atış Paneli */}
          <div className="h-48 grid grid-cols-3 gap-4 shrink-0">
            
            {/* Karar Log'u */}
            <div className="col-span-2 bg-slate-800 p-3 rounded-xl border border-slate-700 shadow-md flex flex-col">
               <h2 className="text-xs font-bold text-slate-400 uppercase mb-2 flex items-center gap-2">
                <Terminal size={14} />
                Otonomi Karar Logu
              </h2>
              <div className="flex-1 bg-slate-900 rounded border border-slate-700 p-2 overflow-y-auto font-mono text-xs space-y-1">
                <div className="text-emerald-400">[14:21:05] SİSTEM: Otonom mod başlatıldı.</div>
                <div className="text-blue-400">[14:21:08] VISION: Su geçişi tespit edildi, hız 1.5m/s'ye ayarlanıyor.</div>
                <div className="text-slate-400">[14:21:20] NAV: Engel aşıldı, normal seyre dönülüyor.</div>
                <div className="text-amber-400">[14:22:15] VISION: Kayar engel algılandı, güvenli geçiş hesaplanıyor...</div>
                <div className="text-emerald-400 animate-pulse">[14:22:18] NAV: Bekleme stratejisi devrede. 3 sn bekleniyor.</div>
              </div>
            </div>

            {/* Atış Paneli */}
            <div className="bg-slate-800 p-3 rounded-xl border border-slate-700 shadow-md flex flex-col items-center justify-center relative overflow-hidden">
              <div className="absolute top-0 w-full h-1 bg-gradient-to-r from-transparent via-red-500 to-transparent opacity-50"></div>
              <Crosshair size={32} className="text-slate-500 mb-2" />
              <h3 className="text-sm font-bold text-slate-300 mb-1">ATIŞ SİSTEMİ</h3>
              <span className="text-xs text-slate-500 mb-4">Lazer İşaretleyici Beklemede</span>
              
              <button disabled className="w-full bg-slate-700 text-slate-500 py-2 rounded font-bold cursor-not-allowed border border-slate-600">
                LAZERİ ATEŞLE
              </button>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
