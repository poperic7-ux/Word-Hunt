import random
import streamlit as st
import streamlit.components.v1 as components

# ----------------------------- Game data -----------------------------
WORDS = """about above actor adult after again agree ahead alarm album alert alive allow alone angle apple
arena argue arise armor avoid awake award aware basic beach begin being bench birth black blame blank blast
blend blind block blood board boost brain brand brave bread break brick bride brief bring broad brown brush
build cable candy carry catch cause chain chair chalk charm chase cheap check chest chief child claim class
clean clear climb clock close cloud coach coast color count court cover craft crane crash cream crowd crown
curve daily dance delay depth dream dress drink drive eager early earth eight elbow empty enjoy enter equal
error event every exact extra faith false field fifth fight final first flame flash floor flour focus force
frame fresh front fruit giant glass globe glory grace grade grain grand grape grass great green group guard
guess guest guide habit happy heart heavy honey horse hotel house human humor image inner issue jelly joint
judge juice knife label large laser later laugh layer learn leave legal lemon level light limit local logic
loose lucky lunch magic major maple march match maybe media metal might minor model money month moral motor
mount mouse mouth movie music nerve night noble noise north novel nurse ocean offer olive onion order other
outer owner paint panel paper party peace pearl phase phone photo piano pilot pitch place plain plane plant
plate point power press price pride prize proof proud queen quick quiet radio raise range rapid ratio reach
ready river robot rough round royal salad scale scene score sense seven shade shape share sharp sheep sheet
shelf shell shift shine shirt shoot short sight skill sleep slice small smart smile smoke snake solid sound
south space spare speak speed spend spice spoon sport staff stage stair stamp stand start state steam steel
stick stone store storm story sugar sunny sweet swift table taste teach thank theme thick thing think three
throw tiger title toast tooth topic total touch tough tower track trade train treat trend trial truck trust
truth uncle under union unity upper urban usual valid value video visit vital voice waste watch water wheel
white whole woman world worry worth write wrong young youth zebra""".split()

COLORS = {"hit": "#24a879", "near": "#e6ad32", "miss": "#596579", "empty": "transparent"}
RANK = {"miss": 0, "near": 1, "hit": 2}
ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

st.set_page_config(page_title="Five Letters", page_icon="🔤", layout="centered")


# ----------------------------- Game logic -----------------------------
def score(guess, answer):
    result = ["miss"] * 5
    pool = {}
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            result[i] = "hit"
        else:
            pool[answer[i]] = pool.get(answer[i], 0) + 1
    for i, ch in enumerate(guess):
        if result[i] != "hit" and pool.get(ch, 0) > 0:
            result[i] = "near"
            pool[ch] -= 1
    return result


def new_game():
    st.session_state.answer = random.choice(WORDS)
    st.session_state.guesses = []
    st.session_state.msg = "Guess the 5-letter word."
    st.session_state.done = False
    st.session_state.won = False
    st.session_state.sound_event = "new"


def submit():
    guess = st.session_state.get("guess_input", "").strip().lower()
    if st.session_state.done:
        return
    if len(guess) != 5 or not guess.isalpha() or not guess.isascii():
        st.session_state.msg = "Enter exactly 5 letters (A–Z)."
        st.session_state.sound_event = "invalid"
        return
    st.session_state.guesses.append(guess)
    n = len(st.session_state.guesses)
    if guess == st.session_state.answer:
        st.session_state.msg = f"Solved in {n} guess{'es' if n != 1 else ''}!"
        st.session_state.done = True
        st.session_state.won = True
        st.session_state.sound_event = "win"
    elif n == 6:
        st.session_state.msg = f"The word was {st.session_state.answer.upper()}."
        st.session_state.done = True
        st.session_state.won = False
        st.session_state.sound_event = "lose"
    else:
        st.session_state.msg = f"Guess {n + 1} of 6"
        st.session_state.sound_event = "guess"


def tile(letter, state):
    bg = COLORS[state]
    border = "#344256" if state == "empty" else bg
    color = "#f8fafc"
    return (
        f"<div class='tile {state}'><span>{letter}</span></div>"
    )


# ----------------------------- Styling -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root { color-scheme: dark; }
.stApp {
    background:
      radial-gradient(ellipse at 12% 0%, rgba(36,168,121,.16), transparent 36%),
      radial-gradient(ellipse at 100% 15%, rgba(70,100,150,.20), transparent 34%),
      linear-gradient(145deg, #0b1220 0%, #111c2e 55%, #0c1524 100%);
    color: #f8fafc;
}
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px; padding-top: 2.3rem; padding-bottom: 3rem; }
h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] { color: #f8fafc; }
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -1.5px;
    text-align: center;
    font-size: clamp(2.3rem, 6vw, 3.4rem) !important;
    margin-bottom: .25rem !important;
}
p { font-family: 'DM Sans', sans-serif; }
.subtitle { text-align:center; color:#a9b8cc; margin:0 0 1.5rem; font-size:.98rem; }
.status {
    text-align:center; margin: 0 auto 1.4rem; padding: .8rem 1rem;
    max-width: 440px; border:1px solid rgba(169,184,204,.16);
    background:rgba(255,255,255,.045); border-radius:14px;
    color:#e8eef7; font-family:'DM Sans',sans-serif; font-weight:600;
}
.board { display:flex; flex-direction:column; align-items:center; gap:7px; margin: 0 auto 1.6rem; }
.board-row { display:flex; gap:7px; justify-content:center; }
.tile {
    width: clamp(43px, 10.8vw, 58px); height: clamp(43px, 10.8vw, 58px);
    display:flex; align-items:center; justify-content:center; box-sizing:border-box;
    border:2px solid #344256; border-radius:10px;
    background:rgba(255,255,255,.025); color:#f8fafc;
    font-family:'Space Grotesk',sans-serif; font-weight:700;
    font-size:clamp(1.2rem, 4.5vw, 1.65rem); text-transform:uppercase;
    transition:transform .18s ease, background .18s ease;
}
.tile.hit { background:#20845f; border-color:#20845f; }
.tile.near { background:#b98620; border-color:#b98620; }
.tile.miss { background:#465267; border-color:#465267; }
.keyboard { display:flex; flex-direction:column; gap:7px; align-items:center; margin: 0 auto 1.6rem; }
.key-row { display:flex; gap:5px; justify-content:center; width:100%; }
.key {
    display:flex; align-items:center; justify-content:center;
    width:clamp(23px, 7.4vw, 43px); height:clamp(36px, 9vw, 44px);
    border-radius:7px; background:#dce5f1; color:#172338;
    font:700 clamp(11px, 2.8vw, 14px) 'DM Sans',sans-serif; text-transform:uppercase;
}
.key.hit { background:#20845f; color:white; }
.key.near { background:#b98620; color:white; }
.key.miss { background:#465267; color:white; }
div[data-testid="stTextInput"] label { color:#dbe5f2 !important; font-weight:600; }
.stTextInput input {
    background:#f8fafc !important; color:#172338 !important;
    border:1px solid #cbd5e1 !important; border-radius:11px !important;
    min-height:48px; font-size:1.05rem; font-weight:600;
}
.stTextInput input:focus { border-color:#24a879 !important; box-shadow:0 0 0 2px rgba(36,168,121,.22) !important; }
.stButton button, .stFormSubmitButton button {
    background:#20845f !important; color:white !important; border:0 !important;
    border-radius:11px !important; min-height:46px; font-weight:700 !important;
    transition:background .15s ease, transform .15s ease;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    background:#29a879 !important; transform:translateY(-1px);
}
div[data-testid="stForm"] { border:0; padding:0; }
div[data-testid="stCheckbox"] label { color:#c9d5e5 !important; }
.footer { text-align:center; color:#8292a8; font-size:.8rem; margin-top:1.6rem; }
@media (max-width:480px) {
  .block-container { padding-left: .8rem; padding-right: .8rem; padding-top:1.5rem; }
  .board-row { gap:5px; }
}
</style>
""", unsafe_allow_html=True)

if "answer" not in st.session_state:
    new_game()
if "sound_event" not in st.session_state:
    st.session_state.sound_event = "none"
if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = True

# ----------------------------- Sound effects -----------------------------
# Audio is generated locally in the browser with Web Audio; no audio files needed.
sound_event = st.session_state.sound_event
sound_enabled = st.session_state.sound_enabled
if sound_enabled and sound_event not in ("none", "new"):
    sound_js = {
        "guess": """
            tone(440, .09, 'sine', 0.045); setTimeout(()=>tone(587, .10, 'sine', 0.04), 85);
        """,
        "win": """
            tone(523, .13, 'sine', .06); setTimeout(()=>tone(659, .13, 'sine', .06), 130);
            setTimeout(()=>tone(784, .18, 'sine', .06), 260); setTimeout(()=>tone(1047, .28, 'sine', .055), 420);
        """,
        "lose": """
            tone(392, .16, 'triangle', .05); setTimeout(()=>tone(330, .18, 'triangle', .05), 170);
            setTimeout(()=>tone(262, .28, 'triangle', .05), 350);
        """,
        "invalid": """
            tone(220, .12, 'square', .025); setTimeout(()=>tone(180, .13, 'square', .025), 100);
        """,
    }.get(sound_event, "")
    if sound_js:
        components.html(f"""
        <script>
        (() => {{
          const AC = window.AudioContext || window.webkitAudioContext;
          if (!AC) return;
          const ctx = new AC();
          function tone(freq, dur, type, vol) {{
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = type; osc.frequency.value = freq;
            gain.gain.setValueAtTime(vol, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
            osc.connect(gain); gain.connect(ctx.destination);
            osc.start(); osc.stop(ctx.currentTime + dur);
          }}
          {sound_js}
          setTimeout(() => ctx.close(), 1400);
        }})();
        </script>
        """, height=0, width=0)
st.session_state.sound_event = "none"

# ----------------------------- Header -----------------------------
st.markdown("<div style='text-align:center;font-size:2rem;margin-bottom:.3rem'>🔤</div>", unsafe_allow_html=True)
st.title("Five Letters")
st.markdown("<div class='subtitle'>Six chances. One five-letter word.</div>", unsafe_allow_html=True)

left, right = st.columns([1, 1])
with left:
    st.caption(f"🎯  {len(st.session_state.guesses)} / 6 guesses used")
with right:
    st.session_state.sound_enabled = st.checkbox("🔊 Sound effects", value=st.session_state.sound_enabled)

st.markdown(f"<div class='status'>{st.session_state.msg}</div>", unsafe_allow_html=True)

# ----------------------------- Board -----------------------------
best = {}
rows_html = "<div class='board'>"
for r in range(6):
    if r < len(st.session_state.guesses):
        g = st.session_state.guesses[r]
        res = score(g, st.session_state.answer)
        for ch, s in zip(g, res):
            if ch not in best or RANK[s] > RANK[best[ch]]:
                best[ch] = s
        cells = "".join(tile(ch, s) for ch, s in zip(g, res))
    else:
        cells = "".join(tile("", "empty") for _ in range(5))
    rows_html += f"<div class='board-row'>{cells}</div>"
rows_html += "</div>"
st.markdown(rows_html, unsafe_allow_html=True)

# ----------------------------- Keyboard -----------------------------
kb_html = "<div class='keyboard'>"
for row in ROWS:
    keys = ""
    for ch in row:
        s = best.get(ch, "empty")
        keys += f"<span class='key {s}'>{ch}</span>"
    kb_html += f"<div class='key-row'>{keys}</div>"
kb_html += "</div>"
st.markdown(kb_html, unsafe_allow_html=True)

# ----------------------------- Input -----------------------------
with st.form("guess_form", clear_on_submit=True):
    st.text_input("Your guess", max_chars=5, key="guess_input", disabled=st.session_state.done, placeholder="Type a 5-letter word")
    st.form_submit_button("Submit guess  ↗", on_click=submit, disabled=st.session_state.done, use_container_width=True)

if st.session_state.done:
    if st.session_state.won:
        st.success("Brilliant! You cracked the word. 🎉")
    else:
        st.info(f"Better luck next time — the answer was **{st.session_state.answer.upper()}**.")
    if st.button("↻  Play again", use_container_width=True):
        new_game()
        st.rerun()

st.markdown("<div class='footer'>A little word puzzle for your daily brain workout.</div>", unsafe_allow_html=True)
