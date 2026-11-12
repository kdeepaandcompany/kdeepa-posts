#!/usr/bin/env python3
"""Edits-style reel assembler for K Deepa & Company.
Usage: python3 edits_style.py <workdir> <music.mp3> <out.mp4> [accent_hex]
<workdir> must hold s0.png..sN.png (1080x1920 scene frames), v0.wav..vN.wav (one voice clip per
scene) and texts.json (list of the spoken Devanagari text per scene).
Adds: word-by-word highlighted captions (ASS/libass, Mukta ExtraBold), punch-in zoom at every cut,
original synthesized whoosh on each transition + pop on the hook, music ducking, loudnorm -14.
Fonts: needs /tmp/fonts/mukta-800.ttf (merged from @fontsource mukta devanagari+latin 800 .woff;
see build_fonts() below)."""
import json, os, re, sys, subprocess as sp
import soundfile as sf, numpy as np

def run(*a): sp.run(list(a), check=True)

def build_fonts():
    if os.path.exists('/tmp/fonts/mukta-800.ttf'): return
    from fontTools.ttLib import TTFont
    from fontTools import merge
    os.makedirs('/tmp/fonts', exist_ok=True); parts = []
    for sub in ['devanagari', 'latin']:
        t = TTFont(f'/tmp/node_modules/@fontsource/mukta/files/mukta-{sub}-800-normal.woff'); t.flavor = None
        p = f'/tmp/mukta-{sub}.ttf'; t.save(p); parts.append(p)
    merge.Merger().merge(parts).save('/tmp/fonts/mukta-800.ttf')

def speech_bounds(wav):
    s, sr = sf.read(wav); s = s if s.ndim == 1 else s.mean(1)
    e = np.abs(s) > 0.01 * np.abs(s).max(); idx = np.where(e)[0]
    return (idx[0] / sr, idx[-1] / sr) if len(idx) else (0, len(s) / sr)

def ts(t):
    t = max(t, 0); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'

def groups(text):
    """split into caption groups of <=3 words, breaking at punctuation"""
    out = []
    for phrase in re.split(r'(?<=[,।!?])\s+', text.strip()):
        w = phrase.split()
        ch = [w[i:i + 3] for i in range(0, len(w), 3)]
        if len(ch) > 1 and len(ch[-1]) == 1: last = ch.pop(); ch[-1] += last  # no lonely last word
        out += ch
    return out

def weight(word):
    core = re.sub(r'[,।!?.]', '', word)
    return max(len(core), 2) + (3 if re.search(r'[,।!?]$', word) else 0)  # pause after punctuation

def main(wd, music, out, accent='&H0066D1FF'):
    build_fonts(); os.chdir(wd)
    texts = json.load(open('texts.json')); n = len(texts); X = 0.25
    d = [sf.info(f'v{i}.wav').duration for i in range(n)]
    L = [d[i] + 0.2 + (X if i < n - 1 else 1.0) for i in range(n)]
    starts = [sum(d[j] + 0.2 for j in range(i)) for i in range(n)]
    T = sum(d) + 0.2 * n + 1.0
    # --- scene clips with punch-in zoom (fast 1.10 -> 1.0 in 6 frames, then slow push to 1.04)
    for i in range(n):
        fr = int(round(L[i] * 30))
        run('ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', f's{i}.png', '-vf',
            f"scale=2160:3840,zoompan=z='if(lt(on,6),1.10-0.10*on/6,1+0.04*(on-6)/{fr})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,format=yuv420p",
            '-frames:v', str(fr), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', f'c{i}.mp4')
    inp = []; [inp.extend(['-i', f'c{i}.mp4']) for i in range(n)]
    f = ''; prev = '[0:v]'; off = 0
    for i in range(1, n):
        off += L[i - 1] - X
        f += f"{prev}[{i}:v]xfade=transition=fade:duration={X}:offset={off:.3f}[v{i}];"; prev = f'[v{i}]'
    # --- ASS captions, word-by-word highlight
    ev = []
    for i, text in enumerate(texts):
        if i == n - 1: continue  # contact scene already shows text
        a, b = speech_bounds(f'v{i}.wav'); g = groups(text)
        words = [w for grp in g for w in grp]; W = [weight(w) for w in words]; tot = sum(W)
        t = starts[i] + a; k = 0
        for grp in g:
            for j, w in enumerate(grp):
                dur = (b - a) * W[k] / tot; k += 1
                line = ' '.join((r'{\c' + accent + r'\fscx112\fscy112}' + x + r'{\r}') if q == j else x for q, x in enumerate([g_.replace('।', '') for g_ in grp]))
                ev.append(f'Dialogue: 0,{ts(t)},{ts(t + dur)},Cap,,0,0,0,,{line}'); t += dur
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Mukta,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,8,4,2,80,220,430,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + '\n'.join(ev) + '\n'
    open('caps.ass', 'w').write(ass)
    f += f"{prev}ass=caps.ass:fontsdir=/tmp/fonts[vout]"
    run('ffmpeg', '-y', '-loglevel', 'error', *inp, '-filter_complex', f, '-map', '[vout]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', 'video.mp4')
    # --- voice track
    ins = []; af = ''
    for i in range(n): ins += ['-i', f'v{i}.wav']; af += f'[{i}:a]aresample=44100,apad=whole_dur={d[i] + 0.2:.3f}[a{i}];'
    af += ''.join(f'[a{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,apad=pad_dur=1.0[out]'
    run('ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', af, '-map', '[out]', 'voice.wav')
    # --- original SFX: whoosh (filtered pink noise) + pop (short sine blip)
    run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anoisesrc=color=pink:d=0.4:a=0.6:r=44100',
        '-af', 'bandpass=f=1800:width_type=o:w=2,afade=t=in:d=0.18,afade=t=out:st=0.18:d=0.22,volume=0.9', 'whoosh.wav')
    run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', "aevalsrc='0.8*sin(2*PI*(900-700*t/0.12)*t)*exp(-t*30)':d=0.15:s=44100", 'pop.wav')
    cuts = [starts[i] - X / 2 for i in range(1, n)]
    sfx_in = ['-i', 'pop.wav'] + sum([['-i', 'whoosh.wav'] for _ in cuts], [])
    sf_f = '[0:a]adelay=0|0[p];' + ''.join(f'[{k + 1}:a]adelay={int(c * 1000)}|{int(c * 1000)}[w{k}];' for k, c in enumerate(cuts))
    sf_f += '[p]' + ''.join(f'[w{k}]' for k in range(len(cuts))) + f'amix=inputs={len(cuts) + 1}:normalize=0,apad=whole_dur={T:.3f}[s]'
    run('ffmpeg', '-y', '-loglevel', 'error', *sfx_in, '-filter_complex', sf_f, '-map', '[s]', 'sfx.wav')
    # --- final mix
    run('ffmpeg', '-y', '-loglevel', 'error', '-i', 'video.mp4', '-i', 'voice.wav', '-i', music, '-i', 'sfx.wav', '-filter_complex',
        f"[2:a]atrim=0:{T:.3f},asetpts=PTS-STARTPTS,aresample=44100,volume='if(lt(t,0.8)+gt(t,{T - 1.5:.3f}),0.3,0.13)':eval=frame,afade=t=out:st={T - 1.2:.3f}:d=1.2[m];"
        f"[1:a]aresample=44100[v];[3:a]aresample=44100,volume=0.35[x];[v][m][x]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5,aresample=44100[a]",
        '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out)
    print('done', out, round(T, 2), 's')

if __name__ == '__main__':
    main(*sys.argv[1:])
