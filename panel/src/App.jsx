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
    <div className="h-screen w-screen bg-transparent text-stone-200 p-4 font-mono select-none flex flex-col overflow-hidden scanlines box-border">
      
      {/* Header */}
      <header className="flex justify-between items-center bg-[#2a241c] p-2 lg:p-3 tactical-border shadow-lg mb-3 shrink-0">
        <div className="corners-alt"></div>
        <div className="flex items-center space-x-3 ml-2">
          <div className="w-10 h-10 lg:w-12 lg:h-12 bg-[#f59e0b]/10 flex items-center justify-center border border-[#f59e0b]/50">
            <Target className="text-[#f59e0b] animate-pulse" size={24} />
          </div>
          <div>
            <h1 className="text-xl lg:text-2xl font-bold tracking-[0.2em] text-stone-100">ODBARS <span className="text-[#f59e0b]">NEXUS</span></h1>
            <p className="text-[9px] lg:text-[10px] text-[#f59e0b] uppercase tracking-widest font-bold">Çöl Askeri Harekat Merkezi // ONLINE</p>
          </div>
        </div>

        <div className="hidden lg:flex space-x-10">
          <div className="flex flex-col items-center">
            <span className="text-[10px] text-stone-400 mb-1 tracking-widest font-bold">GÖREV SÜRESİ</span>
            <span className="text-2xl text-emerald-400 font-bold tracking-widest">14:23</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-[10px] text-stone-400 mb-1 tracking-widest font-bold">SİSTEM ZAMANI</span>
            <span className="text-2xl text-stone-200 tracking-widest font-bold">{currentTime.toLocaleTimeString('tr-TR', { hour12: false })}</span>
          </div>
        </div>

        <div className="flex items-center space-x-3 mr-2">
          <div className="flex items-center space-x-2 bg-[#161412] px-3 py-1.5 border border-[#22c55e]/30">
            <Wifi className="text-[#22c55e]" size={16} />
            <span className="text-base lg:text-lg font-bold text-[#22c55e]">98%</span>
            <span className="text-[9px] lg:text-[10px] text-[#22c55e]/80">12MS</span>
          </div>
          <button className="bg-[#ef4444] hover:bg-red-600 text-white px-4 lg:px-6 py-1.5 lg:py-2 font-bold flex items-center space-x-2 transition-all border-2 border-red-300 shadow-[0_0_15px_rgba(239,68,68,0.4)] active:scale-95 uppercase tracking-widest">
            <AlertOctagon size={18} />
            <span className="text-sm lg:text-base">Acil Durdurma</span>
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <div className="flex-1 grid grid-cols-12 gap-3 min-h-0">
        
        {/* Left Column: Mission & Telemetry */}
        <div className="col-span-3 flex flex-col gap-3 h-full min-h-0">
          
          {/* Active Mode */}
          <div className="bg-[#2a241c] p-3 tactical-border relative shrink-0">
            <div className="corners-alt"></div>
            <div className="flex items-center justify-between mb-3 border-b border-stone-600 pb-2">
              <h2 className="text-[10px] lg:text-xs font-bold text-[#f59e0b] uppercase flex items-center gap-2 tracking-widest">
                <Settings2 size={14} />
                Hareket Modu
              </h2>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <button className="bg-[#f59e0b] text-black py-1.5 font-bold hover:bg-amber-400 transition-colors tracking-widest shadow-md text-xs">
                OTONOM
              </button>
              <button className="bg-[#161412] border border-stone-600 text-stone-400 py-1.5 font-bold hover:text-stone-200 transition-colors tracking-widest text-xs">
                MANUEL
              </button>
            </div>
          </div>

          {/* Mission TODO List */}
          <div className="bg-[#2a241c] p-3 tactical-border flex-1 min-h-0 overflow-y-auto relative">
            <div className="corners-alt"></div>
            <h2 className="text-[10px] lg:text-xs font-bold text-[#f59e0b] uppercase mb-2 flex items-center gap-2 border-b border-stone-600 pb-2 tracking-widest">
              <ListTodo size={14} />
              Görev Durumu
            </h2>
            <div className="space-y-2 mt-2">
              <div className="flex items-center justify-between bg-[#22c55e]/20 border border-[#22c55e] p-1.5 lg:p-2">
                <span className="text-[#22c55e] text-[10px] lg:text-xs font-bold uppercase tracking-wider">1. Su Geçişi</span>
                <span className="text-[9px] lg:text-[10px] bg-[#22c55e] text-black font-bold px-1.5 py-0.5">TAMAM</span>
              </div>
              <div className="flex items-center justify-between bg-[#161412] border-2 border-[#f59e0b] p-1.5 lg:p-2 relative overflow-hidden">
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#f59e0b] animate-pulse"></div>
                <span className="text-[#f59e0b] text-[10px] lg:text-xs font-bold pl-2 uppercase tracking-wider">2. Taşlı Yol</span>
                <span className="text-[9px] lg:text-[10px] bg-[#f59e0b] text-black font-bold px-1.5 py-0.5 animate-pulse">AKTİF</span>
              </div>
              <div className="flex items-center justify-between bg-[#161412] border border-stone-700 p-1.5 lg:p-2 opacity-80">
                <span className="text-stone-400 text-[10px] lg:text-xs font-bold uppercase tracking-wider">3. Yan Eğim</span>
                <span className="text-[9px] lg:text-[10px] bg-stone-700 text-stone-300 font-bold px-1.5 py-0.5">BEKLEME</span>
              </div>
              <div className="flex items-center justify-between bg-[#161412] border border-stone-700 p-1.5 lg:p-2 opacity-80">
                <span className="text-stone-400 text-[10px] lg:text-xs font-bold uppercase tracking-wider">4. Dik Engel</span>
                <span className="text-[9px] lg:text-[10px] bg-stone-700 text-stone-300 font-bold px-1.5 py-0.5">BEKLEME</span>
              </div>
            </div>
          </div>

          {/* Telemetry Overview */}
          <div className="bg-[#2a241c] p-3 tactical-border relative shrink-0">
            <div className="corners-alt"></div>
            <h2 className="text-[10px] lg:text-xs font-bold text-[#f59e0b] uppercase mb-2 flex items-center gap-2 border-b border-stone-600 pb-2 tracking-widest">
              <Activity size={14} />
              Telemetri Verisi
            </h2>
            <div className="grid grid-cols-2 gap-2 mt-2">
              <div className="bg-[#161412] p-1.5 border border-stone-700">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">BATARYA</span>
                <div className="flex items-center gap-1">
                  <Battery size={12} className="text-[#22c55e]" />
                  <span className="text-base text-[#22c55e] font-bold tracking-wider">84%</span>
                </div>
              </div>
              <div className="bg-[#161412] p-1.5 border border-stone-700">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">HIZ (M/S)</span>
                <span className="text-base text-stone-100 font-bold tracking-wider">2.4</span>
              </div>
              <div className="bg-[#161412] p-1.5 border border-stone-700">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">PITCH</span>
                <span className="text-base text-stone-100 font-bold tracking-wider">+4.2°</span>
              </div>
              <div className="bg-[#161412] p-1.5 border border-stone-700">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">ROLL</span>
                <span className="text-base text-stone-100 font-bold tracking-wider">-1.1°</span>
              </div>
            </div>
          </div>

        </div>

        {/* Center & Right Column: Cameras and Target */}
        <div className="col-span-9 flex flex-col gap-3 h-full min-h-0">
          
          {/* Main Camera Feed */}
          <div className="flex-1 bg-[#161412] tactical-border relative overflow-hidden flex flex-col min-h-0">
            <div className="corners-alt"></div>
            <div className="absolute top-2 left-2 z-10 flex items-center gap-2 bg-[#2a241c]/90 px-2 lg:px-3 py-1 lg:py-1.5 border border-stone-600 shadow-md">
              <div className="w-2 h-2 bg-[#ef4444] animate-pulse"></div>
              <span className="text-[10px] lg:text-xs font-bold text-stone-200 tracking-widest">CAM_01_FWD // AI_OVERLAY_ACTIVE</span>
            </div>
            
            <div className="absolute top-2 right-2 z-10 text-[10px] lg:text-xs font-bold text-[#ef4444] bg-[#2a241c]/90 px-2 lg:px-3 py-1 lg:py-1.5 border border-red-500/50 tracking-widest">
              REC ●
            </div>

            {/* Dummy Camera Image / Placeholder */}
            <div className="flex-1 flex items-center justify-center relative bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-stone-800 to-[#161412] min-h-0">
              {/* Tactical Crosshair Background */}
              <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-40">
                <div className="w-full h-[1px] bg-[#f59e0b]/50 absolute"></div>
                <div className="h-full w-[1px] bg-[#f59e0b]/50 absolute"></div>
                <div className="w-48 h-48 lg:w-64 lg:h-64 border-2 border-[#f59e0b]/50 rounded-full absolute"></div>
              </div>

              {/* Overlay elements to simulate AI detection */}
              <div className="absolute top-1/2 left-1/3 w-16 h-24 lg:w-24 lg:h-32 border-2 border-[#f59e0b] bg-[#f59e0b]/20 flex flex-col justify-end shadow-[0_0_15px_rgba(245,158,11,0.3)]">
                <div className="bg-[#f59e0b] text-black text-[8px] lg:text-[10px] font-bold px-1 uppercase tracking-widest">TGT: ENGEL (82%)</div>
              </div>
              <div className="absolute top-2/3 right-1/4 w-8 h-12 lg:w-12 lg:h-16 border-2 border-[#22c55e] bg-[#22c55e]/20 flex flex-col justify-end shadow-[0_0_15px_rgba(34,197,94,0.3)]">
                <div className="bg-[#22c55e] text-black text-[8px] lg:text-[10px] font-bold px-1 uppercase tracking-widest">TGT: KONİ (95%)</div>
              </div>
              
              <Camera size={48} className="text-stone-600 absolute" />
            </div>

            {/* Sub Cameras Row */}
            <div className="h-24 lg:h-36 bg-[#161412] border-t-2 border-stone-700 flex shrink-0">
              <div className="flex-1 border-r-2 border-stone-700 relative group bg-[#1e1b18] flex items-center justify-center min-h-0">
                <div className="absolute top-1 left-1 z-10 text-[9px] lg:text-xs font-bold bg-[#2a241c]/90 px-1 lg:px-2 py-0.5 lg:py-1 text-stone-300 border border-stone-600 tracking-widest">CAM_02_REAR</div>
                <span className="text-stone-500 text-[9px] lg:text-[11px] font-bold tracking-widest uppercase">Sinyal Aranıyor...</span>
              </div>
              <div className="flex-1 relative group bg-[#1e1b18] flex items-center justify-center overflow-hidden min-h-0">
                <div className="absolute top-1 left-1 z-10 text-[9px] lg:text-xs bg-[#2a241c]/90 px-1 lg:px-2 py-0.5 lg:py-1 text-[#f59e0b] border border-[#f59e0b]/50 tracking-widest font-bold flex items-center gap-1 lg:gap-2">
                  <Crosshair size={12} /> CAM_03_AIM
                </div>
                {/* Fake target scope */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-80">
                  <div className="w-16 h-16 lg:w-24 lg:h-24 rounded-full border-2 border-[#ef4444] relative">
                    <div className="absolute top-1/2 left-[-10px] lg:left-[-15px] right-[-10px] lg:right-[-15px] h-[2px] bg-[#ef4444]"></div>
                    <div className="absolute left-1/2 top-[-10px] lg:top-[-15px] bottom-[-10px] lg:bottom-[-15px] w-[2px] bg-[#ef4444]"></div>
                    <div className="w-8 h-8 lg:w-12 lg:h-12 rounded-full border border-[#ef4444]/50 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"></div>
                  </div>
                </div>
                <span className="text-[#ef4444]/60 text-[9px] lg:text-[11px] font-bold tracking-widest uppercase mt-12 lg:mt-20">Hedef Bekleniyor...</span>
              </div>
            </div>
          </div>

          {/* Action Log & Atış Paneli */}
          <div className="h-28 lg:h-36 grid grid-cols-3 gap-3 shrink-0">
            
            {/* Karar Log'u */}
            <div className="col-span-2 bg-[#2a241c] p-2 lg:p-3 tactical-border flex flex-col relative min-h-0">
               <div className="corners-alt"></div>
               <h2 className="text-[10px] lg:text-xs font-bold text-[#f59e0b] uppercase mb-1 lg:mb-2 flex items-center gap-2 tracking-widest border-b border-stone-600 pb-1 lg:pb-2">
                <Terminal size={14} />
                Sistem Olay Günlüğü
              </h2>
              <div className="flex-1 bg-[#161412] border border-stone-700 p-2 overflow-y-auto text-[9px] lg:text-[11px] font-bold space-y-1 lg:space-y-2 tracking-widest leading-relaxed">
                <div className="text-[#22c55e]"><span className="text-stone-500 mr-2">[14:21:05]</span> SYS_AUTH: Otonom mod aktif.</div>
                <div className="text-stone-200"><span className="text-stone-500 mr-2">[14:21:08]</span> VISION_CORE: Su geçişi tespit.</div>
                <div className="text-stone-200"><span className="text-stone-500 mr-2">[14:21:08]</span> NAV_CORE: Hız adapte -&gt; 1.5m/s.</div>
                <div className="text-[#f59e0b]"><span className="text-stone-500 mr-2">[14:22:15]</span> VISION_WARN: Kayar engel algılandı.</div>
                <div className="text-[#f59e0b] animate-pulse"><span className="text-stone-500 mr-2">[14:22:18]</span> NAV_ACTION: Taktik bekleme (3s)</div>
              </div>
            </div>

            {/* Atış Paneli */}
            <div className="bg-[#2a241c] p-2 lg:p-3 tactical-border flex flex-col items-center justify-center relative overflow-hidden min-h-0">
              <div className="corners-alt"></div>
              <div className="absolute top-0 w-full h-1 bg-[#ef4444] opacity-80 shadow-[0_0_15px_#ef4444]"></div>
              
              <Crosshair size={24} className="text-stone-400 mb-1 lg:mb-2" />
              <h3 className="text-[10px] lg:text-sm font-bold text-[#ef4444] mb-1 tracking-widest uppercase text-center">Silah Sistemleri</h3>
              <span className="text-[8px] lg:text-[10px] text-stone-400 mb-2 lg:mb-4 tracking-widest font-bold uppercase text-center leading-tight">Lazer Pasif<br/>Kilit Yok</span>
              
              <button disabled className="w-full bg-[#161412] text-stone-500 py-1.5 lg:py-2 font-bold cursor-not-allowed border-2 border-stone-700 tracking-widest uppercase text-[9px] lg:text-xs">
                KİLİTLİ
              </button>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
