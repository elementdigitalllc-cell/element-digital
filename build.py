#!/usr/bin/env python3
"""Generate the elementdigital.org static pages from a shared shell."""
import re as _re
def _logo():
    try:
        m = _re.search(r'data:image/png;base64,[A-Za-z0-9+/=]+', open('index.html').read())
        if m:
            return m.group(0)
    except OSError:
        pass
    import base64 as _b64
    return "data:image/png;base64," + _b64.b64encode(open("assets/logo-cube.png", "rb").read()).decode()
LOGO = _logo()

CSS = """
  :root {
    --ink: #111111; --sub: #6b6b6b; --line: #e6e4e8;
    --blue: #4090c0; --yellow: #f0c040; --purple: #7b3fb0; --red: #d04040;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; border-radius: 0; }
  html { scroll-behavior: smooth; }
  body {
    font-family: "Inter", -apple-system, "Helvetica Neue", Arial, sans-serif;
    color: var(--ink); background: #ffffff;
    -webkit-font-smoothing: antialiased; line-height: 1.5;
  }
  .bg {
    position: fixed; inset: 0; z-index: -1;
    background:
      radial-gradient(80rem 55rem at 92% -8%, rgba(64,144,192,0.16), transparent 60%),
      radial-gradient(65rem 48rem at -10% 42%, rgba(123,63,176,0.11), transparent 58%),
      radial-gradient(70rem 48rem at 60% 115%, rgba(240,192,64,0.14), transparent 60%),
      radial-gradient(40rem 30rem at 30% -12%, rgba(208,64,64,0.05), transparent 55%),
      #ffffff;
  }
  .mono {
    font-family: "IBM Plex Mono", "SF Mono", Menlo, monospace;
    font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--sub);
  }
  .label-row { display: flex; align-items: center; gap: 14px; }
  .label-rule { width: 26px; height: 2px; display: inline-block; }
  .wrap { max-width: 1120px; margin: 0 auto; padding: 0 24px; }
  .aside-note { color: var(--sub); font-size: 0.9375rem; }
  .aside-note a { color: var(--ink); }

  .reveal {
    opacity: 0; transform: translateY(32px);
    transition: opacity 0.9s cubic-bezier(0.16,1,0.3,1), transform 0.9s cubic-bezier(0.16,1,0.3,1);
  }
  .reveal.in { opacity: 1; transform: none; }
  .reveal.d1 { transition-delay: 0.1s; }
  .reveal.d2 { transition-delay: 0.2s; }
  .reveal.d3 { transition-delay: 0.3s; }
  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    .reveal { opacity: 1; transform: none; transition: none; }
    .demo *, .corner, .el-wrap { animation: none !important; }
  }

  header {
    position: sticky; top: 0; z-index: 20;
    background: rgba(255,255,255,0.94); border-bottom: 1px solid var(--line);
  }
  .nav { display: flex; align-items: center; justify-content: space-between; height: 64px; }
  .nav-links { display: flex; gap: 4px; }
  .nav-links > div { position: relative; }
  .nav-links a.top {
    color: var(--ink); text-decoration: none; font-size: 0.875rem; font-weight: 500;
    padding: 10px 12px; display: inline-flex; align-items: center; gap: 6px;
  }
  .nav-links a.top:hover { color: var(--sub); }
  .chev { display: block; transition: transform 0.25s ease; }
  .nav-links > div:hover .chev { transform: rotate(180deg); }
  .menu {
    position: absolute; top: 100%; left: 0; min-width: 220px;
    background: #fff; border: 1px solid var(--line); display: none; padding: 6px 0;
  }
  @media (min-width: 701px) {
    .nav-links > div:hover .menu, .nav-links > div:focus-within .menu { display: block; }
  }
  .nav-links > div.open .menu { display: block; }
  .nav-links > div.open .chev { transform: rotate(180deg); }
  .menu a { display: block; padding: 10px 16px; color: var(--ink); text-decoration: none; font-size: 0.875rem; }
  .menu a:hover { background: #f5f4f6; }
  .brand { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--ink); }
  .brand img { height: 22px; width: auto; display: block; }
  .brand span { font-size: 0.875rem; font-weight: 700; letter-spacing: 0.02em; }
  .brand span em { font-style: normal; font-weight: 500; color: var(--sub); }

  .page-head { padding: 96px 0 0; }
  .page-head h1 {
    font-size: clamp(1.9rem, 3.8vw, 2.75rem); letter-spacing: -0.02em;
    font-weight: 650; margin-top: 16px; max-width: 26ch;
  }
  .page-head .lede { margin-top: 20px; color: var(--sub); font-size: 1.0625rem; max-width: 56ch; }

  .cta-frame { position: relative; display: inline-block; padding: 9px; }
  .corner { position: absolute; width: 13px; height: 13px; pointer-events: none; }
  .corner.tl { top: 0; left: 0; border-top: 2px solid var(--ink); border-left: 2px solid var(--ink); animation: drift-tl 2.6s ease-in-out infinite alternate; }
  .corner.tr { top: 0; right: 0; border-top: 2px solid var(--ink); border-right: 2px solid var(--ink); animation: drift-tr 2.6s ease-in-out infinite alternate; }
  .corner.bl { bottom: 0; left: 0; border-bottom: 2px solid var(--ink); border-left: 2px solid var(--ink); animation: drift-bl 2.6s ease-in-out infinite alternate; }
  .corner.br { bottom: 0; right: 0; border-bottom: 2px solid var(--ink); border-right: 2px solid var(--ink); animation: drift-br 2.6s ease-in-out infinite alternate; }
  @keyframes drift-tl { to { transform: translate(-5px,-5px); } }
  @keyframes drift-tr { to { transform: translate(5px,-5px); } }
  @keyframes drift-bl { to { transform: translate(-5px,5px); } }
  @keyframes drift-br { to { transform: translate(5px,5px); } }
  .cta-frame:hover .corner { animation: none; transform: translate(0,0); }
  .cta {
    position: relative; display: inline-flex; align-items: center; gap: 12px;
    background: var(--ink); color: #fff; font-size: 0.9375rem; font-weight: 600;
    padding: 16px 30px; text-decoration: none; border: 1px solid var(--ink); overflow: hidden;
  }
  .cta .arr { display: inline-block; transition: transform 0.3s cubic-bezier(0.16,1,0.3,1); }
  .cta:hover .arr { transform: translateX(6px); }
  .cta::after {
    content: ""; position: absolute; left: 0; bottom: 0; height: 2px; width: 100%;
    background: linear-gradient(90deg, var(--blue), var(--purple), var(--red), var(--yellow));
    transform: translateX(-101%); transition: transform 0.45s cubic-bezier(0.16,1,0.3,1);
  }
  .cta:hover::after { transform: translateX(0); }
  .plain-link {
    color: var(--ink); text-decoration: none; font-size: 0.9375rem; font-weight: 500;
    border-bottom: 1px solid var(--ink); padding-bottom: 2px;
  }
  .plain-link:hover { color: var(--sub); border-color: var(--sub); }

  /* centered intro */
  .intro-c { padding: 92px 0 84px; text-align: center; }
  .elements { display: flex; justify-content: center; gap: 18px; margin-bottom: 40px; flex-wrap: wrap; }
  .el-wrap { animation: el-bob 5s ease-in-out infinite; }
  .el-wrap:nth-child(2) { animation-delay: 0.6s; }
  .el-wrap:nth-child(3) { animation-delay: 1.2s; }
  .el-wrap:nth-child(4) { animation-delay: 1.8s; }
  @keyframes el-bob { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }
  .el {
    width: 96px; height: 96px;
    border: 1px solid var(--ink); background: #fff;
    display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px;
    text-decoration: none; color: var(--ink);
    position: relative;
    transition: background 0.2s ease, color 0.2s ease, transform 0.25s cubic-bezier(0.16,1,0.3,1);
  }
  .el::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
  .el .sym { font-size: 1.7rem; font-weight: 650; letter-spacing: -0.02em; line-height: 1; }
  .el .nm {
    font-family: "IBM Plex Mono", monospace; font-size: 0.5625rem;
    letter-spacing: 0.08em; text-transform: uppercase; color: var(--sub);
  }
  .el:hover { background: var(--ink); color: #fff; transform: translateY(-4px); }
  .el:hover .nm { color: #cfccd4; }
  .el.q { border-style: dashed; }
  .el-sites::before { background: var(--blue); }
  .el-assist::before { background: var(--purple); }
  .el-sol::before { background: var(--yellow); }
  .el.q::before { background: var(--red); }
  .intro-c h1 {
    font-size: clamp(1.9rem, 3.8vw, 3rem);
    letter-spacing: -0.02em; font-weight: 650; line-height: 1.15;
  }
  .intro-c .sub { margin-top: 16px; color: var(--sub); font-size: 1.0625rem; }
  .intro-c .intro-actions { margin-top: 42px; display: flex; align-items: center; justify-content: center; gap: 32px; }

  .street { border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
  .street svg { display: block; width: 100%; height: auto; }
  .cards { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; padding: 72px 0 0; }
  .card { border: 1px solid var(--line); background: rgba(255,255,255,0.65); padding: 36px; display: flex; flex-direction: column; }
  .card .demo { margin: 26px 0; }
  .card h3 { font-size: 1.3125rem; font-weight: 650; letter-spacing: -0.01em; }
  .card p { margin-top: 10px; color: var(--sub); font-size: 0.9375rem; flex: 1; }
  .card .plain-link { margin-top: 22px; align-self: flex-start; }
  .cards-aside { padding: 28px 0 0; }
  .info { border-top: 1px solid var(--line); margin-top: 88px; padding: 72px 0 88px; }
  .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 48px; margin-top: 48px; }
  .info-grid h3 { font-size: 1.0625rem; font-weight: 600; }
  .info-grid p { margin-top: 8px; color: var(--sub); font-size: 0.9375rem; }
  .cta-band { border-top: 1px solid var(--line); padding: 88px 0 112px; }
  .cta-band h2 { font-size: clamp(1.6rem, 3vw, 2.2rem); letter-spacing: -0.02em; font-weight: 650; max-width: 26ch; }
  .cta-band .cta-frame { margin-top: 40px; }
  .note-band { padding: 88px 0; }
  .note-band .big {
    font-size: clamp(1.35rem, 2.6vw, 1.9rem); font-weight: 600;
    letter-spacing: -0.015em; line-height: 1.35; max-width: 44ch;
  }
  .note-band .big .quiet { color: var(--sub); }

  /* products */
  .product { border-top: 1px solid var(--line); }
  .product .inner { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; padding: 88px 0; align-items: center; }
  .product h2 { font-size: clamp(1.5rem, 2.8vw, 2.1rem); letter-spacing: -0.02em; font-weight: 650; line-height: 1.18; margin-top: 14px; }
  .product .body { margin-top: 18px; color: var(--sub); font-size: 1.0625rem; max-width: 54ch; }
  .product ul { margin-top: 28px; list-style: none; max-width: 54ch; }
  .product li { padding: 13px 0; border-top: 1px solid var(--line); font-size: 0.9375rem; }

  .demo { border: 1px solid var(--line); background: #fff; aspect-ratio: 5 / 4; position: relative; overflow: hidden; }
  .d-web .stage { position: absolute; inset: 0; display: grid; place-items: center; }
  .d-web .frame { width: min(300px, 94%); height: 220px; border: 1px solid var(--ink); background: #fff; display: flex; flex-direction: column; }
  .d-web .chrome { height: 26px; border-bottom: 1px solid var(--line); display: flex; align-items: center; gap: 5px; padding: 0 10px; flex: none; }
  .d-web .chrome i { width: 6px; height: 6px; background: #d4d2d8; display: block; }
  .d-web .chrome-logo { height: 14px; width: auto; margin-left: 8px; }
  .d-web .chrome-label {
    font-family: "IBM Plex Mono", monospace; font-size: 0.625rem;
    letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink); margin-left: 6px;
  }
  .d-web .page { flex: 1; padding: 14px; position: relative; }
  .d-web .blk { position: absolute; transform-origin: left center; }
  .d-web .b-nav  { top: 14px; left: 14px; right: 14px; height: 10px; background: #eceaef; animation: blk 9s infinite; }
  .d-web .b-h1   { top: 40px; left: 14px; width: 55%; height: 22px; background: var(--ink); animation: blk 9s infinite; animation-delay: 0.45s; }
  .d-web .b-t1   { top: 74px; left: 14px; width: 70%; height: 8px; background: #dddbe1; animation: blk 9s infinite; animation-delay: 0.9s; }
  .d-web .b-t2   { top: 88px; left: 14px; width: 62%; height: 8px; background: #dddbe1; animation: blk 9s infinite; animation-delay: 1.15s; }
  .d-web .b-cta  { top: 110px; left: 14px; width: 84px; height: 24px; background: var(--ink); animation: blk 9s infinite; animation-delay: 1.5s; }
  .d-web .b-img  { top: 40px; right: 14px; width: 30%; height: 94px; background: rgba(64,144,192,0.18); border: 1px solid rgba(64,144,192,0.35); animation: blk 9s infinite; animation-delay: 1.85s; }
  .d-web .b-f1   { bottom: 14px; left: 14px; width: 28%; height: 8px; background: #eceaef; animation: blk 9s infinite; animation-delay: 2.2s; }
  .d-web .b-f2   { bottom: 14px; left: 38%; width: 28%; height: 8px; background: #eceaef; animation: blk 9s infinite; animation-delay: 2.4s; }
  @keyframes blk { 0% {opacity:0; transform:scaleX(0)} 5% {opacity:1; transform:scaleX(1)} 82% {opacity:1} 92%,100% {opacity:0} }
  .d-bot .stage { position: absolute; inset: 0; display: grid; place-items: center; }
  .d-bot .chat { width: min(280px, 94%); height: 230px; border: 1px solid var(--ink); background: #fff; display: flex; flex-direction: column; }
  .d-bot .chead { height: 34px; border-bottom: 1px solid var(--line); display: flex; align-items: center; gap: 8px; padding: 0 12px; flex: none; }
  .d-bot .chead img { height: 14px; }
  .d-bot .chead .mono { font-size: 0.625rem; color: var(--ink); }
  .d-bot .chead .dot { width: 6px; height: 6px; background: #3fae5a; margin-left: auto; }
  .d-bot .clog { flex: 1; padding: 12px; display: flex; flex-direction: column; gap: 8px; overflow: hidden; }
  .d-bot .msg { max-width: 78%; font-size: 0.6875rem; line-height: 1.45; padding: 8px 10px; opacity: 0; }
  .d-bot .from-user { align-self: flex-end; border: 1px solid var(--line); color: var(--ink); }
  .d-bot .from-bot  { align-self: flex-start; background: var(--ink); color: #fff; }
  .d-bot .m1 { animation: msg1 10s infinite; }
  .d-bot .typing { align-self: flex-start; display: flex; gap: 4px; padding: 8px 10px; opacity: 0; animation: msgTyping 10s infinite; }
  .d-bot .typing i { width: 5px; height: 5px; background: #b9b6bf; display: block; animation: tw 1s infinite; }
  .d-bot .typing i:nth-child(2) { animation-delay: 0.15s; }
  .d-bot .typing i:nth-child(3) { animation-delay: 0.3s; }
  @keyframes tw { 0%,100% {opacity:0.35} 50% {opacity:1} }
  .d-bot .m2 { animation: msg2 10s infinite; }
  .d-bot .m3 { animation: msg3 10s infinite; }
  .d-bot .m4 { animation: msg4 10s infinite; }
  @keyframes msg1 { 0%,6% {opacity:0; transform:translateY(6px)} 10% {opacity:1; transform:none} 86% {opacity:1} 94%,100% {opacity:0} }
  @keyframes msgTyping { 0%,12% {opacity:0} 15% {opacity:1} 26% {opacity:1} 28% {opacity:0} 100% {opacity:0} }
  @keyframes msg2 { 0%,28% {opacity:0; transform:translateY(6px)} 32% {opacity:1; transform:none} 86% {opacity:1} 94%,100% {opacity:0} }
  @keyframes msg3 { 0%,44% {opacity:0; transform:translateY(6px)} 48% {opacity:1; transform:none} 86% {opacity:1} 94%,100% {opacity:0} }
  @keyframes msg4 { 0%,60% {opacity:0; transform:translateY(6px)} 64% {opacity:1; transform:none} 86% {opacity:1} 94%,100% {opacity:0} }

  /* solutions */
  .sol-grid { margin: 64px 0 0; display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid var(--line); border-left: 1px solid var(--line); }
  .sol { padding: 34px 30px 38px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); background: rgba(255,255,255,0.55); }
  .sol h2 { font-size: 1.0625rem; font-weight: 600; margin-top: 10px; }
  .sol p { margin-top: 8px; color: var(--sub); font-size: 0.875rem; }

  /* pricing */
  .plans { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 56px; }
  .plan {
    border: 1px solid var(--ink); background: #fff;
    padding: 32px; position: relative;
    display: flex; flex-direction: column;
  }
  .plan::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
  .plan.p-sites::before { background: var(--blue); }
  .plan.p-assist::before { background: var(--purple); }
  .plan.p-else { border-style: dashed; }
  .plan.p-else::before { background: var(--red); }
  .plan h2 { font-size: 1.375rem; font-weight: 650; letter-spacing: -0.01em; }
  .plan .for { margin-top: 8px; color: var(--sub); font-size: 0.9375rem; }
  .plan ul { list-style: none; margin-top: 22px; margin-bottom: 26px; }
  .plan li { padding: 11px 0; border-top: 1px solid var(--line); font-size: 0.875rem; }
  .plan .quote-tag {
    margin-top: auto;
    font-family: "IBM Plex Mono", monospace; font-size: 0.8125rem;
    letter-spacing: 0.08em; text-transform: uppercase; font-weight: 500;
    padding-bottom: 16px;
  }
  .plan .go {
    display: block; text-align: center;
    background: var(--ink); color: #fff;
    font-size: 0.9375rem; font-weight: 600;
    padding: 14px 0; text-decoration: none; border: 1px solid var(--ink);
  }
  .plan .go:hover { background: #333; }
  .plan.p-else .go { background: #fff; color: var(--ink); }
  .plan.p-else .go:hover { background: #f5f4f6; }
  .price-points { display: grid; grid-template-columns: repeat(3, 1fr); gap: 48px; margin-top: 48px; }
  .price-points h3 { font-size: 1.0625rem; font-weight: 600; }
  .price-points p { margin-top: 8px; color: var(--sub); font-size: 0.9375rem; }

  /* faq */
  .faq { border-top: 1px solid var(--line); margin-top: 88px; padding: 72px 0 24px; }
  .faq-list { margin-top: 40px; max-width: 760px; }
  .qa { border-bottom: 1px solid var(--line); }
  .qa summary {
    padding: 20px 0; cursor: pointer; list-style: none;
    display: flex; justify-content: space-between; align-items: center; gap: 24px;
    font-weight: 600; font-size: 1rem;
  }
  .qa summary::-webkit-details-marker { display: none; }
  .qa .plus { flex: none; font-size: 1.2rem; font-weight: 500; color: var(--sub); transition: transform 0.25s ease; }
  .qa[open] .plus { transform: rotate(45deg); }
  .qa .a { padding: 0 0 22px; color: var(--sub); font-size: 0.9375rem; max-width: 62ch; }

  /* contact */
  .contact { padding: 72px 0 112px; }
  .contact .inner { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; }
  form { display: grid; gap: 20px; }
  .field label { display: block; font-size: 0.8125rem; font-weight: 600; margin-bottom: 6px; }
  .field input, .field textarea {
    width: 100%; font: inherit; font-size: 0.9375rem; color: var(--ink);
    background: #fff; border: 1px solid #d4d2d8; padding: 12px 14px;
  }
  .field input:focus, .field textarea:focus { outline: none; border-color: var(--ink); }
  .field textarea { min-height: 120px; resize: vertical; }
  form button {
    font: inherit; font-size: 0.9375rem; font-weight: 600; background: var(--ink); color: #fff;
    border: 1px solid var(--ink); padding: 14px 28px; cursor: pointer; justify-self: start;
  }
  form button:hover { background: #333; }
  form button:disabled { opacity: 0.5; cursor: default; }
  .form-status { font-size: 0.9375rem; margin-top: 4px; }
  .form-status.ok { color: #1a7f37; }
  .form-status.err { color: var(--red); }
  .contact-side p { margin-top: 18px; color: var(--sub); max-width: 44ch; }
  .contact-side a { color: var(--ink); }

  /* legal */
  .legal { padding: 24px 0 112px; }
  .legal .prose { max-width: 72ch; }
  .legal h2 { font-size: 1.1875rem; font-weight: 650; margin-top: 44px; }
  .legal p, .legal li { color: var(--sub); font-size: 0.9375rem; margin-top: 12px; }
  .legal ul { margin-top: 6px; padding-left: 20px; }
  .legal a { color: var(--ink); }

  /* chat widget */
  #chat-launch {
    position: fixed; right: 24px; bottom: 24px; z-index: 40;
    height: 48px; padding: 0 18px;
    background: var(--ink); color: #fff; border: 1px solid var(--ink);
    display: flex; align-items: center; gap: 10px;
    font: inherit; font-size: 0.875rem; font-weight: 600;
    cursor: pointer;
  }
  #chat-launch img { height: 18px; }
  #chat-launch:hover { background: #333; }
  #chat-panel {
    position: fixed; right: 24px; bottom: 84px; z-index: 41;
    width: 340px; max-width: calc(100vw - 32px); height: 460px; max-height: calc(100vh - 120px);
    background: #fff; border: 1px solid var(--ink);
    display: none; flex-direction: column;
  }
  #chat-panel.open { display: flex; }
  .cw-head {
    height: 44px; border-bottom: 1px solid var(--line); flex: none;
    display: flex; align-items: center; gap: 8px; padding: 0 14px;
  }
  .cw-head img { height: 16px; }
  .cw-head .mono { font-size: 0.6875rem; color: var(--ink); }
  .cw-head .dot { width: 7px; height: 7px; background: #3fae5a; margin-left: auto; }
  .cw-head button {
    background: none; border: none; font-size: 1.1rem; line-height: 1;
    color: var(--sub); cursor: pointer; padding: 4px; margin-left: 8px;
  }
  .cw-head button:hover { color: var(--ink); }
  .cw-log { flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
  .cw-msg { max-width: 85%; font-size: 0.8125rem; line-height: 1.5; padding: 9px 12px; white-space: pre-wrap; }
  .cw-msg.u { align-self: flex-end; border: 1px solid var(--line); color: var(--ink); }
  .cw-msg.b { align-self: flex-start; background: var(--ink); color: #fff; }
  .cw-msg.b a { color: #fff; }
  .cw-typing { align-self: flex-start; display: flex; gap: 4px; padding: 9px 12px; }
  .cw-typing i { width: 5px; height: 5px; background: #b9b6bf; display: block; animation: tw 1s infinite; }
  .cw-typing i:nth-child(2) { animation-delay: 0.15s; }
  .cw-typing i:nth-child(3) { animation-delay: 0.3s; }
  .cw-input { flex: none; border-top: 1px solid var(--line); display: flex; }
  .cw-input input {
    flex: 1; border: none; padding: 13px 14px; font: inherit; font-size: 0.875rem; color: var(--ink);
  }
  .cw-input input:focus { outline: none; }
  .cw-input button {
    flex: none; border: none; background: var(--ink); color: #fff;
    font: inherit; font-size: 0.875rem; font-weight: 600; padding: 0 18px; cursor: pointer;
  }
  .cw-input button:disabled { opacity: 0.5; }
  @media (max-width: 700px) {
    #chat-launch { right: 16px; bottom: 16px; }
    #chat-panel { right: 16px; bottom: 74px; }
  }

  /* back to top */
  #btt {
    position: fixed; right: 24px; bottom: 88px; z-index: 30;
    width: 44px; height: 44px;
    background: #fff; border: 1px solid var(--ink); color: var(--ink);
    font-size: 1.05rem; display: grid; place-items: center;
    text-decoration: none; cursor: pointer;
    opacity: 0; transform: translateY(10px); pointer-events: none;
    transition: opacity 0.3s ease, transform 0.3s ease, background 0.2s, color 0.2s;
  }
  #btt.show { opacity: 1; transform: none; pointer-events: auto; }
  #btt:hover { background: var(--ink); color: #fff; }

  footer { border-top: 1px solid var(--line); background: #fff; margin-top: 88px; }
  .foot-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; padding: 64px 0; }
  .foot-brand img { height: 24px; }
  .foot-brand .wordmark { display: flex; align-items: center; gap: 10px; }
  .foot-brand .wordmark span { font-size: 0.875rem; font-weight: 700; letter-spacing: 0.02em; }
  .foot-brand .wordmark em { font-style: normal; font-weight: 500; color: var(--sub); }
  .foot-brand p { margin-top: 14px; color: var(--sub); font-size: 0.875rem; max-width: 34ch; }
  .foot-col h4 {
    font-family: "IBM Plex Mono", monospace; font-size: 0.6875rem;
    letter-spacing: 0.08em; text-transform: uppercase; color: var(--sub); font-weight: 500;
  }
  .foot-col ul { list-style: none; margin-top: 16px; }
  .foot-col li { margin-bottom: 10px; }
  .foot-col a { color: var(--ink); text-decoration: none; font-size: 0.875rem; }
  .foot-col a:hover { color: var(--sub); }
  .foot-bottom {
    border-top: 1px solid var(--line); padding: 24px 0;
    display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap;
  }
  .foot-bottom .mono { text-transform: none; letter-spacing: 0.02em; font-size: 0.75rem; }
  .foot-bottom a { color: var(--sub); text-decoration: none; }
  .foot-bottom a:hover { color: var(--ink); }

  @media (max-width: 900px) {
    .sol-grid { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 860px) {
    .cards, .product .inner, .contact .inner { grid-template-columns: 1fr; }
    .product .inner { gap: 40px; }
    .contact .inner { gap: 48px; }
    .info-grid, .price-points { grid-template-columns: 1fr; gap: 32px; }
    .plans { grid-template-columns: 1fr; }
    .foot-grid { grid-template-columns: 1fr 1fr; gap: 40px; }
  }
  @media (max-width: 700px) {
    .nav-links a.top { font-size: 0.8125rem; padding: 10px 7px; }
    .brand span { display: none; }
    .intro-c { padding: 72px 0 64px; }
    .intro-c .intro-actions { flex-direction: column; gap: 24px; }
    .sol-grid { grid-template-columns: 1fr; }
    .foot-grid { grid-template-columns: 1fr; gap: 36px; padding: 48px 0; }
    #btt { right: 16px; bottom: 78px; }
  }

"""

CHEV = '<svg class="chev" width="9" height="6" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'

def header():
    return f"""
<header>
  <div class="wrap nav">
    <nav class="nav-links">
      <div>
        <a class="top" href="products.html">Products {CHEV}</a>
        <div class="menu">
          <a href="products.html#assistant">Element Assistant</a>
          <a href="products.html#sites">Element Sites</a>
        </div>
      </div>
      <div>
        <a class="top" href="solutions.html">Solutions {CHEV}</a>
        <div class="menu">
          <a href="solutions.html#sol-restaurants">Restaurants &amp; caf&eacute;s</a>
          <a href="solutions.html#sol-salons">Salons &amp; barbershops</a>
          <a href="solutions.html#sol-home">Home services &amp; trades</a>
          <a href="solutions.html#sol-retail">Retail &amp; boutiques</a>
          <a href="solutions.html">All solutions</a>
        </div>
      </div>
      <div><a class="top" href="pricing.html">Pricing</a></div>
      <div><a class="top" href="contact.html">Contact</a></div>
    </nav>
    <a class="brand" href="index.html" aria-label="Element Digital">
      <img src="{LOGO}" alt="Element Digital">
      <span>ELEMENT <em>DIGITAL</em></span>
    </a>
  </div>
</header>"""

def footer():
    return f"""
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <div class="wordmark">
          <img src="{LOGO}" alt="Element Digital">
          <span>ELEMENT <em>DIGITAL</em></span>
        </div>
        <p>Websites and chatbots for businesses. Built by us, looked after by us.</p>
      </div>
      <div class="foot-col">
        <h4>Company</h4>
        <ul>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="solutions.html">Solutions</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h4>Legal</h4>
        <ul>
          <li><a href="accessibility.html">Accessibility</a></li>
          <li><a href="cookies.html">Cookie Policy</a></li>
          <li><a href="disclaimer.html">Disclaimer</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="privacy.html">Privacy Policy</a></li>
          <li><a href="terms.html">Terms of Service</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h4>Products</h4>
        <ul>
          <li><a href="products.html#assistant">Element Assistant</a></li>
          <li><a href="products.html#sites">Element Sites</a></li>
          <li><a href="pricing.html">Pricing</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span class="mono">&copy; 2026 Element Digital LLC. All rights reserved.</span>
      <a class="mono" href="index.html">elementdigital.org</a>
    </div>
  </div>
</footer>
<a id="btt" href="#" aria-label="Back to top">&uarr;</a>
<button id="chat-launch" aria-label="Chat with Element Assistant">
  <img src="{LOGO}" alt="">
  <span>Chat with us</span>
</button>
<div id="chat-panel" role="dialog" aria-label="Element Assistant chat">
  <div class="cw-head">
    <img src="{LOGO}" alt="">
    <span class="mono">Element Assistant</span>
    <span class="dot"></span>
    <button id="chat-close" aria-label="Close chat">&times;</button>
  </div>
  <div class="cw-log" id="chat-log"></div>
  <div class="cw-input">
    <input id="chat-text" type="text" placeholder="Ask about what we do..." maxlength="500">
    <button id="chat-send">Send</button>
  </div>
</div>"""

BASE_JS = """
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }
  }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  const btt = document.getElementById('btt');
  const onScroll = () => btt.classList.toggle('show', window.scrollY > 600);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  btt.addEventListener('click', (e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });

  const compactNav = window.matchMedia('(max-width: 700px)');
  document.querySelectorAll('.nav-links > div').forEach((d) => {
    const top = d.querySelector('a.top');
    if (!d.querySelector('.menu')) return;
    top.addEventListener('click', (e) => {
      if (!compactNav.matches) return;
      if (!d.classList.contains('open')) {
        e.preventDefault();
        document.querySelectorAll('.nav-links > div.open').forEach((o) => o.classList.remove('open'));
        d.classList.add('open');
      }
    });
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-links')) {
      document.querySelectorAll('.nav-links > div.open').forEach((o) => o.classList.remove('open'));
    }
  });

  const cwPanel = document.getElementById('chat-panel');
  const cwLog = document.getElementById('chat-log');
  const cwText = document.getElementById('chat-text');
  const cwSend = document.getElementById('chat-send');
  const cwHistory = [];
  let cwBusy = false;

  function cwAdd(role, text, asHtml) {
    const div = document.createElement('div');
    div.className = 'cw-msg ' + (role === 'user' ? 'u' : 'b');
    if (asHtml) { div.innerHTML = text; } else { div.textContent = text; }
    cwLog.appendChild(div);
    cwLog.scrollTop = cwLog.scrollHeight;
    return div;
  }

  document.getElementById('chat-launch').addEventListener('click', () => {
    cwPanel.classList.toggle('open');
    if (cwPanel.classList.contains('open')) {
      if (!cwLog.children.length) {
        cwAdd('bot', "Hi, I'm Element Assistant. Ask me anything about what we build or how working with us goes.");
      }
      cwText.focus();
    }
  });
  document.getElementById('chat-close').addEventListener('click', () => cwPanel.classList.remove('open'));

  async function cwSubmit() {
    const q = cwText.value.trim();
    if (!q || cwBusy) return;
    cwText.value = '';
    cwAdd('user', q);
    cwHistory.push({ role: 'user', content: q });
    cwBusy = true;
    cwSend.disabled = true;
    const typing = document.createElement('div');
    typing.className = 'cw-typing';
    typing.innerHTML = '<i></i><i></i><i></i>';
    cwLog.appendChild(typing);
    cwLog.scrollTop = cwLog.scrollHeight;
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: cwHistory })
      });
      const data = await res.json();
      typing.remove();
      if (res.ok && data.reply) {
        cwAdd('bot', data.reply);
        cwHistory.push({ role: 'assistant', content: data.reply });
      } else {
        throw new Error('bad response');
      }
    } catch (err) {
      typing.remove();
      cwAdd('bot', "I am having trouble connecting right now. You can reach us any time through the <a href='contact.html'>contact page</a>.", true);
    } finally {
      cwBusy = false;
      cwSend.disabled = false;
      cwText.focus();
    }
  }
  cwSend.addEventListener('click', cwSubmit);
  cwText.addEventListener('keydown', (e) => { if (e.key === 'Enter') cwSubmit(); });
"""

FORM_JS = """
  const form = document.getElementById('contactForm');
  const status = document.getElementById('formStatus');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = form.name.value.trim();
    const contact = form.contact.value.trim();
    if (!name || !contact) {
      status.textContent = 'Please add your name and a way to reach you.';
      status.className = 'form-status err';
      return;
    }
    const btn = form.querySelector('button');
    btn.disabled = true;
    status.textContent = 'Sending\\u2026';
    status.className = 'form-status';
    try {
      const res = await fetch('https://formsubmit.co/ajax/elementdigitalllc@gmail.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          _subject: 'New lead from elementdigital.org',
          name,
          business: form.business.value.trim(),
          contact,
          message: form.message.value.trim()
        })
      });
      if (!res.ok) throw new Error('bad response');
      form.reset();
      status.textContent = 'Sent. We\\'ll be in touch.';
      status.className = 'form-status ok';
    } catch {
      status.textContent = 'Something went wrong. Email us directly: elementdigitalllc@gmail.com';
      status.className = 'form-status err';
    } finally {
      btn.disabled = false;
    }
  });
"""

def page(fname, title, desc, body, script=BASE_JS):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="{LOGO}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="bg" aria-hidden="true"></div>
{header()}
<main>
{body}
</main>
{footer()}
<script>{script}</script>
</body>
</html>
"""
    open(fname, "w").write(html)
    print("wrote", fname, len(html))

def cta(href="contact.html", label="Talk to us"):
    return f"""<div class="cta-frame">
      <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>
      <a class="cta" href="{href}">{label} <span class="arr">&rarr;</span></a>
    </div>"""

def label(text, color):
    return f'<div class="label-row"><span class="label-rule" style="background: var(--{color})"></span><span class="mono">{text}</span></div>'

ELEMENTS_HTML = """<div class="elements" aria-label="What Element Digital builds">
        <span class="el-wrap"><a class="el el-assist" href="products.html#assistant">
          <span class="sym">As</span><span class="nm">Assistant</span>
        </a></span>
        <span class="el-wrap"><a class="el el-sites" href="products.html#sites">
          <span class="sym">St</span><span class="nm">Sites</span>
        </a></span>
        <span class="el-wrap"><a class="el el-sol" href="solutions.html">
          <span class="sym">Sn</span><span class="nm">Solutions</span>
        </a></span>
        <span class="el-wrap"><a class="el q" href="contact.html">
          <span class="sym">?</span><span class="nm">Anything else</span>
        </a></span>
      </div>"""

STREET_SVG = """<svg viewBox="0 0 1120 190" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A row of storefronts">
  <g stroke="#111111" stroke-width="1.5" fill="none">
    <line x1="0" y1="168" x2="1120" y2="168"/>
    <rect x="90" y="58" width="200" height="110" fill="#ffffff"/>
    <rect x="90" y="42" width="200" height="16" fill="#ffffff"/>
    <g fill="#4090c0" stroke="none">
      <polygon points="90,58 115,58 108,74 83,74"/>
      <polygon points="140,58 165,58 158,74 133,74"/>
      <polygon points="190,58 215,58 208,74 183,74"/>
      <polygon points="240,58 265,58 258,74 233,74"/>
      <polygon points="290,58 297,74 272,74 265,58"/>
    </g>
    <rect x="110" y="92" width="70" height="48" fill="#ffffff"/>
    <rect x="216" y="92" width="46" height="76" fill="#ffffff"/>
    <line x1="216" y1="130" x2="262" y2="130"/>
    <line x1="110" y1="116" x2="180" y2="116"/>
    <rect x="330" y="70" width="170" height="98" fill="#ffffff"/>
    <rect x="330" y="52" width="170" height="18" fill="#ffffff"/>
    <rect x="344" y="58" width="142" height="6" fill="#d04040" stroke="none"/>
    <rect x="348" y="98" width="54" height="42" fill="#ffffff"/>
    <rect x="424" y="98" width="42" height="70" fill="#ffffff"/>
    <circle cx="445" cy="134" r="2.5" fill="#111111" stroke="none"/>
    <rect x="540" y="62" width="190" height="106" fill="#ffffff"/>
    <rect x="558" y="80" width="154" height="22" fill="#f0c040" stroke="#111111"/>
    <rect x="558" y="118" width="66" height="50" fill="#ffffff"/>
    <rect x="646" y="118" width="66" height="30" fill="#ffffff"/>
    <line x1="646" y1="133" x2="712" y2="133"/>
    <rect x="770" y="54" width="180" height="114" fill="#ffffff"/>
    <polygon points="770,54 860,34 950,54" fill="#ffffff"/>
    <rect x="788" y="76" width="60" height="14" fill="#7b3fb0" stroke="none"/>
    <rect x="788" y="104" width="60" height="44" fill="#ffffff"/>
    <rect x="872" y="104" width="58" height="64" fill="#ffffff"/>
    <line x1="872" y1="136" x2="930" y2="136"/>
    <line x1="1010" y1="168" x2="1010" y2="128"/>
    <rect x="994" y="96" width="32" height="32" fill="#ffffff"/>
  </g>
</svg>"""

def demo_web(reveal="reveal d2"):
    return f"""<div class="demo d-web {reveal}" aria-hidden="true">
  <div class="stage">
    <div class="frame">
      <div class="chrome"><i></i><i></i><i></i><img class="chrome-logo" src="{LOGO}" alt=""><span class="chrome-label">element sites</span></div>
      <div class="page">
        <div class="blk b-nav"></div><div class="blk b-h1"></div><div class="blk b-t1"></div>
        <div class="blk b-t2"></div><div class="blk b-cta"></div><div class="blk b-img"></div>
        <div class="blk b-f1"></div><div class="blk b-f2"></div>
      </div>
    </div>
  </div>
</div>"""

def demo_bot(reveal="reveal d2"):
    return f"""<div class="demo d-bot {reveal}" aria-hidden="true">
  <div class="stage">
    <div class="chat">
      <div class="chead">
        <img src="{LOGO}" alt="">
        <span class="mono">Element Assistant</span>
        <span class="dot"></span>
      </div>
      <div class="clog">
        <div class="msg from-user m1">Do you have anything open Saturday?</div>
        <div class="typing"><i></i><i></i><i></i></div>
        <div class="msg from-bot m2">We do. Saturday 10 to 4. Want me to book you in?</div>
        <div class="msg from-user m3">Yes, 11 works.</div>
        <div class="msg from-bot m4">Done. You're booked for Saturday at 11.</div>
      </div>
    </div>
  </div>
</div>"""

# ------- index -------
index_body = f"""
  <section class="intro-c">
    <div class="wrap">
      {ELEMENTS_HTML}
      <h1 class="reveal in">The elements your business is missing.</h1>
      <p class="sub reveal in d1">A solutions company for businesses. Whatever's costing you customers, we build the fix.</p>
      <div class="intro-actions reveal in d2">
        {cta()}
        <a class="plain-link" href="products.html">See our products</a>
      </div>
    </div>
  </section>

  <div class="street reveal">
    <div class="wrap" style="padding-top: 34px; padding-bottom: 26px;">
      {STREET_SVG}
    </div>
  </div>

  <section>
    <div class="wrap">
      <div class="cards">
        <div class="card reveal">
          {label('Element Assistant', 'purple')}
          {demo_bot(reveal="")}
          <h3>Never miss another customer.</h3>
          <p>An assistant on your site that knows your hours, your services, and your availability. It answers questions, captures leads, and books appointments while you work.</p>
          <a class="plain-link" href="products.html#assistant">See the product</a>
        </div>
        <div class="card reveal d1">
          {label('Element Sites', 'blue')}
          {demo_web(reveal="")}
          <h3>A website that takes your business seriously.</h3>
          <p>Fast, mobile first, and built around what your customers actually look for. Designed and built for you, then looked after long past launch.</p>
          <a class="plain-link" href="products.html#sites">See the product</a>
        </div>
      </div>
      <p class="aside-note cards-aside reveal">Looking for something else? <a href="contact.html">Ask us</a>. If we can solve it, we'll tell you how.</p>
    </div>
  </section>

  <section class="info">
    <div class="wrap">
      {label('Working with us', 'yellow')}
      <div class="info-grid">
        <div class="reveal">
          <h3>Straight answers</h3>
          <p>We look at what you have and tell you what's worth doing and what isn't. No upsell scripts, no jargon.</p>
        </div>
        <div class="reveal d1">
          <h3>Done for you</h3>
          <p>You don't touch hosting, settings, or software. We set everything up and hand you the finished result.</p>
        </div>
        <div class="reveal d2">
          <h3>Ongoing upkeep</h3>
          <p>Hosting, updates, and anything that breaks stays our problem. One message and it's handled.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap">
      <h2 class="reveal">Tell us about your business.</h2>
      <div class="reveal d1">{cta()}</div>
    </div>
  </section>
"""
page("index.html",
     "Element Digital | Websites and chatbots for businesses",
     "Element Digital is a solutions company for businesses. We build clean, fast websites and chatbots that answer customers around the clock.",
     index_body)

# ------- products -------
products_body = f"""
  <section class="page-head">
    <div class="wrap">
      {label('Products', 'blue')}
      <h1 class="reveal in">Built for you. Run by us.</h1>
      <p class="lede reveal in d1">Everything we sell is set up for you and maintained by us. You get the result, not another piece of software to manage.</p>
    </div>
  </section>

  <div class="wrap" style="margin-top: 56px;">
    <section class="product" id="assistant">
      <div class="inner">
        <div>
          {label('Element Assistant', 'purple')}
          <h2 class="reveal">Never miss another customer.</h2>
          <p class="body reveal d1">An assistant on your website that knows your business. Your hours, your services, your availability. It answers questions, captures leads, and books appointments while you're with a customer, off the clock, or asleep.</p>
          <ul>
            <li class="reveal d1">Trained on your business and your tone</li>
            <li class="reveal d2">Books appointments and captures every lead</li>
            <li class="reveal d3">Installed on your site and maintained by us</li>
          </ul>
        </div>
        {demo_bot()}
      </div>
    </section>

    <section class="product" id="sites">
      <div class="inner">
        <div>
          {label('Element Sites', 'blue')}
          <h2 class="reveal">A website that takes your business seriously.</h2>
          <p class="body reveal d1">Most business websites are slow, outdated, or missing entirely. Customers notice before they ever call. We design and build sites that look right on a phone, say what you do, and make it easy to book or get in touch.</p>
          <ul>
            <li class="reveal d1">Designed and built for you, start to finish</li>
            <li class="reveal d2">Fast, mobile first, easy to find on Google</li>
            <li class="reveal d3">Hosting, updates, and upkeep handled by us</li>
          </ul>
        </div>
        {demo_web()}
      </div>
    </section>
  </div>

  <section class="cta-band" style="border-top: 1px solid var(--line); margin-top: 88px;">
    <div class="wrap">
      <h2 class="reveal">Tell us about your business.</h2>
      <div class="reveal d1">{cta()}</div>
      <p class="aside-note reveal d1" style="margin-top: 32px;">Can't find what you're looking for? <a href="contact.html">Ask us anyway</a>.</p>
    </div>
  </section>
"""
page("products.html",
     "Products | Element Digital",
     "Element Sites and Element Assistant. Websites and chatbots built for you and run by us.",
     products_body)

# ------- solutions -------
SOLUTIONS = [
    ("sol-restaurants", "Restaurants &amp; caf&eacute;s", "Fewer phone calls. Fuller tables.",
     "Menus, hours, and reservations on a site that loads fast. The assistant answers “are you open?” and takes bookings while your staff pours coffee."),
    ("sol-salons", "Salons &amp; barbershops", "Appointments book themselves.",
     "Your site shows your work. The assistant fills your chair while your hands are busy. No missed calls, no back and forth."),
    ("sol-home", "Home services &amp; trades", "Look credible. Answer first.",
     "Plumbing, HVAC, electrical, roofing. Jobs go to whoever looks legitimate and responds fastest. Be both."),
    ("sol-retail", "Retail &amp; boutiques", "Every question answered.",
     "Hours, stock, directions, holiday schedules. Customers get an instant answer instead of a voicemail."),
    ("sol-auto", "Auto repair &amp; detailing", "Quotes without the phone tag.",
     "Customers describe the job, the assistant captures it, and you reply with a number. Appointments land on your calendar."),
    ("sol-fitness", "Gyms &amp; fitness studios", "From “what classes?” to signed up.",
     "Schedules, memberships, and trial signups handled on the spot, even when the front desk is empty."),
    ("sol-medical", "Medical &amp; dental offices", "After-hours answers, calmer front desk.",
     "Appointment requests, accepted insurance, directions, and prep questions answered without tying up your staff."),
    ("sol-legal", "Law &amp; accounting firms", "Client intake that never sleeps.",
     "A credible site plus an assistant that qualifies inquiries and books consultations while you're billing hours."),
    ("sol-realestate", "Real estate", "Every inquiry captured.",
     "Listings presented cleanly, showing requests and buyer questions captured the moment interest is highest."),
    ("sol-cleaning", "Cleaning services", "Requests become recurring clients.",
     "Quote requests captured with the details you need, and repeat bookings made effortless."),
    ("sol-landscaping", "Landscaping &amp; lawn care", "Busy season without the missed calls.",
     "When the spring rush hits, every inquiry gets an answer and lands in your queue instead of a competitor's."),
    ("sol-petcare", "Pet care &amp; grooming", "Booked solid, minus the phone.",
     "Appointments, vaccination policies, and new client intake handled while you're elbow deep in suds."),
]

sol_cells = "\n".join(
    f"""      <div class="sol reveal{' d' + str(i % 3) if i % 3 else ''}" id="{sid}">
        <span class="mono">{industry}</span>
        <h2>{head}</h2>
        <p>{body}</p>
      </div>"""
    for i, (sid, industry, head, body) in enumerate(SOLUTIONS)
)

solutions_body = f"""
  <section class="page-head">
    <div class="wrap">
      {label('Solutions', 'yellow')}
      <h1 class="reveal in">Built around how your business actually works.</h1>
      <p class="lede reveal in d1">Different businesses lose customers in different places. Here's where we plug the gaps.</p>
    </div>
  </section>

  <div class="wrap">
    <div class="sol-grid">
{sol_cells}
    </div>
  </div>

  <section class="note-band">
    <div class="wrap">
      <p class="big reveal">Your industry isn't the point. <span class="quiet">If customers search, compare, and ask questions before they buy, this works for you.</span></p>
      <div class="reveal d1" style="margin-top: 36px;">{cta()}</div>
      <p class="aside-note reveal d1" style="margin-top: 32px;">Can't find what you're looking for? <a href="contact.html">Ask us anyway</a>.</p>
    </div>
  </section>
"""
page("solutions.html",
     "Solutions | Element Digital",
     "How Element Digital works for restaurants, salons, trades, retail, fitness, medical offices, and more.",
     solutions_body)

# ------- pricing -------
pricing_body = f"""
  <section class="page-head">
    <div class="wrap">
      {label('Pricing', 'red')}
      <h1 class="reveal in">One straight number.</h1>
      <p class="lede reveal in d1">No packages, no tiers, no surprise line items. Tell us about your business and you get one number for the whole job.</p>
    </div>
  </section>

  <div class="wrap">
    <div class="plans">
      <div class="plan p-assist reveal in">
        <h2>Element Assistant</h2>
        <p class="for">For businesses that miss calls and lose leads.</p>
        <ul>
          <li>Trained on your business and your tone</li>
          <li>Answers questions and captures every lead</li>
          <li>Books appointments while you work</li>
          <li>Retrained whenever your details change</li>
        </ul>
        <div class="quote-tag">Quoted directly</div>
        <a class="go" href="contact.html">Contact us</a>
      </div>
      <div class="plan p-sites reveal in d1">
        <h2>Element Sites</h2>
        <p class="for">For businesses whose website is outdated, slow, or missing.</p>
        <ul>
          <li>Custom design and build, start to finish</li>
          <li>Hosting, SSL, and backups managed by us</li>
          <li>Content updates and fixes, ongoing</li>
          <li>Fast, mobile first, easy to find on Google</li>
        </ul>
        <div class="quote-tag">Quoted directly</div>
        <a class="go" href="contact.html">Contact us</a>
      </div>
      <div class="plan p-else reveal in d2">
        <h2>Anything else</h2>
        <p class="for">Have a different problem? Bring it to us.</p>
        <ul>
          <li>A straight assessment of what's worth doing</li>
          <li>If we can solve it, we tell you how</li>
          <li>If we can't, we say so and point you right</li>
        </ul>
        <div class="quote-tag">Ask us</div>
        <a class="go" href="contact.html">Contact us</a>
      </div>
    </div>
  </div>

  <div class="wrap">
    <section style="margin-top: 88px; border-top: 1px solid var(--line); padding-top: 72px;">
      {label('How quoting works', 'red')}
      <div class="price-points">
        <div class="reveal">
          <h3>Quoted directly</h3>
          <p>One conversation about your business, one number for the whole job. No surprise line items later.</p>
        </div>
        <div class="reveal d1">
          <h3>Nothing starts unpriced</h3>
          <p>You approve the quote before any work begins. If the scope changes, the number changes with your sign-off first.</p>
        </div>
        <div class="reveal d2">
          <h3>Upkeep included</h3>
          <p>Hosting, updates, and fixes are covered as part of the arrangement. You never get billed for a surprise.</p>
        </div>
      </div>
    </section>
  </div>

  <div class="wrap">
    <section class="faq">
      {label('FAQ', 'red')}
      <div class="faq-list">
        <details class="qa">
          <summary>How much does it cost? <span class="plus">+</span></summary>
          <p class="a">Every job is quoted directly. We look at your business, agree on what's worth doing, and give you one number for the whole thing before any work starts.</p>
        </details>
        <details class="qa">
          <summary>Why don't you list prices? <span class="plus">+</span></summary>
          <p class="a">Because every business needs different things. A one-size price list either overcharges you for things you don't need or undercharges and cuts corners. A direct quote does neither.</p>
        </details>
        <details class="qa">
          <summary>What does the quote include? <span class="plus">+</span></summary>
          <p class="a">Everything for that job: design, build, launch, and the ongoing upkeep. Hosting, updates, and fixes are part of the arrangement, not extras.</p>
        </details>
        <details class="qa">
          <summary>Do I need to handle anything technical? <span class="plus">+</span></summary>
          <p class="a">No. We set everything up, run it, and maintain it. You get the results and one point of contact.</p>
        </details>
        <details class="qa">
          <summary>I already have a website. Is that a problem? <span class="plus">+</span></summary>
          <p class="a">Not at all. We'll look at what you have and tell you straight whether it's worth improving or replacing, and the assistant can be added to a site we didn't build.</p>
        </details>
        <details class="qa">
          <summary>Can you help with something that isn't a website or a chatbot? <span class="plus">+</span></summary>
          <p class="a">Bring it to us. Tell us what's costing you customers and we'll tell you whether we can fix it. If we can't, we'll say so and point you to someone who can.</p>
        </details>
        <details class="qa">
          <summary>How do payments work? <span class="plus">+</span></summary>
          <p class="a">Payment terms are part of your quote, including any ongoing amount for hosting and upkeep. Nothing recurring gets added without your sign-off.</p>
        </details>
        <details class="qa">
          <summary>What if I want to stop? <span class="plus">+</span></summary>
          <p class="a">Ongoing arrangements can be ended with written notice as described in your quote. You keep what you've paid for, and we stop billing for what we no longer provide.</p>
        </details>
      </div>
    </section>
  </div>
"""
page("pricing.html",
     "Pricing | Element Digital",
     "No packages and no surprise line items. Element Digital quotes every job directly. You approve the number before anything starts.",
     pricing_body)

# ------- contact -------
contact_body = f"""
  <section class="page-head">
    <div class="wrap">
      {label('Contact', 'red')}
      <h1 class="reveal in">Tell us about your business.</h1>
    </div>
  </section>

  <section class="contact">
    <div class="wrap inner">
      <div class="contact-side">
        <p class="reveal in">Send a note and we'll get back to you. Prefer email? Write to <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a>. Prefer to talk? Leave your number and we'll call.</p>
        <p class="reveal in d1">Not sure if your problem fits what we do? Send it anyway. If we can solve it, we'll tell you how. If we can't, we'll point you somewhere that can.</p>
      </div>
      <form id="contactForm" novalidate class="reveal in d1">
        <div class="field">
          <label for="f-name">Name</label>
          <input id="f-name" name="name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="f-biz">Business</label>
          <input id="f-biz" name="business" type="text" autocomplete="organization">
        </div>
        <div class="field">
          <label for="f-contact">Email or phone</label>
          <input id="f-contact" name="contact" type="text" required>
        </div>
        <div class="field">
          <label for="f-msg">What do you need?</label>
          <textarea id="f-msg" name="message"></textarea>
        </div>
        <button type="submit">Send</button>
        <div class="form-status" id="formStatus" role="status"></div>
      </form>
    </div>
  </section>
"""
page("contact.html",
     "Contact | Element Digital",
     "Tell us about your business. Element Digital replies with straight answers and a direct quote.",
     contact_body, script=BASE_JS + FORM_JS)

# ------- privacy -------
privacy_body = """
  <section class="page-head">
    <div class="wrap">
      <span class="mono">Legal</span>
      <h1>Privacy Policy</h1>
      <p class="lede">Effective July 11, 2026</p>
    </div>
  </section>
  <section class="legal">
    <div class="wrap prose">
      <h2>Who we are</h2>
      <p>Element Digital LLC ("Element Digital", "we", "us") builds websites and chatbots for businesses. This site is elementdigital.org. You can reach us at <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a>.</p>

      <h2>What we collect</h2>
      <p>When you use the contact form, we collect what you type: your name, your business name, your email or phone number, and your message. That's it. We don't require accounts, we don't set our own cookies, and we don't run ad trackers.</p>

      <h2>How we use it</h2>
      <p>We use your contact details to reply to you, prepare quotes, and provide the services you ask for. We do not sell or rent your information to anyone, and we don't add you to marketing lists you didn't ask for.</p>

      <h2>Who processes it</h2>
      <p>A few service providers handle data on our behalf to make this site work:</p>
      <ul>
        <li>FormSubmit delivers contact form messages to our email.</li>
        <li>Cloudflare hosts this site and may log requests (like IP addresses) to serve and protect it.</li>
        <li>Google Fonts serves the typefaces on this site, which involves your browser requesting files from Google.</li>
      </ul>
      <p>Each of these providers has its own privacy policy governing that processing.</p>

      <h2>How long we keep it</h2>
      <p>We keep contact messages in our email for as long as we need them to serve you or as required by law. If you want your information deleted, email us and we'll remove it.</p>

      <h2>Your choices</h2>
      <p>You can contact us by email instead of the form. You can ask us what we have about you, ask us to correct it, or ask us to delete it at any time by writing to <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a>.</p>

      <h2>Children</h2>
      <p>This site is for business owners and is not directed to children under 13. We do not knowingly collect information from children.</p>

      <h2>Changes</h2>
      <p>If we change this policy, we'll update this page and the date at the top. Meaningful changes won't apply retroactively to information we already have without telling you.</p>

      <h2>Contact</h2>
      <p>Questions about this policy: <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a></p>
    </div>
  </section>
"""
page("privacy.html",
     "Privacy Policy | Element Digital",
     "How Element Digital handles the information you share with us.",
     privacy_body)

# ------- terms -------
terms_body = """
  <section class="page-head">
    <div class="wrap">
      <span class="mono">Legal</span>
      <h1>Terms of Service</h1>
      <p class="lede">Effective July 11, 2026</p>
    </div>
  </section>
  <section class="legal">
    <div class="wrap prose">
      <h2>Who these terms cover</h2>
      <p>These terms apply to your use of elementdigital.org and to services provided by Element Digital LLC ("Element Digital", "we", "us"). By using this site or hiring us, you agree to them.</p>

      <h2>Our services</h2>
      <p>We design, build, and maintain websites and chatbots for businesses. Each engagement is defined by a direct quote that describes the work, the price, and any ongoing arrangement. The quote is the agreement for that job; these terms fill in everything the quote doesn't say.</p>

      <h2>Quotes and payment</h2>
      <p>Work begins after you approve a quote. If the scope changes, we re-quote before doing the changed work. Payment terms, including any recurring amounts for hosting or upkeep, are stated in the quote.</p>

      <h2>Your responsibilities</h2>
      <p>You agree to provide accurate information about your business and to only supply content (text, images, logos) that you have the right to use. You're responsible for the accuracy of business details we publish or train an assistant on, and for reviewing them when they change.</p>

      <h2>Ownership</h2>
      <p>You own your business content. When a job is paid in full, you own the deliverables built for you. We retain ownership of our internal tools, templates, and processes used to build them.</p>

      <h2>Chatbot conduct</h2>
      <p>Assistants we build answer based on the information you give us. They can make mistakes. You agree to review your assistant's setup and to tell us promptly when your business details change so we can retrain it.</p>

      <h2>Service and uptime</h2>
      <p>We manage hosting through reputable providers and work to keep your site and assistant online, but we don't guarantee uninterrupted availability and aren't liable for outages caused by third-party providers.</p>

      <h2>Termination</h2>
      <p>Either side can end an ongoing arrangement with written notice as described in the quote. You keep what you've paid for; we stop billing for what we no longer provide.</p>

      <h2>Disclaimer and limitation of liability</h2>
      <p>Services are provided as described in the quote and otherwise "as is". To the extent the law allows, Element Digital's total liability for any claim related to a job is limited to the amount you paid us for that job, and we aren't liable for indirect or consequential damages such as lost profits.</p>

      <h2>Governing law</h2>
      <p>These terms are governed by the laws of the State of New York. Disputes will be handled in the courts located in New York.</p>

      <h2>Changes</h2>
      <p>We may update these terms from time to time. The version on this page applies from its effective date forward; changes don't rewrite agreements already in progress.</p>

      <h2>Contact</h2>
      <p>Questions about these terms: <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a></p>
    </div>
  </section>
"""
page("terms.html",
     "Terms of Service | Element Digital",
     "The terms that govern elementdigital.org and Element Digital's services.",
     terms_body)

# ------- cookies -------
cookies_body = """
  <section class="page-head">
    <div class="wrap">
      <span class="mono">Legal</span>
      <h1>Cookie Policy</h1>
      <p class="lede">Effective July 11, 2026</p>
    </div>
  </section>
  <section class="legal">
    <div class="wrap prose">
      <h2>The short version</h2>
      <p>Element Digital does not set its own cookies on this site. No analytics cookies, no advertising cookies, no tracking pixels. You can browse every page without accepting anything, which is why you don't see a cookie banner.</p>

      <h2>Third-party cookies</h2>
      <p>Two service providers make this site work, and they may set a limited number of strictly functional cookies:</p>
      <ul>
        <li>Cloudflare, which hosts and protects this site, may set security cookies (such as bot protection) that are required to serve the site safely. These do not track you across other websites.</li>
        <li>Google Fonts serves the typefaces on this site. Font requests go to Google's servers, but the Google Fonts API is designed not to set cookies.</li>
      </ul>

      <h2>Managing cookies</h2>
      <p>You can block or delete cookies at any time in your browser settings. Because we don't rely on our own cookies, the site works fine with them disabled.</p>

      <h2>Changes</h2>
      <p>If we ever add tools that use cookies, we'll update this page and the date at the top before they go live.</p>

      <h2>Contact</h2>
      <p>Questions about this policy: <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a></p>
    </div>
  </section>
"""
page("cookies.html",
     "Cookie Policy | Element Digital",
     "Element Digital does not set its own cookies. Here's the full picture.",
     cookies_body)

# ------- disclaimer -------
disclaimer_body = """
  <section class="page-head">
    <div class="wrap">
      <span class="mono">Legal</span>
      <h1>Disclaimer</h1>
      <p class="lede">Effective July 11, 2026</p>
    </div>
  </section>
  <section class="legal">
    <div class="wrap prose">
      <h2>General information only</h2>
      <p>The content on elementdigital.org is provided for general information about our services. It isn't legal, financial, tax, or other professional advice, and you shouldn't rely on it as such.</p>

      <h2>No guaranteed results</h2>
      <p>We build websites and assistants that are designed to win you customers, and we stand behind our work. But every business and market is different, and we can't guarantee specific outcomes such as rankings, traffic, review counts, lead volume, or revenue.</p>

      <h2>Assistant responses</h2>
      <p>Assistants we build answer from the information their business owner provides. Like any automated system, they can occasionally be wrong or out of date. The businesses that use them remain responsible for confirming details like pricing, availability, and bookings.</p>

      <h2>Third-party services and links</h2>
      <p>Our work and this site rely on third-party providers (such as hosting, fonts, and form delivery), and we may link to external websites. We don't control those services or sites and aren't responsible for their content, availability, or practices.</p>

      <h2>Errors and availability</h2>
      <p>We work to keep this site accurate and online, but we make no warranty that it will always be current, complete, or uninterrupted.</p>

      <h2>Contact</h2>
      <p>Questions about this disclaimer: <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a></p>
    </div>
  </section>
"""
page("disclaimer.html",
     "Disclaimer | Element Digital",
     "What elementdigital.org does and doesn't promise.",
     disclaimer_body)

# ------- accessibility -------
accessibility_body = """
  <section class="page-head">
    <div class="wrap">
      <span class="mono">Legal</span>
      <h1>Accessibility</h1>
      <p class="lede">Updated July 11, 2026</p>
    </div>
  </section>
  <section class="legal">
    <div class="wrap prose">
      <h2>Our commitment</h2>
      <p>We want every visitor to be able to use this site, including people who rely on assistive technology. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA.</p>

      <h2>What we've done</h2>
      <ul>
        <li>Semantic HTML structure with proper headings, labels, and landmarks</li>
        <li>Text and interface colors chosen for strong contrast</li>
        <li>Full keyboard navigation, including menus and forms</li>
        <li>Animations automatically disabled for visitors who have reduced motion turned on</li>
        <li>Text that scales cleanly with browser zoom and system font settings</li>
      </ul>

      <h2>Known limitations</h2>
      <p>Some decorative animations and illustrations are hidden from screen readers rather than described in detail, because they don't carry information the text doesn't already provide.</p>

      <h2>Feedback</h2>
      <p>If any part of this site is hard for you to use, tell us and we'll fix it: <a href="mailto:elementdigitalllc@gmail.com">elementdigitalllc@gmail.com</a>. Accessibility is also something we build into every website we make for clients.</p>
    </div>
  </section>
"""
page("accessibility.html",
     "Accessibility | Element Digital",
     "Element Digital's accessibility commitment for elementdigital.org.",
     accessibility_body)


# ------- faq -------
faq_body = f"""
  <section class="page-head">
    <div class="wrap">
      {label('FAQ', 'yellow')}
      <h1 class="reveal in">Questions, answered straight.</h1>
      <p class="lede reveal in d1">If yours isn't here, <a href="contact.html" style="color: var(--ink);">ask us directly</a>. You'll get a real answer either way.</p>
    </div>
  </section>

  <div class="wrap">
    <section class="faq" style="border-top: none; margin-top: 24px; padding-top: 24px;">
      <div class="faq-list" style="margin-top: 0;">
        <details class="qa">
          <summary>What does Element Digital actually do? <span class="plus">+</span></summary>
          <p class="a">We build and run two products: Element Sites, websites built for you and maintained by us, and Element Assistant, an assistant on your site that answers customers and books appointments. We also take on other problems that cost businesses customers. You bring the problem, we quote the fix.</p>
        </details>
        <details class="qa">
          <summary>Do you only work with certain industries? <span class="plus">+</span></summary>
          <p class="a">No. Restaurants, salons, trades, offices, shops. If customers look you up, compare you, and ask questions before they buy, our work applies. See the <a href="solutions.html">solutions page</a> for examples.</p>
        </details>
        <details class="qa">
          <summary>How do we get started? <span class="plus">+</span></summary>
          <p class="a">Send a note through the <a href="contact.html">contact page</a> with a little about your business. We look at what you have, tell you what's worth doing, and give you a straight quote. You decide from there.</p>
        </details>
        <details class="qa">
          <summary>How much does it cost? <span class="plus">+</span></summary>
          <p class="a">Every job is quoted directly. We look at your business, agree on what's worth doing, and give you one number for the whole thing before any work starts.</p>
        </details>
        <details class="qa">
          <summary>Why don't you list prices? <span class="plus">+</span></summary>
          <p class="a">Because every business needs different things. A one-size price list either overcharges you for things you don't need or undercharges and cuts corners. A direct quote does neither.</p>
        </details>
        <details class="qa">
          <summary>What does the quote include? <span class="plus">+</span></summary>
          <p class="a">Everything for that job: design, build, launch, and the ongoing upkeep. Hosting, updates, and fixes are part of the arrangement, not extras.</p>
        </details>
        <details class="qa">
          <summary>Do I need to handle anything technical? <span class="plus">+</span></summary>
          <p class="a">No. We set everything up, run it, and maintain it. You get the results and one point of contact.</p>
        </details>
        <details class="qa">
          <summary>I already have a website. Is that a problem? <span class="plus">+</span></summary>
          <p class="a">Not at all. We'll look at what you have and tell you straight whether it's worth improving or replacing, and the assistant can be added to a site we didn't build.</p>
        </details>
        <details class="qa">
          <summary>Can you help with something that isn't a website or a chatbot? <span class="plus">+</span></summary>
          <p class="a">Bring it to us. Tell us what's costing you customers and we'll tell you whether we can fix it. If we can't, we'll say so and point you to someone who can.</p>
        </details>
        <details class="qa">
          <summary>How do payments work? <span class="plus">+</span></summary>
          <p class="a">Payment terms are part of your quote, including any ongoing amount for hosting and upkeep. Nothing recurring gets added without your sign-off.</p>
        </details>
        <details class="qa">
          <summary>What if I want to stop? <span class="plus">+</span></summary>
          <p class="a">Ongoing arrangements can be ended with written notice as described in your quote. You keep what you've paid for, and we stop billing for what we no longer provide.</p>
        </details>
      </div>
      <div style="margin-top: 56px;">{cta()}</div>
    </section>
  </div>
"""
page("faq.html",
     "FAQ | Element Digital",
     "Straight answers about how Element Digital works, quotes, and what's included.",
     faq_body)

print("done")
