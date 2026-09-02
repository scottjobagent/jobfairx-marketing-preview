#!/usr/bin/env python3
"""Build the JobFairX PRODUCT DEMO from real product screenshots.

Separate from build-video.py (the event-day lobby explainer, owned by the parallel
video session) on purpose: two-session rules say do not edit another stream's files.
Same engine and template; different scene list, different screenshots, different output.

VO text is the FINAL approved script, verbatim (chunk splits affect captions/timing only,
never words). Each scene is ONE steady view of a real screen — at most a slow centered
push-in, never a lateral pan. Timeline derives from measured audio + word boundaries.
"""
import asyncio, base64, json, math, os, re, sys

import edge_tts

VOICE = sys.argv[1] if len(sys.argv) > 1 else 'en-US-EmmaNeural'
VOICE_NAME = re.sub(r'^[a-z]{2}-[A-Z]{2}-|Neural$|Multilingual.*$', '', VOICE)
TEMPLATE = 'demo-template.html'
OUT = 'jobfairx-demo.html'
AUDIO_DIR = 'vo-demo'
ASSETS = '/Users/scottl./Desktop/jobfairx-marketing/assets/product'
GAP = 0.5          # breath between one scene's last word and the next cut
LEAD = 0.4         # VO starts this soon after each cut
IMG_W, IMG_H = 3200, 2000
DESIGN_W = 960
ZOOM = 0.97        # end-of-scene push-in (about the crop center; no lateral movement)

IMAGES = {
    # dashboard: three events, three interview locations, one column
    'dash':      f'{ASSETS}/demo-dash-hc.png',
    # setup: where the employer chooses how they interview
    'setvideo':  f'{ASSETS}/demo-setup-video-hc.png',
    'setperson': f'{ASSETS}/demo-setup-person-hc.png',
    # the two surfaces the old demo predates
    'autos':     f'{ASSETS}/demo-automations-hc.png',
    'analytics': f'{ASSETS}/demo-analytics-hc.png',
    # before the event
    'pre':       f'{ASSETS}/lobby-pre-hc.png',
    'resume':    f'{ASSETS}/demo-resume-hc.png',
    'toast':     f'{ASSETS}/demo-accept-toast-hc.png',
    'lobbylive': f'{ASSETS}/lobby-live-hc.png',
    'prewait':   f'{ASSETS}/lobby-pre-waiting-hc.png',
    # event day, video vs in person
    'lobby':     f'{ASSETS}/lobby-tables-hc.png',
    'lobbyperson': f'{ASSETS}/demo-lobby-person-hc.png',
    'ivg':       f'{ASSETS}/lobby-interviewing-hc.png',
    'ivd':       f'{ASSETS}/lobby-interviewed-hc.png',
    'room':      f'{ASSETS}/room-late-hc.png',
    'recmodal':  f'{ASSETS}/room-recmodal-hc.png',
    # after the event
    'report':    f'{ASSETS}/demo-report-hc.png',
}
from PIL import Image as _Img
IMG_DIMS = {k: _Img.open(v).size for k, v in IMAGES.items()}

# Scene keys: crop (W, ox, oy natural px); callouts = rings (x,y,w,h, capIdx, +delta);
# fx = image-coord effect HTML with __D__ delay placeholder, timed like callouts;
# ov = design-coord overlay HTML (fit dialog); label = on-screen section label.
SCENES = [
    dict(id='s1', title='Interview Location', label='INTERVIEW LOCATION', img='dash',
         crop=(2200, 470, 500),
         # All three cities are named inside ONE spoken chunk, so the rings stagger
         # within that chunk instead of each waiting for a caption of its own.
         callouts=[(1360, 676, 520, 158, 1, 0.4),
                   (1360, 994, 520, 190, 1, 2.0),
                   (1360, 1312, 520, 158, 1, 3.5)],
         fx=[], ov=[],
         onscreen='Cold open on the events table, already moving. Rings land on the Interview location chip of each event as its city is named: Video in Dallas, In person in Omaha, Phone in Chicago.',
         vo=["Three hiring events. Three completely different ways to interview.",
             "Northwind interviews on video in Dallas, in person in Omaha, and by phone in Chicago.",
             "Interview location is your setting, and you pick it for every event."]),

    dict(id='s2', title='Choose How You Interview', label='CHOOSE HOW YOU INTERVIEW', img='setperson',
         # Measured: question at y=622, the Video/Phone/In-Person control at y=766.
         # Framed tight on the choice itself so nothing sits under a caption, and cropped
         # left of x=620 so the setup flow's OLD three-item nav never enters frame and
         # contradicts the five-item nav from scene 1.
         crop=(1600, 1020, 372),
         callouts=[], fx=[], ov=[],
         onscreen='The interview-location control, with In-Person chosen. One setting that applies to every interview scheduled for this event.',
         vo=["You do not have to run every interview on video.",
             "Video, on the JobFairX call or your own Teams, Zoom, or Meet link.",
             "Phone, where you call each candidate. Or in person, at your own address."]),

    dict(id='s2b', title='What The Candidate Gets', label='CHOOSE HOW YOU INTERVIEW', img='setperson',
         # The in-person detail: address, parking, arrival, and the product's own line
         # about where those details go. Held clear of the caption band on purpose.
         crop=(2400, 620, 805),
         callouts=[], fx=[], ov=[],
         onscreen='Choosing in person opens the address, parking and arrival fields, and the product states where those details end up.',
         vo=["In person opens the address, with parking and arrival instructions.",
             "They go out with every interview confirmation. They are never posted on the event."]),

    dict(id='s3', title='They Pick The Time', label='BEFORE THE EVENT', img='pre',
         crop=(3200, 0, 330),
         callouts=[], fx=[], ov=[],
         onscreen='The pre-event lobby: eight candidates awaiting a response, each row carrying the time slot that candidate chose.',
         vo=["Scheduling is the part you never have to do.",
             "Matching starts the moment your jobs are posted, and the first requests arrive within a few hours.",
             "Each one carries the time slot the candidate picked."]),

    dict(id='s4', title='Read It, Then Accept', label='BEFORE THE EVENT', img='resume',
         crop=(3200, 0, 300),
         callouts=[], fx=[], ov=[],
         onscreen='The resume behind a request, open on the work history, skills and the screener answers the employer actually reads before deciding.',
         vo=["Open the resume, read their screener answers, accept.",
             "Accepting is the scheduling step. There is no second one.",
             "Or turn on auto accept and let them confirm themselves."]),

    dict(id='s5', title='Accepted', label='BEFORE THE EVENT', img='toast',
         crop=(3200, 0, 0),
         callouts=[], fx=[], ov=[],
         onscreen='The accept lands: the confirmation with Undo, the awaiting count down to seven, and that candidate now sitting under upcoming interviews.',
         vo=["That is it. The candidate is booked, and the count moves with it."]),

    dict(id='s6', title='Automations', label='AUTOMATIONS', img='autos',
         crop=(3200, 0, 190),
         callouts=[], fx=[], ov=[],
         onscreen='The Automations table, all five presets readable at once, with the On and Off state and the job and event each one covers.',
         vo=["Between now and event day, the messaging runs itself. Five presets are ready.",
             "New candidates, scheduled candidates, missed interviews, declines, and a follow up after you interview.",
             "Pick the jobs and the event each one covers, then switch it on."]),

    dict(id='s7', title='Event Day', label='EVENT DAY', img='lobbylive',
         crop=(3200, 0, 0),
         callouts=[], fx=[], ov=[],
         onscreen='The lobby live, with the clock running down. On a video event it splits: interview rooms for the candidates who are ready, waiting rooms for the rest.',
         vo=["Event day. The lobby goes live with a clock on it.",
             "On the video path it splits in two. Interview rooms for candidates who are ready, and waiting rooms for the rest."]),

    dict(id='s8', title='The Same Event, In Person', label='EVENT DAY, IN PERSON', img='lobbyperson',
         crop=(3200, 0, 0),
         callouts=[], fx=[], ov=[],
         onscreen='A hard cut at the identical framing. Same event, same date, same six candidates. Only the interview location changed, and the lobby has changed shape with it.',
         vo=["Same event. Same candidates. Set the interview location to in person and the lobby changes shape.",
             "No rooms to split. One queue, longest wait first, and every status reads checked in, because they walked through your door.",
             "Everyone matched to you is verified to be within about twenty miles of the event city."]),

    dict(id='s9', title='The Interview', label='THE INTERVIEW', img='room',
         crop=(3200, 0, 0),
         callouts=[], fx=[], ov=[],
         onscreen='Inside a video interview: the candidate on screen, and the resume, notes and chat sitting beside the call rather than behind a menu.',
         vo=["Back in a video interview, the resume, your notes, and chat sit beside the call."]),

    dict(id='s10', title='Yes, Maybe, Or No', label='THE INTERVIEW', img='recmodal',
         crop=(3200, 0, 0),
         callouts=[], fx=[], ov=[],
         onscreen='The one question at the end of every interview, whichever way it was run.',
         vo=["Either way, you finish the same. One optional question. Would you recommend moving forward.",
             "Yes, maybe, or no, with a note."]),

    dict(id='s11', title='It Stays With The Interviewer', label='THE INTERVIEW', img='ivd',
         crop=(3200, 0, 250),
         callouts=[], fx=[], ov=[],
         onscreen='The interviewed tab: every answer kept against the candidate, with the interviewer who ran it and the note they left.',
         vo=["And it stays with the interviewer who ran it."]),

    dict(id='s12', title='The Report Is Already Built', label='AFTER THE EVENT', img='report',
         crop=(3200, 0, 120),
         callouts=[], fx=[], ov=[],
         onscreen='The event report, filtered by outcome, with the interviewer, the feedback and the notes reading together on every row.',
         vo=["When it is over, the report is already built.",
             "Every candidate who had a time with you, with the interviewer, the feedback, and the notes.",
             "Filter it, export it, or offer a follow up interview right from the row."]),

    dict(id='s13', title='Your Numbers', label='ANALYTICS', img='analytics',
         crop=(3200, 0, 120),
         callouts=[], fx=[], ov=[],
         onscreen='Analytics over a date range you choose, on your own account: interviews scheduled, attendance, missed, and how many you marked yes.',
         vo=["Analytics runs on your own account, over the dates you pick.",
             "Interviews scheduled, attendance, missed interviews, and how many you marked yes.",
             "Your numbers, not an industry average."]),

    dict(id='s14', title='Register', label='REGISTER', img='dash',
         crop=(2200, 470, 500),
         callouts=[], fx=[], ov=[],
         onscreen='Back where it started, on the three events and their three interview locations.',
         vo=["Pick a hiring event, post your jobs, and set your interview location.",
             "Register at jobfairx.com."]),
]

def spoken_tokens(text):
    return [w for w in text.split() if re.search(r'[A-Za-z0-9]', w)]


async def synth(text, path):
    tts = edge_tts.Communicate(text, VOICE, boundary='WordBoundary')
    words, last_end = [], 0.0
    with open(path, 'wb') as f:
        async for chunk in tts.stream():
            if chunk['type'] == 'audio':
                f.write(chunk['data'])
            elif chunk['type'] == 'WordBoundary':
                words.append(chunk['offset'] / 1e7)
                last_end = chunk['offset'] / 1e7 + chunk['duration'] / 1e7
    return words, last_end


def zoomed(crop):
    w, ox, oy = crop
    h = w * 540 / 960
    w2 = w * ZOOM
    return (w2, ox + (w - w2) / 2, oy + (h - w2 * 540 / 960) / 2)


def crop_transform(crop):
    w, ox, oy = crop
    k = DESIGN_W / w
    return f'scale({k:.5f}) translate({-ox:.1f}px, {-oy:.1f}px)'


def check_scene(s):
    msgs = []
    iw, ih = IMG_DIMS[s['img']]
    w, ox, oy = s['crop']
    h = w * 540 / 960
    if ox >= 0 and (ox + w > iw or oy + h > ih or oy < 0):
        msgs.append(f' !! crop out of bounds (oy+H={oy + h:.0f})')
    end = zoomed(s['crop']) if s.get('zoom', True) else s['crop']
    ew, eox, eoy = end
    eh = ew * 540 / 960
    k = DESIGN_W / ew
    for j, (x, y, cw, ch, ci, delta) in enumerate(s['callouts']):
        if not (x >= eox and y >= eoy and x + cw <= eox + ew and y + ch <= eoy + eh):
            msgs.append(f' !! callout {j} outside end crop')
        top_d, bot_d = (y - eoy) * k, (y + ch - eoy) * k
        if s.get('capTop') and top_d < 100:
            msgs.append(f' !! callout {j} in top caption zone (y={top_d:.0f})')
        if not s.get('capTop') and bot_d > 445:
            msgs.append(f' !! callout {j} in caption zone (bottom={bot_d:.0f})')
        left_d = (x - eox) * k
        if s.get('label') and top_d < 62 and left_d < 230:
            msgs.append(f' !! callout {j} under the label chip (y={top_d:.0f}, x={left_d:.0f})')
    return ''.join(msgs)


async def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    for f in os.listdir(AUDIO_DIR):
        if f.endswith('.mp3') and not f.startswith('sample'):
            os.remove(f'{AUDIO_DIR}/{f}')

    for s in SCENES:
        text = ' '.join(s['vo'])
        path = f"{AUDIO_DIR}/{s['id']}.mp3"
        words, audio_end = await synth(text, path)
        counts = [len(spoken_tokens(c)) for c in s['vo']]
        # NB: edge-tts emits a SINGLE WordBoundary for "Month DD" (e.g. "April 15"),
        # so a numeric date silently desyncs captions from audio. Spell dates out
        # ("April fifteenth") in vo strings. This assert is what catches it.
        assert sum(counts) == len(words), f"{s['id']}: {len(words)} events vs {sum(counts)} tokens"
        offs, idx = [], 0
        for n in counts:
            offs.append(words[idx])
            idx += n
        s['chunk_offs'], s['audio_end'], s['audio_path'] = offs, audio_end, path
        print(f"{s['id']}: {audio_end:5.2f}s audio, {len(words)} words{check_scene(s)}")

    caps, scenes_json, clips = [], [], []
    cursor = 0.0
    for s in SCENES:
        s['start'] = round(cursor, 1)
        anchor = s['start'] + LEAD
        s['anchor'] = anchor
        for off, text in zip(s['chunk_offs'], s['vo']):
            caps.append([round(anchor + off, 1), text])
        clips.append(dict(t=anchor, end=round(anchor + s['audio_end'], 2), path=s['audio_path']))
        cursor = anchor + s['audio_end'] + GAP
    dur = math.ceil(SCENES[-1]['anchor'] + SCENES[-1]['audio_end'] + 3.0)
    for i, s in enumerate(SCENES):
        s['dur'] = (SCENES[i + 1]['start'] if i + 1 < len(SCENES) else dur) - s['start']
        scenes_json.append(dict(id=s['id'], start=s['start'], title=s['title'], capTop=s.get('capTop', False)))

    sections, keyframes = [], []
    for s in SCENES:
        def at(ci, delta):
            return round(LEAD + s['chunk_offs'][ci] + delta, 1)
        cos = ''.join(
            f'<div class="co" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{at(ci, d)}s"></div>'
            for (x, y, w, h, ci, d) in s['callouts'])
        fxs = ''.join(html.replace('__D__', f'{at(ci, d)}s') for (html, ci, d) in s['fx'])
        ovs = ''.join(html.replace('__D__', f'{at(ci, d)}s') for (html, ci, d) in s['ov'])
        lab = f'<span class="slabel {s.get("labelPos", "")}">{s["label"]}</span>' if s['label'] else ''
        sections.append(
            f'        <section class="scene" id="{s["id"]}"><div class="shot{" has-label" if s["label"] else ""}">'
            f'<div class="pan pan-{s["id"]}" style="width:{IMG_DIMS[s["img"]][0]}px;height:{IMG_DIMS[s["img"]][1]}px">'
            f'<div class="bg img-{s["img"]}" style="background-size:{IMG_DIMS[s["img"]][0]}px {IMG_DIMS[s["img"]][1]}px"></div>{cos}{fxs}</div>'
            f'{ovs}{lab}</div></section>')
        end = zoomed(s['crop']) if s.get('zoom', True) else s['crop']
        keyframes.append(
            f'  .on .pan-{s["id"]}{{animation:kf-{s["id"]} {s["dur"]:.1f}s linear both}}\n'
            f'  @keyframes kf-{s["id"]}{{0%{{transform:{crop_transform(s["crop"])}}}'
            f'100%{{transform:{crop_transform(end)}}}}}')

    img_css = []
    for name, path in IMAGES.items():
        raw = open(path, 'rb').read()
        mime = 'image/png'
        if len(raw) > 1_000_000:  # photographic captures compress far better as JPEG
            import io
            buf = io.BytesIO()
            _Img.open(path).convert('RGB').save(buf, 'JPEG', quality=86)
            raw, mime = buf.getvalue(), 'image/jpeg'
        b64 = base64.b64encode(raw).decode()
        img_css.append(f'  .img-{name}{{background-image:url(data:{mime};base64,{b64})}}')
    clip_js = []
    for c in clips:
        b64 = base64.b64encode(open(c['path'], 'rb').read()).decode()
        clip_js.append(f'    {{t: {c["t"]}, end: {c["end"]}, src: "data:audio/mpeg;base64,{b64}"}}')

    n_sections = len({s['title'] for s in SCENES})
    label = f"{int(dur // 60)}:{int(dur % 60):02d}"
    html_out = open(TEMPLATE).read()
    subs = {
        '%%DUR%%': str(dur), '%%DUR_INT%%': str(dur), '%%DURLABEL%%': label,
        '%%SCRIPT_H2%%': f"{ {5:'Five',6:'Six',7:'Seven'}.get(n_sections, n_sections) } sections in {label}",
        '%%VOICE%%': f'{VOICE} (draft)',
        '%%VOICE_NAME%%': VOICE_NAME,
        '%%IMG_CSS%%': '\n'.join(img_css),
        '%%SCENE_KEYFRAMES%%': '\n'.join(keyframes),
        '%%SCENE_SECTIONS%%': '\n'.join(sections),
        '%%SCENES_JSON%%': json.dumps(scenes_json),
        '%%CAPS_JSON%%': json.dumps(caps, ensure_ascii=False),
        '%%VOTRACK_CLIPS%%': ',\n'.join(clip_js),
        '%%ONSCREEN_JSON%%': json.dumps({s['id']: s['onscreen'] for s in SCENES}, ensure_ascii=False),
    }
    for key, val in subs.items():
        assert key in html_out, f'missing placeholder {key}'
        html_out = html_out.replace(key, val)
    open(OUT, 'w').write(html_out)
    json.dump({'voice': VOICE, 'dur': dur,
               'scenes': [dict(id=s['id'], start=s['start'], anchor=s['anchor'],
                               audio=round(s['audio_end'], 2)) for s in SCENES],
               'caps': caps},
              open(f'{AUDIO_DIR}/timing.json', 'w'), indent=1)
    print(f'built {OUT}: {len(html_out)} bytes, duration {label}, voice {VOICE}')


asyncio.run(main())
