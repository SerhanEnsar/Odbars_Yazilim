import React, { useState, useEffect, useRef } from 'react';
import { 
  Activity, Battery, Camera, Crosshair, ShieldAlert, Wifi, Zap, Terminal, 
  Play, Pause, AlertOctagon, Settings2, ListTodo, Target, Navigation, Unlock, Lock
} from 'lucide-react';

const Keybox = ({ letter, label, pressed, unassigned, wide }) => {
  return (
    <div className={`flex items-center justify-center font-bold text-[10px] uppercase transition-all duration-100 
      ${wide ? 'w-24' : 'w-8'} h-8 
      ${unassigned 
        ? 'bg-[#161412] text-stone-500 border border-[#f59e0b]/50' // Unassigned: Turuncu çerçeve
        : pressed 
          ? 'bg-[#22c55e] text-black shadow-[0_0_10px_#22c55e] border border-[#22c55e]' 
          : 'bg-[#161412] text-stone-300 border border-[#22c55e]' // Assigned: Yeşil çerçeve
      }`}>
      {label || letter}
    </div>
  );
};

export default function App() {
  const [currentTime, setCurrentTime] = useState(new Date());
  
  // Sürüş Modu ve Tuşlar
  const [driveMode, setDriveMode] = useState("OTONOM");
  const [pressedKeys, setPressedKeys] = useState(new Set());

  // Görev Durumları
  const [taskStatuses, setTaskStatuses] = useState({
    1: 'TAMAM', 2: 'TAMAM', 3: 'AKTİF', 4: 'BEKLEME', 5: 'BEKLEME', 6: 'BEKLEME', 7: 'BEKLEME'
  });
  const [popupMenu, setPopupMenu] = useState({ visible: false, taskId: null, x: 0, y: 0, focusedOptionIndex: 0 });
  const [focusedTaskId, setFocusedTaskId] = useState(null);
  
  // Sistem Logları
  const [logs, setLogs] = useState([
    { id: 1, time: new Date().toLocaleTimeString('tr-TR', { hour12: false }), sender: 'SYS_AUTH', text: 'Sistem başlatıldı. NEXUS Çöl Harekat Merkezi devrede.', type: 'success' }
  ]);
  const logContainerRef = useRef(null);

  const addLog = (sender, text, type = 'info') => {
    setLogs(prev => [...prev, {
      id: Date.now() + Math.random(),
      time: new Date().toLocaleTimeString('tr-TR', { hour12: false }),
      sender,
      text,
      type
    }]);
  };

  // Loglar eklendikçe en alta scroll
  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);
  
  const isTargeting = taskStatuses[7] === 'AKTİF';

  const [telemetry, setTelemetry] = useState({
    battery: 84,
    speed: '0.0',
    pitch: '+0.0',
    roll: '0.0',
    ping: 12
  });

  // Saat, Telemetri ve Klavye Listener
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    let removeListener = null;

    if (window.electronAPI && window.electronAPI.onTelemetryUpdate) {
      removeListener = window.electronAPI.onTelemetryUpdate((data) => {
        setTelemetry(data);
      });
    }

    return () => {
      clearInterval(timer);
      if (removeListener) removeListener();
    };
  }, []);

  useEffect(() => {
    const validKeys = ['w', 'a', 's', 'd', ' '];
    
    const handleKeyDown = (e) => {
      const key = e.key.toLowerCase();
      
      // O/o Tuşu İle Mod Geçişi
      if (key === 'o') {
        const nextMode = driveMode === 'OTONOM' ? 'MANUEL' : 'OTONOM';
        setDriveMode(nextMode);
        if (nextMode === 'OTONOM') {
          setPressedKeys(new Set());
          setFocusedTaskId(null);
          setPopupMenu(p => ({ ...p, visible: false }));
        } else {
          const activeTask = Object.keys(taskStatuses).find(k => taskStatuses[k] === 'AKTİF') || 1;
          setFocusedTaskId(Number(activeTask));
        }
        addLog('SYS_AUTH', `${nextMode} sürüş modu aktifleştirildi.`, nextMode === 'MANUEL' ? 'warning' : 'success');
        return;
      }

      if (driveMode !== 'MANUEL') return;

      // Ok Tuşları Navigasyonu
      if (key === 'arrowup' || key === 'arrowdown') {
        e.preventDefault(); // Sayfanın kaymasını engelle
        if (popupMenu.visible) {
          let newIdx = popupMenu.focusedOptionIndex;
          if (key === 'arrowup') newIdx = Math.max(0, newIdx - 1);
          if (key === 'arrowdown') newIdx = Math.min(2, newIdx + 1);
          setPopupMenu({ ...popupMenu, focusedOptionIndex: newIdx });
        } else {
          let next = focusedTaskId || 1;
          if (key === 'arrowup') next = Math.max(1, next - 1);
          if (key === 'arrowdown') next = Math.min(7, next + 1);
          setFocusedTaskId(next);
        }
        return;
      }

      // Enter Tuşu Onayı
      if (key === 'enter') {
        e.preventDefault();
        if (popupMenu.visible) {
          const options = ['TAMAM', 'AKTİF', 'BEKLEME'];
          updateTaskStatus(popupMenu.taskId, options[popupMenu.focusedOptionIndex]);
        } else if (focusedTaskId) {
          const el = document.getElementById(`task-${focusedTaskId}`);
          let x = window.innerWidth / 2;
          let y = window.innerHeight / 2;
          if (el) {
            const rect = el.getBoundingClientRect();
            x = rect.right - 100;
            y = rect.bottom - 10;
          }
          // Varsayılan olarak "AKTİF" seçeneğini seçili başlat
          setPopupMenu({ visible: true, taskId: focusedTaskId, x, y, focusedOptionIndex: 1 });
        }
        return;
      }

      // Esc Tuşu İptal
      if (key === 'escape') {
        setPopupMenu(p => ({ ...p, visible: false }));
        return;
      }

      // Sürüş Tuşları
      if (validKeys.includes(key)) {
        setPressedKeys(prev => new Set(prev).add(key));
      }
    };

    const handleKeyUp = (e) => {
      const key = e.key.toLowerCase();
      if (driveMode === 'MANUEL' && validKeys.includes(key)) {
        setPressedKeys(prev => {
          const next = new Set(prev);
          next.delete(key);
          return next;
        });
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [driveMode, taskStatuses, popupMenu, focusedTaskId]);

  const updateTaskStatus = (id, status) => {
    setTaskStatuses(prev => {
      const next = { ...prev };
      if (status === 'AKTİF') {
        Object.keys(next).forEach(k => {
          if (next[k] === 'AKTİF') next[k] = 'BEKLEME';
        });
      }
      next[id] = status;
      return next;
    });
    setPopupMenu({ visible: false, taskId: null, x: 0, y: 0, focusedOptionIndex: 0 });

    // Duruma göre log ekle
    const taskNames = {
      1: "Su Geçişi", 2: "Taşlı Yol", 3: "Kayar Engel", 
      4: "Tabela Okuma", 5: "Dik Eğim (Stop)", 6: "Yan Eğim", 7: "Atış Görevi"
    };
    if (status === 'AKTİF') {
      addLog('NAV_CORE', `${taskNames[id]} görevine başlandı.`, 'info');
      if (id === 7) addLog('WPN_SYS', 'Silah sistemleri devreye alınıyor. Hedef taraması başladı.', 'error');
    } else if (status === 'TAMAM') {
      addLog('NAV_CORE', `${taskNames[id]} görevi başarıyla tamamlandı.`, 'success');
    } else {
      addLog('NAV_CORE', `${taskNames[id]} görevi beklemeye alındı.`, 'warning');
    }
  };

  return (
    <div className="h-screen w-screen bg-transparent text-stone-200 p-4 font-mono select-none flex flex-col overflow-hidden scanlines box-border" onClick={() => popupMenu.visible && setPopupMenu({ ...popupMenu, visible: false })}>
      
      {/* Görev Popup Menüsü */}
      {popupMenu.visible && (
        <div 
          className="fixed z-50 bg-[#2a241c] border border-stone-500 shadow-xl p-1 flex flex-col gap-1"
          style={{ top: popupMenu.y, left: popupMenu.x }}
          onClick={(e) => e.stopPropagation()}
          onMouseLeave={() => setPopupMenu({ ...popupMenu, visible: false })}
        >
          <div className="text-[8px] text-stone-400 font-bold px-1 mb-1 border-b border-stone-600 pb-1 uppercase tracking-widest">Durum Seçin</div>
          <button 
            onClick={() => updateTaskStatus(popupMenu.taskId, 'TAMAM')} 
            className={`text-[10px] px-3 py-1 font-bold text-left tracking-widest ${popupMenu.focusedOptionIndex === 0 ? 'bg-[#22c55e] text-black border border-[#22c55e]' : 'bg-[#22c55e]/20 text-[#22c55e] hover:bg-[#22c55e]/40 border border-transparent'}`}
          >
            TAMAM
          </button>
          <button 
            onClick={() => updateTaskStatus(popupMenu.taskId, 'AKTİF')} 
            className={`text-[10px] px-3 py-1 font-bold text-left tracking-widest ${popupMenu.focusedOptionIndex === 1 ? 'bg-[#f59e0b] text-black border border-[#f59e0b]' : 'bg-[#f59e0b]/20 text-[#f59e0b] hover:bg-[#f59e0b]/40 border border-transparent'}`}
          >
            AKTİF
          </button>
          <button 
            onClick={() => updateTaskStatus(popupMenu.taskId, 'BEKLEME')} 
            className={`text-[10px] px-3 py-1 font-bold text-left tracking-widest ${popupMenu.focusedOptionIndex === 2 ? 'bg-stone-300 text-black border border-stone-300' : 'bg-stone-700/50 text-stone-300 hover:bg-stone-600 border border-transparent'}`}
          >
            BEKLEME
          </button>
        </div>
      )}

      {/* Header */}
      <header className="flex justify-between items-center bg-[#2a241c] p-2 lg:p-3 tactical-border shadow-lg mb-3 shrink-0">
        <div className="corners-alt"></div>
        <div className="flex items-center space-x-3 ml-2">
          <div className="w-10 h-10 lg:w-12 h-12 bg-[#f59e0b]/10 flex items-center justify-center border border-[#f59e0b]/50">
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
            <span className="text-[9px] lg:text-[10px] text-[#22c55e]/80">{telemetry.ping}MS</span>
          </div>
          <button 
            onClick={() => addLog('SYS_CRIT', 'ACİL DURDURMA PROTOKOLÜ DEVREDE!', 'error')}
            className="bg-[#ef4444] hover:bg-red-600 text-white px-4 lg:px-6 py-1.5 lg:py-2 font-bold flex items-center space-x-2 transition-all border-2 border-red-300 shadow-[0_0_15px_rgba(239,68,68,0.4)] active:scale-95 uppercase tracking-widest"
          >
            <AlertOctagon size={18} />
            <span className="text-sm lg:text-base">Acil Durdurma</span>
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <div className="flex-1 grid grid-cols-12 gap-3 min-h-0">
        
        {/* Left Column: Mission & Telemetry */}
        <div className="col-span-3 flex flex-col gap-3 h-full min-h-0">
          
          {/* Active Mode & Keyboard Controls */}
          <div className="bg-[#2a241c] p-3 tactical-border relative shrink-0">
            <div className="corners-alt"></div>
            <div className="flex items-center justify-between mb-3 border-b border-stone-600 pb-2">
              <h2 className="text-[10px] lg:text-xs font-bold text-[#f59e0b] uppercase flex items-center gap-2 tracking-widest">
                <Settings2 size={14} />
                Hareket Modu
              </h2>
            </div>
            
            <div className="grid grid-cols-2 gap-2">
              <button 
                onClick={() => { setDriveMode('OTONOM'); setPressedKeys(new Set()); setFocusedTaskId(null); }}
                className={`py-1.5 font-bold transition-colors tracking-widest shadow-md text-xs flex justify-center items-center gap-1 ${driveMode === 'OTONOM' ? 'bg-[#f59e0b] text-black' : 'bg-[#161412] text-stone-400 border border-stone-600 hover:text-stone-200'}`}
              >
                OTONOM <span className="text-[9px] opacity-70">[O]</span>
              </button>
              <button 
                onClick={() => { 
                  setDriveMode('MANUEL'); 
                  const activeTask = Object.keys(taskStatuses).find(k => taskStatuses[k] === 'AKTİF') || 1;
                  setFocusedTaskId(Number(activeTask)); 
                }}
                className={`py-1.5 font-bold transition-colors tracking-widest text-xs flex justify-center items-center gap-1 ${driveMode === 'MANUEL' ? 'bg-[#f59e0b] text-black' : 'bg-[#161412] border border-stone-600 text-stone-400 hover:text-stone-200'}`}
              >
                MANUEL <span className="text-[9px] opacity-70">[O]</span>
              </button>
            </div>

            {/* Klavye Göstergesi */}
            <div className={`mt-3 transition-all duration-300 ${driveMode === 'MANUEL' ? 'opacity-100 min-h-[32px]' : 'opacity-0 h-0 overflow-hidden'}`}>
              <div className="flex justify-center gap-2 flex-wrap">
                {Array.from(pressedKeys).map(key => (
                  <Keybox 
                    key={key} 
                    letter={key === ' ' ? 'FREN' : key} 
                    pressed={true} 
                    wide={key === ' '} 
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Mission TODO List */}
          <div className="bg-[#2a241c] p-3 tactical-border flex-1 min-h-0 overflow-y-auto relative">
            <div className="corners-alt"></div>
            <div className="flex items-center justify-between border-b border-stone-600 pb-2 mb-2">
              <h2 className="text-[10px] lg:text-xs font-bold text-[#f59e0b] uppercase flex items-center gap-2 tracking-widest">
                <ListTodo size={14} />
                Görev Durumu
              </h2>
              <div className="flex gap-2">
                <span className="text-[9px] bg-[#ef4444]/20 text-[#ef4444] px-1 border border-[#ef4444]/50">CEZA: 0</span>
                <span className="text-[9px] bg-stone-700 text-stone-200 px-1 border border-stone-500">PAS: 2</span>
              </div>
            </div>
            
            <div className="space-y-1.5 mt-2 overflow-y-auto pr-1 pb-1 relative">
              {[
                { id: 1, name: "Su Geçişi" },
                { id: 2, name: "Taşlı Yol" },
                { id: 3, name: "Kayar Engel" },
                { id: 4, name: "Tabela Okuma" },
                { id: 5, name: "Dik Eğim (Stop)" },
                { id: 6, name: "Yan Eğim" },
                { id: 7, name: "Atış Görevi" },
              ].map(task => {
                const status = taskStatuses[task.id];
                const isCompleted = status === 'TAMAM';
                const isActive = status === 'AKTİF';
                const isPending = status === 'BEKLEME';
                const isFocused = focusedTaskId === task.id;

                return (
                  <div 
                    id={`task-${task.id}`}
                    key={task.id} 
                    onClick={(e) => {
                      if (driveMode !== 'MANUEL') return;
                      e.stopPropagation();
                      setFocusedTaskId(task.id);
                      const rect = e.currentTarget.getBoundingClientRect();
                      setPopupMenu({ visible: true, taskId: task.id, x: rect.right - 100, y: rect.bottom - 10, focusedOptionIndex: 1 });
                    }}
                    className={`flex items-center justify-between p-1.5 relative overflow-hidden transition-colors ${driveMode === 'MANUEL' ? 'cursor-pointer hover:border-stone-400' : ''}
                      ${isCompleted ? 'bg-[#22c55e]/10 border border-[#22c55e]/50' : ''}
                      ${isActive ? 'bg-[#161412] border-2 border-[#f59e0b]' : ''}
                      ${isPending ? 'bg-[#161412] border border-stone-700 opacity-80' : ''}
                      ${isFocused && driveMode === 'MANUEL' ? 'outline outline-2 outline-[#f59e0b]/80 bg-[#161412]/50' : ''}
                    `}
                  >
                    {isActive && <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#f59e0b] animate-pulse"></div>}
                    
                    <span className={`text-[9px] lg:text-[10px] font-bold uppercase tracking-wider ${isActive ? 'pl-2' : ''}
                      ${isCompleted ? 'text-[#22c55e]' : ''}
                      ${isActive ? 'text-[#f59e0b]' : ''}
                      ${isPending ? 'text-stone-400' : ''}
                    `}>
                      {task.id}. {task.name}
                    </span>
                    
                    <span className={`text-[8px] lg:text-[9px] font-bold px-1.5 py-0.5
                      ${isCompleted ? 'bg-[#22c55e] text-black' : ''}
                      ${isActive ? 'bg-[#f59e0b] text-black animate-pulse' : ''}
                      ${isPending ? 'bg-stone-700 text-stone-300' : ''}
                    `}>
                      {status}
                    </span>
                  </div>
                );
              })}
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
              <div className="bg-[#161412] p-1.5 border border-stone-700 transition-colors">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">BATARYA</span>
                <div className="flex items-center gap-1">
                  <Battery size={12} className={telemetry.battery > 20 ? "text-[#22c55e]" : "text-[#ef4444] animate-pulse"} />
                  <span className={`text-base font-bold tracking-wider ${telemetry.battery > 20 ? "text-[#22c55e]" : "text-[#ef4444]"}`}>
                    {telemetry.battery}%
                  </span>
                </div>
              </div>
              <div className="bg-[#161412] p-1.5 border border-stone-700">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">HIZ (M/S)</span>
                <span className="text-base text-stone-100 font-bold tracking-wider">
                  {telemetry.speed}
                </span>
              </div>
              <div className="bg-[#161412] p-1.5 border border-stone-700">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">PITCH</span>
                <span className="text-base text-stone-100 font-bold tracking-wider">
                  {telemetry.pitch > 0 ? '+' : ''}{telemetry.pitch}°
                </span>
              </div>
              <div className="bg-[#161412] p-1.5 border border-stone-700">
                <span className="text-[9px] text-stone-400 font-bold block mb-0.5">ROLL</span>
                <span className="text-base text-stone-100 font-bold tracking-wider">
                  {telemetry.roll > 0 ? '+' : ''}{telemetry.roll}°
                </span>
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
              <div ref={logContainerRef} className="flex-1 bg-[#161412] border border-stone-700 p-2 overflow-y-auto text-[9px] lg:text-[11px] font-bold space-y-1 lg:space-y-2 tracking-widest leading-relaxed">
                {logs.map(log => {
                  let colorClass = 'text-stone-200';
                  if (log.type === 'success') colorClass = 'text-[#22c55e]';
                  if (log.type === 'warning') colorClass = 'text-[#f59e0b]';
                  if (log.type === 'error') colorClass = 'text-[#ef4444] animate-pulse';
                  
                  return (
                    <div key={log.id} className={colorClass}>
                      <span className="text-stone-500 mr-2">[{log.time}]</span> 
                      {log.sender}: {log.text}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Atış Paneli */}
            <div className="bg-[#2a241c] p-2 lg:p-3 tactical-border flex flex-col items-center justify-center relative overflow-hidden min-h-0">
              <div className="corners-alt"></div>
              <div className={`absolute top-0 w-full h-1 transition-colors duration-500 ${isTargeting ? 'bg-[#ef4444] opacity-100 shadow-[0_0_20px_#ef4444]' : 'bg-[#f59e0b] opacity-50'}`}></div>
              
              <Crosshair size={24} className={`mb-1 lg:mb-2 transition-colors duration-500 ${isTargeting ? 'text-[#ef4444] animate-pulse' : 'text-stone-400'}`} />
              <h3 className={`text-[10px] lg:text-sm font-bold mb-1 tracking-widest uppercase text-center transition-colors duration-500 ${isTargeting ? 'text-[#ef4444]' : 'text-[#f59e0b]'}`}>Silah Sistemleri</h3>
              <span className={`text-[8px] lg:text-[9px] mb-2 lg:mb-4 tracking-widest font-bold uppercase text-center leading-tight transition-all duration-500 ${isTargeting ? 'text-stone-200' : 'text-stone-500'}`}>
                {isTargeting ? 'Lazer Modülü Aktif\nHedef Aranıyor' : 'Sistem Beklemede\nOtonom Sürüş Aktif'}
              </span>
              
              <div 
                className={`w-full py-1.5 lg:py-2 font-bold transition-all duration-300 border-2 tracking-widest uppercase text-[9px] lg:text-xs flex justify-center items-center gap-2
                  ${isTargeting 
                    ? 'bg-[#ef4444]/20 border-[#ef4444] text-[#ef4444] shadow-[0_0_10px_rgba(239,68,68,0.3)]' 
                    : 'bg-[#161412] text-stone-500 border-stone-700'}`}
              >
                {isTargeting ? <><Unlock size={12}/> Mod Açık</> : <><Lock size={12}/> Kapalı</>}
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
