import React, { useState, useEffect } from 'react';
import { 
  Activity, Battery, Camera, Crosshair, ShieldAlert, Wifi, Zap, Terminal, 
  Play, Pause, AlertOctagon, Settings2, ListTodo, Target, Navigation, Unlock, Lock
} from 'lucide-react';

export default function App() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isTargeting, setIsTargeting] = useState(false);

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
              <div className="flex items-center justify-between bg-[#22c55e]/20 border border-[#22c55e] p-1.5 lg:p-2 transition-colors">
                <span className="text-[#22c55e] text-[10px] lg:text-xs font-bold uppercase tracking-wider">1. Su Geçişi</span>
                <span className="text-[9px] lg:text-[10px] bg-[#22c55e] text-black font-bold px-1.5 py-0.5">TAMAM</span>
              </div>
              <div className={`flex items-center justify-between p-1.5 lg:p-2 relative overflow-hidden transition-colors ${!isTargeting ? 'bg-[#161412] border-2 border-[#f59e0b]' : 'bg-[#161412] border border-stone-700 opacity-80'}`}>
                {!isTargeting && <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#f59e0b] animate-pulse"></div>}
                <span className={`text-[10px] lg:text-xs font-bold pl-2 uppercase tracking-wider ${!isTargeting ? 'text-[#f59e0b]' : 'text-stone-400'}`}>2. Taşlı Yol</span>
                <span className={`text-[9px] lg:text-[10px] font-bold px-1.5 py-0.5 ${!isTargeting ? 'bg-[#f59e0b] text-black animate-pulse' : 'bg-stone-700 text-stone-300'}`}>
                  {!isTargeting ? 'AKTİF' : 'BEKLEME'}
                </span>
              </div>
              <div className={`flex items-center justify-between p-1.5 lg:p-2 relative overflow-hidden transition-colors ${isTargeting ? 'bg-[#161412] border-2 border-[#f59e0b]' : 'bg-[#161412] border border-stone-700 opacity-80'}`}>
                {isTargeting && <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#f59e0b] animate-pulse"></div>}
                <span className={`text-[10px] lg:text-xs font-bold pl-2 uppercase tracking-wider ${isTargeting ? 'text-[#f59e0b]' : 'text-stone-400'}`}>3. Atış Görevi</span>
                <span className={`text-[9px] lg:text-[10px] font-bold px-1.5 py-0.5 ${isTargeting ? 'bg-[#f59e0b] text-black animate-pulse' : 'bg-stone-700 text-stone-300'}`}>
                  {isTargeting ? 'AKTİF' : 'BEKLEME'}
                </span>
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
                <span className="text-base text-stone-100 font-bold tracking-wider">{isTargeting ? '0.0' : '2.4'}</span>
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
          
          {/* Animated Cameras Container */}
          <div className="flex-1 relative min-h-0 w-full overflow-hidden">
            
            {/* CAM 1 - FWD */}
            <div 
              className={`absolute transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] p-1.5
              ${isTargeting 
                ? 'top-[65%] left-0 w-1/2 h-[35%] opacity-80' 
                : 'top-0 left-0 w-full h-[65%] opacity-100'}`}
            >
              <div className="w-full h-full relative tactical-border flex flex-col justify-center items-center overflow-hidden bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-stone-800 to-[#161412]">
                <div className="corners-alt"></div>
                <div className="absolute top-2 left-2 z-10 flex items-center gap-2 bg-[#2a241c]/90 px-2 py-1 border border-stone-600 shadow-md">
                  <div className={`w-2 h-2 ${isTargeting ? 'bg-stone-500' : 'bg-[#ef4444] animate-pulse'}`}></div>
                  <span className="text-[9px] lg:text-xs font-bold text-stone-200 tracking-widest">CAM_01_FWD</span>
                </div>
                
                {/* Fake AI Overlay - Only visible when large */}
                <div className={`absolute inset-0 transition-opacity duration-300 ${isTargeting ? 'opacity-0' : 'opacity-100'}`}>
                  <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-40">
                    <div className="w-full h-[1px] bg-[#f59e0b]/50 absolute"></div>
                    <div className="h-full w-[1px] bg-[#f59e0b]/50 absolute"></div>
                  </div>
                  <div className="absolute top-1/2 left-1/3 w-20 h-28 border-2 border-[#f59e0b] bg-[#f59e0b]/20 flex flex-col justify-end shadow-[0_0_15px_rgba(245,158,11,0.3)]">
                    <div className="bg-[#f59e0b] text-black text-[9px] font-bold px-1 uppercase tracking-widest">TGT: ENGEL (82%)</div>
                  </div>
                </div>
                <Camera size={48} className="text-stone-600 absolute" />
              </div>
            </div>

            {/* CAM 2 - REAR */}
            <div 
              className={`absolute transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] p-1.5
              ${isTargeting 
                ? 'top-[65%] left-1/2 w-1/2 h-[35%] opacity-80' 
                : 'top-[65%] left-0 w-1/2 h-[35%] opacity-80'}`}
            >
              <div className="w-full h-full relative tactical-border flex flex-col justify-center items-center overflow-hidden bg-[#1e1b18]">
                <div className="absolute top-1 left-1 z-10 text-[9px] lg:text-[10px] font-bold bg-[#2a241c]/90 px-2 py-1 text-stone-300 border border-stone-600 tracking-widest">CAM_02_REAR</div>
                <span className="text-stone-500 text-[9px] lg:text-[11px] font-bold tracking-widest uppercase">Sinyal Aranıyor...</span>
              </div>
            </div>

            {/* CAM 3 - AIM (Targeting) */}
            <div 
              className={`absolute transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] p-1.5
              ${isTargeting 
                ? 'top-0 left-0 w-full h-[65%] opacity-100' 
                : 'top-[65%] left-1/2 w-1/2 h-[35%] opacity-80'}`}
            >
              <div className={`w-full h-full relative tactical-border flex flex-col justify-center items-center overflow-hidden bg-[#1e1b18] transition-all duration-700 ${isTargeting ? 'border-2 border-[#ef4444]/50 shadow-[0_0_30px_rgba(239,68,68,0.15)]' : ''}`}>
                <div className="corners-alt"></div>
                <div className="absolute top-2 left-2 z-10 text-[9px] lg:text-[11px] bg-[#2a241c]/90 px-2 py-1 text-[#f59e0b] border border-[#f59e0b]/50 tracking-widest font-bold flex items-center gap-2 transition-all">
                  <Crosshair size={isTargeting ? 14 : 12} className={isTargeting ? "text-[#ef4444] animate-pulse" : ""} /> CAM_03_AIM
                </div>
                
                {/* Fake target scope - Scales based on state */}
                <div className={`absolute inset-0 flex items-center justify-center pointer-events-none transition-all duration-700 ${isTargeting ? 'opacity-100 scale-125' : 'opacity-60 scale-75'}`}>
                  <div className={`rounded-full border-2 border-[#ef4444] relative transition-all duration-700 ${isTargeting ? 'w-48 h-48 shadow-[0_0_20px_rgba(239,68,68,0.3)]' : 'w-20 h-20'}`}>
                    <div className="absolute top-1/2 left-[-20px] right-[-20px] h-[2px] bg-[#ef4444]"></div>
                    <div className="absolute left-1/2 top-[-20px] bottom-[-20px] w-[2px] bg-[#ef4444]"></div>
                    <div className={`rounded-full border border-[#ef4444]/50 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 transition-all duration-700 ${isTargeting ? 'w-24 h-24' : 'w-10 h-10'}`}></div>
                  </div>
                </div>
                <span className={`text-[#ef4444] font-bold tracking-widest uppercase mt-32 transition-all duration-500 ${isTargeting ? 'text-sm opacity-100' : 'text-[9px] opacity-60'}`}>
                  {isTargeting ? 'HEDEF ARANIYOR...' : 'BEKLEMEDE'}
                </span>
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
                <div className="text-[#f59e0b]"><span className="text-stone-500 mr-2">[14:22:15]</span> VISION_WARN: Kayar engel aşıldı.</div>
                {isTargeting && (
                  <>
                    <div className="text-stone-200"><span className="text-stone-500 mr-2">[14:24:10]</span> NAV_CORE: Atış istasyonuna ulaşıldı. Araç durduruldu.</div>
                    <div className="text-[#ef4444] animate-pulse"><span className="text-stone-500 mr-2">[14:24:11]</span> WPN_SYS: Silah sistemleri devreye alınıyor. Hedef taraması başladı.</div>
                  </>
                )}
              </div>
            </div>

            {/* Atış Paneli */}
            <div className="bg-[#2a241c] p-2 lg:p-3 tactical-border flex flex-col items-center justify-center relative overflow-hidden min-h-0">
              <div className="corners-alt"></div>
              <div className={`absolute top-0 w-full h-1 transition-colors duration-500 ${isTargeting ? 'bg-[#ef4444] opacity-100 shadow-[0_0_20px_#ef4444]' : 'bg-[#f59e0b] opacity-50'}`}></div>
              
              <Crosshair size={24} className={`mb-1 lg:mb-2 transition-colors duration-500 ${isTargeting ? 'text-[#ef4444] animate-pulse' : 'text-stone-400'}`} />
              <h3 className={`text-[10px] lg:text-sm font-bold mb-1 tracking-widest uppercase text-center transition-colors duration-500 ${isTargeting ? 'text-[#ef4444]' : 'text-[#f59e0b]'}`}>Silah Sistemleri</h3>
              <span className={`text-[8px] lg:text-[9px] mb-2 lg:mb-4 tracking-widest font-bold uppercase text-center leading-tight transition-all duration-500 ${isTargeting ? 'text-stone-200' : 'text-stone-500'}`}>
                {isTargeting ? 'Lazer Modülü Aktif\nHedef Aranıyor' : 'Lazer Modülü Pasif\nKilit Yok'}
              </span>
              
              <button 
                onClick={() => setIsTargeting(!isTargeting)}
                className={`w-full py-1.5 lg:py-2 font-bold transition-all duration-300 border-2 tracking-widest uppercase text-[9px] lg:text-xs flex justify-center items-center gap-2
                  ${isTargeting 
                    ? 'bg-[#ef4444]/20 border-[#ef4444] text-[#ef4444] hover:bg-[#ef4444]/40 shadow-[0_0_10px_rgba(239,68,68,0.3)]' 
                    : 'bg-[#161412] text-[#f59e0b] border-stone-700 hover:border-[#f59e0b] cursor-pointer'}`}
              >
                {isTargeting ? <><Unlock size={12}/> Kapat</> : <><Lock size={12}/> Aktifleştir</>}
              </button>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
