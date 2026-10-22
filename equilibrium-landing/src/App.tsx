import { useState, useEffect } from 'react';
import { ChevronDown, Infinity, Menu, X } from 'lucide-react';

const BG_VIDEO =
  'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260511_230229_7c9bc431-46cf-489a-948d-e8144d8eb5d4.mp4';

interface NavLinkItem {
  label: string;
  active?: boolean;
  dropdown?: boolean;
}

const navLinks: NavLinkItem[] = [
  { label: 'Home', active: true },
  { label: 'Wellness', dropdown: true },
  { label: 'Routine' },
  { label: 'Our Team' },
];

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [videoLoaded, setVideoLoaded] = useState(false);
  const [videoError, setVideoError] = useState(false);

  // Close mobile menu on Escape key press
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && menuOpen) {
        setMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [menuOpen]);

  return (
    <div className="relative w-full h-screen overflow-hidden bg-neutral-950 select-none">
      {/* Fallback ambient gradient if video is loading or fails */}
      <div
        className={`absolute inset-0 bg-gradient-to-tr from-neutral-950 via-neutral-900 to-stone-900 transition-opacity duration-1000 ${
          videoLoaded && !videoError ? 'opacity-0' : 'opacity-100'
        }`}
        aria-hidden="true"
      />

      {/* Looping background video */}
      {!videoError && (
        <video
          autoPlay
          muted
          loop
          playsInline
          onLoadedData={() => setVideoLoaded(true)}
          onError={() => setVideoError(true)}
          className="absolute inset-0 w-full h-full object-cover pointer-events-none"
        >
          <source src={BG_VIDEO} type="video/mp4" />
        </video>
      )}

      {/* Subtle dark contrast overlay to ensure foreground text legibility */}
      <div
        className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/35 to-black/30 pointer-events-none"
        aria-hidden="true"
      />

      {/* Navbar */}
      <header className="absolute top-0 left-0 right-0 z-20 flex items-center justify-between px-5 sm:px-8 py-5">
        {/* Left logo */}
        <div className="flex items-center gap-2 text-white font-medium text-base">
          <Infinity size={22} strokeWidth={1.5} />
          <span>Equilibrium</span>
        </div>

        {/* Centered nav pill (Desktop) */}
        <nav
          aria-label="Main Navigation"
          className="hidden md:flex liquid-glass items-center gap-1 rounded-xl px-2 py-2"
        >
          {navLinks.map((link) => (
            <button
              key={link.label}
              type="button"
              className={`flex items-center gap-0.5 px-3 py-1.5 rounded-md text-sm transition-colors ${
                link.active
                  ? 'bg-white/15 text-white'
                  : 'text-white/70 hover:text-white'
              }`}
            >
              <span>{link.label}</span>
              {link.dropdown && <ChevronDown size={13} className="mt-px" />}
            </button>
          ))}
        </nav>

        {/* Desktop CTAs */}
        <div className="hidden md:flex items-center gap-2.5">
          <button
            type="button"
            className="liquid-glass text-white text-sm font-medium px-4 py-2.5 rounded-full hover:bg-white/5 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-white/40"
          >
            Log in
          </button>
          <button
            type="button"
            className="bg-white text-black text-sm font-medium px-4 py-2.5 rounded-full hover:bg-white/90 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-black"
          >
            Begin Now
          </button>
        </div>

        {/* Mobile toggle */}
        <button
          type="button"
          aria-label={menuOpen ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={menuOpen}
          aria-controls="mobile-nav-panel"
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden liquid-glass text-white p-2 rounded-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-white/40"
        >
          {menuOpen ? <X size={18} /> : <Menu size={18} />}
        </button>
      </header>

      {/* Mobile menu panel */}
      {menuOpen && (
        <>
          <div
            className="fixed inset-0 z-20 md:hidden bg-black/40 backdrop-blur-sm"
            onClick={() => setMenuOpen(false)}
            aria-hidden="true"
          />
          <nav
            id="mobile-nav-panel"
            aria-label="Mobile Navigation"
            className="absolute top-[72px] left-4 right-4 z-30 md:hidden liquid-glass rounded-2xl p-4 flex flex-col gap-1 shadow-2xl"
          >
            {navLinks.map((link) => (
              <button
                key={link.label}
                type="button"
                onClick={() => setMenuOpen(false)}
                className={`flex items-center justify-between w-full px-4 py-3 rounded-lg text-sm transition-colors text-left ${
                  link.active
                    ? 'bg-white/15 text-white font-medium'
                    : 'text-white/70 hover:text-white hover:bg-white/5'
                }`}
              >
                <span>{link.label}</span>
                {link.dropdown && <ChevronDown size={14} />}
              </button>
            ))}

            <div className="flex gap-2 mt-2 pt-3 border-t border-white/10">
              <button
                type="button"
                onClick={() => setMenuOpen(false)}
                className="flex-1 liquid-glass text-white text-sm font-medium py-2.5 rounded-full hover:bg-white/5 transition-colors text-center"
              >
                Log in
              </button>
              <button
                type="button"
                onClick={() => setMenuOpen(false)}
                className="flex-1 bg-white text-black text-sm font-medium py-2.5 rounded-full hover:bg-white/90 transition-colors text-center"
              >
                Begin Now
              </button>
            </div>
          </nav>
        </>
      )}

      {/* Hero content */}
      <main className="absolute bottom-0 left-0 z-20 px-6 sm:px-12 pb-10 sm:pb-16 max-w-2xl">
        <h1 className="text-white text-4xl sm:text-5xl lg:text-6xl font-medium leading-tight tracking-tight mb-4">
          Live Better, Feel Whole Every Day
        </h1>
        <p className="text-white/60 text-sm leading-relaxed mb-7 max-w-md">
          Take charge of how you feel with a companion built for your journey—build routines, follow your growth, and unlock tailored insights for a steadier, more vibrant life each day.
        </p>
        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            className="bg-white text-black text-sm sm:text-base font-medium px-6 sm:px-7 py-3 rounded-full hover:bg-white/90 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-white"
          >
            Start Today
          </button>
          <button
            type="button"
            className="liquid-glass text-white text-sm sm:text-base font-medium px-6 sm:px-7 py-3 rounded-full hover:bg-white/5 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-white/40"
          >
            Discover How
          </button>
        </div>
      </main>
    </div>
  );
}
