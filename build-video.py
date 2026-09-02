#!/usr/bin/env python3
"""Build the JobFairX hiring-event product video from real product screenshots.

VO text is the FINAL approved script, verbatim (chunk splits affect captions/timing only,
never words). Each scene is ONE steady view of a real screen — at most a slow centered
push-in, never a lateral pan. Timeline derives from measured audio + word boundaries.
"""
import asyncio, base64, json, math, os, re, sys

import edge_tts

VOICE = sys.argv[1] if len(sys.argv) > 1 else 'en-US-EmmaNeural'
VOICE_NAME = re.sub(r'^[a-z]{2}-[A-Z]{2}-|Neural$|Multilingual.*$', '', VOICE)
TEMPLATE = 'video-template.html'
OUT = 'event-day-lobby-explainer.html'
AUDIO_DIR = 'vo'
ASSETS = '/Users/scottl./Desktop/jobfairx-marketing/assets/product'
GAP = 0.5          # breath between one scene's last word and the next cut
LEAD = 0.4         # VO starts this soon after each cut
IMG_W, IMG_H = 3200, 2000
DESIGN_W = 960
ZOOM = 0.97        # end-of-scene push-in (about the crop center; no lateral movement)

IMAGES = {
    'lobby':    f'{ASSETS}/lobby-tables-hc.png',
    'dash':     f'{ASSETS}/dashboard-events-hc.png',
    'ivg':      f'{ASSETS}/lobby-interviewing-hc.png',
    'ivd':      f'{ASSETS}/lobby-interviewed-hc.png',
    'room':     f'{ASSETS}/room-late-hc.png',
    'recmodal': f'{ASSETS}/room-recmodal-hc.png',
    # pre-event chapter: the lobby in its "Active" state, before the event goes live
    'pre':      f'{ASSETS}/lobby-pre-hc.png',
    'resched':  f'{ASSETS}/resched-person-hc.png',
    'prewait':  f'{ASSETS}/lobby-pre-waiting-hc.png',
}
from PIL import Image as _Img
IMG_DIMS = {k: _Img.open(v).size for k, v in IMAGES.items()}

# Scene keys: crop (W, ox, oy natural px); callouts = rings (x,y,w,h, capIdx, +delta);
# fx = image-coord effect HTML with __D__ delay placeholder, timed like callouts;
# ov = design-coord overlay HTML (fit dialog); label = on-screen section label.
SCENES = [
    dict(id='s1', title='The Lobby', label='THE LOBBY', img='lobby', crop=(3200, 0, 0),
         callouts=[], fx=[], ov=[],
         onscreen='Cold open on the live lobby, full frame — header, countdown, tabs, and the interview tables.',
         vo=["This is the event-day lobby — your entire hiring event, live and organized in one place.",
             "You can see your candidates, manage interviews, and keep your hiring event moving."]),

    dict(id='s2', title='Choose How You Interview', label='CHOOSE HOW YOU INTERVIEW', img='dash',
         crop=(2100, 700, 530),
         callouts=[(1375, 700, 420, 162, 1, 0.2),
                   (1375, 1022, 450, 196, 2, 0.2), (1375, 1338, 400, 150, 3, 0.2)],
         fx=[], ov=[],
         onscreen='The events dashboard, steady on the Interview location column: Video, In person, and Phone — ringed top to bottom in narration order.',
         vo=["When you register for an event, you choose how you want to interview candidates: video, in person, or phone.",
             "For video interviews, interviews take place on the JobFairX platform.",
             "For in-person interviews, candidates receive the location and instructions they need for their interview.",
             "And for phone interviews, you call the candidate at their scheduled interview time."]),

    # ── BEFORE THE EVENT ──────────────────────────────────────────────────────
    # Added Aug 2026: the video showed only live event day and never showed the
    # employer what to do beforehand. All frames are the A ("Active") lobby state.
    dict(id='p1', title='Before the Event', label='BEFORE THE EVENT', img='pre', crop=(3200, 0, 0),
         callouts=[(80, 355, 420, 70, 0, 0.4), (2545, 580, 420, 90, 1, 0.5),
                   (95, 720, 950, 110, 2, 0.3)],
         fx=[], ov=[],
         onscreen='The same lobby, weeks before the event: a countdown to April 22, three empty tabs, and eight candidate requests already waiting under Candidates awaiting your response.',
         vo=["This is the same lobby before your event, two weeks and three days out.",
             "When your jobs are posted, candidates start requesting interviews, weeks before the hiring event begins.",
             "Until then, your work happens under Candidates awaiting your response."]),

    dict(id='p2', title='Before the Event', label='CANDIDATE REQUESTS', img='pre', crop=(2800, 40, 622),
         callouts=[(2140, 965, 630, 105, 1, 0.3)],
         fx=[], ov=[],
         onscreen='The awaiting-response table: name, desired job, desired location, requested time, and the three actions on every row.',
         vo=["Each request shows the candidate's name, the job and location they want, and the time they requested.",
             "You have three choices on every row: Accept, Decline, or Reschedule.",
             "When you select Accept, the interview is scheduled at the time the candidate requested.",
             "When you select Decline, the candidate is removed from your lobby."]),

    dict(id='p3a', title='Before the Event', label='RESCHEDULE', img='resched', crop=(3130, 31, 75),
         callouts=[(595, 335, 690, 100, 1, 0.3)],
         fx=[], ov=[],
         onscreen='The Schedule window for one candidate, with the required Format control set to In-Person.',
         vo=["When you select Reschedule, you propose a different time and set the interview location for that one interview.",
             "Format sets how you will interview this one candidate. Video, phone, or in person.",
             "It covers this one interview, and it does not change what you chose when you registered."]),

    # split off p3a so neither shot holds a single static frame for 26 seconds
    dict(id='p3a2', title='Before the Event', label='IN PERSON', img='resched', crop=(2400, 400, 200),
         callouts=[(590, 450, 810, 825, 0, 0.4)],
         fx=[], ov=[],
         onscreen='Close on the In-Person fields the format reveals: interview address, parking instructions, arrival instructions, and the note that the candidate receives them.',
         vo=["With In-Person selected, you enter the interview address, parking, and arrival instructions.",
             "Those details are included in the candidate's interview confirmation."]),

    dict(id='p3b', title='Before the Event', label='PROPOSE TIMES', img='resched', crop=(2700, 480, 250),
         zoom=False,
         callouts=[(1430, 290, 1190, 360, 0, 0.3)],
         fx=[], ov=[],
         onscreen='The proposed slots, both dated six weeks after the event, above the message to the candidate and the Send button.',
         vo=["You can suggest more than one time, and the times do not have to fall on event day.",
             "Write a message to the candidate, then select Send."]),

    dict(id='p4', title='Before the Event', label='PROPOSED', capTop=True, img='pre', crop=(3120, 40, 480),
         callouts=[(100, 1750, 3000, 300, 0, 0.4)],
         fx=[], ov=[],
         onscreen='Two rows now read Proposed, awaiting candidate, with the offered times and a Cancel link, while the rows above still show Accept, Decline and Reschedule.',
         vo=["When you send the times, the row reads Proposed, awaiting candidate.",
             "The candidate stays under Candidates awaiting your response until they pick one of your times.",
             "Select Cancel to withdraw the proposal.",
             "The rows above still show Accept, Decline, and Reschedule."]),

    dict(id='p5', title='Before the Event', label='SCHEDULED', img='pre', crop=(3120, 40, 1820),
         callouts=[(100, 2130, 1100, 110, 0, 0.4), (1690, 2320, 420, 300, 1, 0.6)],
         fx=[], ov=[],
         onscreen='Candidates with upcoming interviews: two interviews carry their own dates off event day, the rest are set for April 22.',
         vo=["When the candidate picks one of your times, the interview moves down into Candidates with upcoming interviews, at the time the candidate chose.",
             "Interviews scheduled away from event day carry their own date, like Sarah Kim on April fifteenth and David Okafor on April sixteenth.",
             "The rest are set for April twenty second, the day of the hiring event."]),

    dict(id='p6', title='Before the Event', label='BEFORE EVENT DAY', img='prewait', crop=(3120, 40, 60),
         callouts=[(100, 700, 3000, 360, 0, 0.4)],
         fx=[], ov=[],
         onscreen='The Waiting to interview tab before the event: Interviewing has not begun.',
         vo=["Before the event, the Waiting to interview tab reads Interviewing has not begun.",
             "The Waiting Room becomes active when your event goes live."]),

    dict(id='s3a', title='Interviews', label='WAITING ROOM', img='lobby', crop=(3200, 0, 485),
         callouts=[(90, 1460, 500, 80, 0, 0.5), (2390, 1680, 390, 200, 1, 0.3), (90, 765, 530, 80, 2, 1.7)],
         fx=[], ov=[],
         onscreen='Both lobby tables in one view. The Waiting rooms section lights up as the candidate logs in, the statuses show they are online, then the highlight moves up into the Interview rooms table.',
         vo=["When a candidate logs in for their interview, they appear in the Waiting Room.",
             "This lets you know the candidate is online and ready for their interview.",
             "When the candidate joins their scheduled interview, they move from the Waiting Room into an Interview Room."]),

    dict(id='s3b', title='Interviews', label='INTERVIEWING', img='ivg', crop=(3200, 0, 0), zoom=False,
         callouts=[(100, 764, 650, 90, 0, 0.4), (1050, 586, 330, 108, 1, 0.5), (2350, 876, 340, 450, 1, 3.0)],
         fx=[], ov=[],
         onscreen='The real Interviewing tab: Interviews in progress with interviewer names and running durations. Rings land on the section header, the active tab, then the Interviewer column.',
         vo=["When the interviewer joins, the interview begins in the Interview Room.",
             "At the same time, the interview moves from the Waiting to Interview tab to the Interviewing tab, making it easy to see which interviews are currently in progress."]),

    dict(id='s3c', title='Interviews', label='CANDIDATE FIT', labelPos='tr', capTop=True, img='recmodal',
         crop=(3556, -178, 0), zoom=False,
         callouts=[(1120, 790, 650, 110, 1, 0.3)],
         fx=[], ov=[],
         onscreen='The real end-of-interview prompt over the live video call with James Cooper (both people on camera). A ring lands on the Yes / Maybe / No toggle.',
         vo=["When the interview ends, the interviewer is asked whether the candidate is a good fit for the role.",
             "They can select Yes, No, or Maybe."]),

    dict(id='s3d', title='Interviews', label='INTERVIEWED', img='ivd', crop=(3200, 0, 150),
         callouts=[(1820, 588, 320, 110, 0, 0.5), (1765, 975, 320, 630, 0, 2.0), (240, 588, 420, 110, 1, 1.0)],
         fx=[], ov=[],
         onscreen='The real Interviewed tab: each candidate with Yes / No / Maybe feedback and who interviewed them. Rings land on the Interviewed tab, the Feedback column, then back on Waiting to Interview.',
         vo=["The interview then moves to the Interviewed tab,",
             "and the interviewer is returned to the Waiting to Interview tab, where they can start their next scheduled interview."]),

    dict(id='s4', title='Event Status', label='EVENT STATUS', img='lobby', crop=(3200, 0, 150),
         callouts=[(60, 574, 3020, 124, 0, 0.3), (1820, 588, 300, 110, 2, 0.3)],
         fx=[('<div class="fx-plus" style="left:2085px; top:465px; --d:__D__">+1</div>', 1, 0.6)],
         ov=[],
         onscreen='The full lobby, tab strip ringed. A subtle +1 rises by the Interviewed count, then Interviewed is emphasized as the running total.',
         vo=["The four tabs show the state of your event — waiting to interview, interviewing, interviewed, and not yet interviewed.",
             "The counts update automatically throughout the day.",
             "Interviewed gives you a running total of completed interviews."]),

    dict(id='s5a', title='Conducting Video Interviews', label='VIDEO INTERVIEWS', img='lobby',
         crop=(1700, 1440, 660),
         callouts=[(2690, 1108, 392, 92, 0, 0.4)],
         fx=[], ov=[],
         onscreen='Close on James Cooper\'s Ready row. The Start Interview button is ringed as it is named.',
         vo=["Select Start Interview to open a JobFairX video room."]),

    dict(id='s5b', title='Conducting Video Interviews', label='VIDEO INTERVIEWS', labelPos='tr', capTop=True, img='room',
         crop=(3556, -178, 0), zoom=False,
         callouts=[(1395, 1838, 450, 160, 1, 0.3), (1700, 1840, 130, 155, 2, 0.5), (2780, 1865, 130, 130, 3, 0.3)],
         fx=[], ov=[],
         onscreen='The JobFairX video room, whole screen: the candidate full-frame on camera, the interviewer in the self-view. Rings land on the call controls, then End, then Notes.',
         vo=["There's nothing for the candidate to download or install.",
             "The interviewer controls the conversation, with no time limit on the interview.",
             "When the interview is complete, simply select End.",
             "Notes taken during the interview and how you rated the candidate are available after the event."]),

    dict(id='s6', title='Recap', label='', img='lobby', crop=(3200, 0, 0),
         callouts=[], fx=[], ov=[],
         onscreen='The full live lobby holds through the close, then the JobFairX end card.',
         vo=["That's a hiring event on JobFairX. Open the lobby, meet candidates, run your interviews, and turn conversations into hires."]),
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
