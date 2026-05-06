import React, { useState, useEffect } from 'react';
import { 
  Activity, Battery, Camera, Crosshair, ShieldAlert, Wifi, Zap, Terminal, 
  Play, Pause, AlertOctagon, Settings2, ListTodo, Target, Navigation
} from 'lucide-react';

export default function App() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-[#050505] text-neutral-300 p-4 font-mono select-none flex flex-col h-screen overflow-hidden scanlines">
      
      {/* Header */}
      <header className="flex justify-between items-center bg-[#0a0a0a] p-3 tactical-border shadow-[0_0_15px_rgba(0,255,65,0.05)] mb-4 shrink-0">
        <div className="corners-alt"></div>
        <div className="flex items-center space-x-4 ml-2">
          <div className="w-12 h-12 bg-[#00ff41]/10 flex items-center justify-center border border-[#00ff41]/50">
            <Target className="text-[#00ff41] animate-pulse" size={28} />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-[0.2em] text-neutral-100">İKA-GCS <span className="text-[#00ff41]">NEXUS</span></h1>
            <p className="text-[10px] text-[#00ff41]/70 uppercase tracking-widest">Taktik Operasyon Merkezi // SYS_ONLINE</p>
          </div>
        </div>

        <div className="flex space-x-10">
          <div className="flex flex-col items-center">
            <span className="text-[10px] text-neutral-500 mb-1 tracking-widest">GÖREV SÜRESİ</span>
            <span className="text-2xl text-[#ffb000] font-bold tracking-widest">14:23</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-[10px] text-neutral-500 mb-1 tracking-widest">SİSTEM ZAMANI</span>
            <span className="text-2xl text-neutral-300 tracking-widest">{currentTime.toLocaleTimeString('tr-TR', { hour12: false })}</span>
          </div>
        </div>

        <div className="flex items-center space-x-4 mr-2">
          <div className="flex items-center space-x-3 bg-black px-4 py-2 border border-[#00ff41]/30">
            <Wifi className="text-[#00ff41]" size={18} />
            <span className="text-lg font-bold text-[#00ff41]">98%</span>
            <span className="text-[10px] text-[#00ff41]/60">12MS</span>
          </div>
          <button className="bg-[#ff003c]/20 hover:bg-[#ff003c]/40 text-[#ff003c] px-6 py-2 font-bold flex items-center space-x-2 transition-all border border-[#ff003c] shadow-[0_0_10px_rgba(255,0,60,0.3)] active:scale-95 uppercase tracking-widest">
            <AlertOctagon size={20} />
            <span>Acil Durdurma</span>
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <div className="flex-1 grid grid-cols-12 gap-4 min-h-0">
        
        {/* Left Column: Mission & Telemetry */}
        <div className="col-span-3 flex flex-col gap-4 overflow-y-auto pr-1">
          
          {/* Active Mode */}
          <div className="bg-[#0a0a0a] p-4 tactical-border relative">
            <div className="corners-alt"></div>
            <div className="flex items-center justify-between mb-4 border-b border-[#00ff41]/20 pb-2">
              <h2 className="text-xs font-bold text-[#00ff41] uppercase flex items-center gap-2 tracking-widest">
                <Settings2 size={16} />
                Hareket Modu
              </h2>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button className="bg-[#00ff41]/20 border border-[#00ff41] text-[#00ff41] py-2 font-bold hover:bg-[#00ff41]/30 transition-colors tracking-widest shadow-[0_0_10px_rgba(0,255,65,0.2)]">
                OTONOM
              </button>
              <button className="bg-black border border-neutral-700 text-neutral-500 py-2 font-bold hover:border-neutral-500 transition-colors tracking-widest">
                MANUEL
              </button>
            </div>
          </div>

          {/* Mission TODO List */}
          <div className="bg-[#0a0a0a] p-4 tactical-border flex-1 relative">
            <div className="corners-alt"></div>
            <h2 className="text-xs font-bold text-[#ffb000] uppercase mb-3 flex items-center gap-2 border-b border-[#ffb000]/20 pb-2 tracking-widest">
              <ListTodo size={16} />
              Görev Durumu
            </h2>
            <div className="space-y-2 mt-4">
              <div className="flex items-center justify-between bg-[#00ff41]/5 border border-[#00ff41]/30 p-2">
                <span className="text-[#00ff41] text-xs uppercase tracking-wider">1. Su Geçişi</span>
                <span className="text-[10px] bg-[#00ff41] text-black font-bold px-2 py-0.5">TAMAM</span>
              </div>
              <div className="flex items-center justify-between bg-black border border-[#ffb000] p-2 relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#ffb000] animate-pulse"></div>
                <span className="text-[#ffb000] text-xs pl-2 uppercase tracking-wider">2. Taşlı Yol</span>
                <span className="text-[10px] bg-[#ffb000] text-black font-bold px-2 py-0.5 animate-pulse">AKTİF</span>
              </div>
              <div className="flex items-center justify-between bg-black border border-neutral-800 p-2 opacity-60">
                <span className="text-neutral-500 text-xs uppercase tracking-wider">3. Yan Eğim</span>
                <span className="text-[10px] bg-neutral-800 text-neutral-400 px-2 py-0.5">BEKLEME</span>
              </div>
              <div className="flex items-center justify-between bg-black border border-neutral-800 p-2 opacity-60">
                <span className="text-neutral-500 text-xs uppercase tracking-wider">4. Dik Engel</span>
                <span className="text-[10px] bg-neutral-800 text-neutral-400 px-2 py-0.5">BEKLEME</span>
              </div>
            </div>
          </div>

          {/* Telemetry Overview */}
          <div className="bg-[#0a0a0a] p-4 tactical-border relative">
            <div className="corners-alt"></div>
            <h2 className="text-xs font-bold text-[#00ff41] uppercase mb-3 flex items-center gap-2 border-b border-[#00ff41]/20 pb-2 tracking-widest">
              <Activity size={16} />
              Telemetri Verisi
            </h2>
            <div className="grid grid-cols-2 gap-2 mt-4">
              <div className="bg-black p-2 border border-neutral-800">
                <span className="text-[10px] text-neutral-500 block mb-1">BATARYA SEVİYESİ</span>
                <div className="flex items-center gap-2">
                  <Battery size={14} className="text-[#00ff41]" />
                  <span className="text-lg text-[#00ff41] font-bold tracking-wider">84%</span>
                </div>
              </div>
              <div className="bg-black p-2 border border-neutral-800">
                <span className="text-[10px] text-neutral-500 block mb-1">ARAÇ HIZI (M/S)</span>
                <div className="flex items-center gap-2">
                  <span className="text-lg text-neutral-300 font-bold tracking-wider">2.4</span>
                </div>
              </div>
              <div className="bg-black p-2 border border-neutral-800">
                <span className="text-[10px] text-neutral-500 block mb-1">PITCH (EĞİM)</span>
                <span className="text-lg text-neutral-300 font-bold tracking-wider">+4.2°</span>
              </div>
              <div className="bg-black p-2 border border-neutral-800">
                <span className="text-[10px] text-neutral-500 block mb-1">ROLL (YATMA)</span>
                <span className="text-lg text-neutral-300 font-bold tracking-wider">-1.1°</span>
              </div>
            </div>
          </div>

        </div>

        {/* Center & Right Column: Cameras and Target */}
        <div className="col-span-9 flex flex-col gap-4">
          
          {/* Main Camera Feed */}
          <div className="flex-1 bg-black tactical-border relative overflow-hidden flex flex-col">
            <div className="corners-alt"></div>
            <div className="absolute top-2 left-2 z-10 flex items-center gap-2 bg-black/80 px-2 py-1 border border-[#00ff41]/30">
              <div className="w-2 h-2 bg-[#ff003c] animate-pulse"></div>
              <span className="text-[10px] text-[#00ff41] tracking-widest">CAM_01_FWD // AI_OVERLAY_ACTIVE</span>
            </div>
            
            <div className="absolute top-2 right-2 z-10 text-[10px] text-[#00ff41] bg-black/80 px-2 py-1 border border-[#00ff41]/30 tracking-widest">
              REC ●
            </div>

            {/* Dummy Camera Image / Placeholder */}
            <div className="flex-1 flex items-center justify-center relative bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-neutral-900 to-black">
              {/* Tactical Crosshair Background */}
              <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-30">
                <div className="w-full h-[1px] bg-[#00ff41]/40 absolute"></div>
                <div className="h-full w-[1px] bg-[#00ff41]/40 absolute"></div>
                <div className="w-64 h-64 border border-[#00ff41]/40 rounded-full absolute"></div>
              </div>

              {/* Overlay elements to simulate AI detection */}
              <div className="absolute top-1/2 left-1/3 w-24 h-32 border border-[#ffb000] bg-[#ffb000]/10 flex flex-col justify-end">
                <div className="bg-[#ffb000] text-black text-[9px] font-bold px-1 uppercase tracking-widest">TGT: ENGEL (82%)</div>
              </div>
              <div className="absolute top-2/3 right-1/4 w-12 h-16 border border-[#00ff41] bg-[#00ff41]/10 flex flex-col justify-end">
                <div className="bg-[#00ff41] text-black text-[9px] font-bold px-1 uppercase tracking-widest">TGT: KONİ (95%)</div>
              </div>
              
              <Camera size={64} className="text-[#00ff41]/10 absolute" />
            </div>

            {/* Sub Cameras Row */}
            <div className="h-48 bg-black border-t border-[#00ff41]/30 flex">
              <div className="flex-1 border-r border-[#00ff41]/30 relative group bg-neutral-950 flex items-center justify-center">
                <div className="absolute top-2 left-2 z-10 text-[10px] bg-black/80 px-2 py-1 text-neutral-400 border border-neutral-700 tracking-widest">CAM_02_REAR</div>
                <span className="text-neutral-600 text-[10px] tracking-widest uppercase">Sinyal Aranıyor...</span>
              </div>
              <div className="flex-1 relative group bg-[#001a04] flex items-center justify-center overflow-hidden">
                <div className="absolute top-2 left-2 z-10 text-[10px] bg-black/80 px-2 py-1 text-[#ffb000] border border-[#ffb000]/50 tracking-widest font-bold flex items-center gap-2">
                  <Crosshair size={12} /> CAM_03_AIM (NİŞAN)
                </div>
                {/* Fake target scope */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-60">
                  <div className="w-24 h-24 rounded-full border border-[#ffb000] relative">
                    <div className="absolute top-1/2 left-[-10px] right-[-10px] h-[1px] bg-[#ffb000]"></div>
                    <div className="absolute left-1/2 top-[-10px] bottom-[-10px] w-[1px] bg-[#ffb000]"></div>
                    <div className="w-12 h-12 rounded-full border border-[#ffb000]/50 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"></div>
                  </div>
                </div>
                <span className="text-[#ffb000]/40 text-[10px] tracking-widest uppercase mt-16">Hedef Bekleniyor...</span>
              </div>
            </div>
          </div>

          {/* Action Log & Atış Paneli */}
          <div className="h-40 grid grid-cols-3 gap-4 shrink-0">
            
            {/* Karar Log'u */}
            <div className="col-span-2 bg-[#0a0a0a] p-3 tactical-border flex flex-col relative">
               <div className="corners-alt"></div>
               <h2 className="text-[10px] font-bold text-neutral-500 uppercase mb-2 flex items-center gap-2 tracking-widest border-b border-neutral-800 pb-2">
                <Terminal size={12} />
                Sistem Olay Günlüğü
              </h2>
              <div className="flex-1 bg-black border border-neutral-800 p-2 overflow-y-auto text-[10px] space-y-1 tracking-widest leading-relaxed">
                <div className="text-[#00ff41]"><span className="text-neutral-600">[14:21:05]</span> SYS_AUTH: Otonom mod aktif. Sürüş kontrolü devredildi.</div>
                <div className="text-neutral-300"><span className="text-neutral-600">[14:21:08]</span> VISION_CORE: Su geçişi tespit edildi.</div>
                <div className="text-neutral-300"><span className="text-neutral-600">[14:21:08]</span> NAV_CORE: Hız adaptasyonu -> 1.5m/s.</div>
                <div className="text-neutral-300"><span className="text-neutral-600">[14:21:20]</span> NAV_CORE: Engel aşıldı, normal seyre dönülüyor.</div>
                <div className="text-[#ffb000]"><span className="text-neutral-600">[14:22:15]</span> VISION_WARN: Kayar engel algılandı, geçiş penceresi hesaplanıyor...</div>
                <div className="text-[#00ff41] animate-pulse"><span className="text-neutral-600">[14:22:18]</span> NAV_ACTION: Taktik bekleme devrede. (3s)</div>
              </div>
            </div>

            {/* Atış Paneli */}
            <div className="bg-[#0a0a0a] p-3 tactical-border flex flex-col items-center justify-center relative overflow-hidden">
              <div className="corners-alt"></div>
              <div className="absolute top-0 w-full h-1 bg-[#ff003c] opacity-30 shadow-[0_0_10px_#ff003c]"></div>
              
              <Crosshair size={28} className="text-neutral-600 mb-2" />
              <h3 className="text-xs font-bold text-[#ff003c] mb-1 tracking-widest uppercase">Silah Sistemleri</h3>
              <span className="text-[9px] text-neutral-500 mb-4 tracking-widest uppercase text-center">Lazer Modülü Pasif<br/>Hedef Kilitli Değil</span>
              
              <button disabled className="w-full bg-black text-neutral-600 py-3 font-bold cursor-not-allowed border border-neutral-800 tracking-widest uppercase text-[10px]">
                Ateşleme Kilitli
              </button>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
