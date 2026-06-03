/* Lotus Matrix Engine - Static Stylesheet
   ©2026 Nicholas Desjardins. All Rights Reserved.
   Additional global styles that supplement inline styles in index.html */

* { 
    box-sizing: border-box; 
}

/* Custom scrollbar webkit */
::-webkit-scrollbar { 
    width: 4px; 
    height: 4px; 
}

::-webkit-scrollbar-track { 
    background: #03030a; 
}

::-webkit-scrollbar-thumb { 
    background: #252540; 
    border-radius: 2px; 
}

/* Smooth scroll for anchor links */
html { 
    scroll-behavior: smooth; 
}

/* Mobile bottom-padding safety for fixed elements */
@media (max-width: 768px) {
    body { 
        padding-bottom: 20px; 
    }
}

/* Print - hide interactive chrome */
@media print {
    threat-banner,
    .terminal-overlay,
    .btn-threat,
    .btn-contain,
    .demo-panel { 
        display: none !important; 
    }
}
