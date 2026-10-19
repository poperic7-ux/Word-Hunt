import random
import streamlit as st

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

COLORS = {"hit": "#1f7a5c", "near": "#e0a100", "miss": "#6b7690", "empty": "transparent"}
RANK = {"miss": 0, "near": 1, "hit": 2}
ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]


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


def submit():
    guess = st.session_state.guess_input.strip().lower()
    if st.session_state.done:
        return
    if len(guess) != 5 or not guess.isalpha():
        st.session_state.msg = "Enter exactly 5 letters."
        return
    st.session_state.guesses.append(guess)
    n = len(st.session_state.guesses)
    if guess == st.session_state.answer:
        st.session_state.msg = f"Solved in {n} guess{'es' if n > 1 else ''}!"
        st.session_state.done = True
    elif n == 6:
        st.session_state.msg = f"The word was {st.session_state.answer.upper()}."
        st.session_state.done = True
    else:
        st.session_state.msg = f"Guess {n + 1} of 6"


def tile(letter, state):
    bg = COLORS[state]
    border = "#c5cfdd" if state == "empty" else bg
    color = "#fff" if state != "empty" else "inherit"
    return (
        f"<div style='width:52px;height:52px;display:flex;align-items:center;justify-content:center;"
        f"border:2px solid {border};border-radius:6px;background:{bg};color:{color};"
        f"font:700 26px Georgia,serif;text-transform:uppercase'>{letter}</div>"
    )


st.set_page_config(page_title="Five Letters", page_icon="🔤", layout="centered")
if "answer" not in st.session_state:
    new_game()

st.title("Five Letters")
st.write(st.session_state.msg)

best = {}
rows_html = ""
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
    rows_html += f"<div style='display:flex;gap:6px;justify-content:center;margin-bottom:6px'>{cells}</div>"
st.markdown(rows_html, unsafe_allow_html=True)

kb_html = ""
for row in ROWS:
    keys = ""
    for ch in row:
        s = best.get(ch, "empty")
        bg = "#dbe3ee" if s == "empty" else COLORS[s]
        fg = "#14213d" if s == "empty" else "#fff"
        keys += (
            f"<span style='width:28px;height:38px;display:inline-flex;align-items:center;"
            f"justify-content:center;border-radius:5px;background:{bg};color:{fg};"
            f"font:700 14px sans-serif;text-transform:uppercase'>{ch}</span>"
        )
    kb_html += f"<div style='display:flex;gap:4px;justify-content:center;margin-top:5px'>{keys}</div>"
st.markdown(kb_html, unsafe_allow_html=True)

with st.form("guess_form", clear_on_submit=True):
    st.text_input("Your guess", max_chars=5, key="guess_input", disabled=st.session_state.done)
    st.form_submit_button("Guess", on_click=submit, disabled=st.session_state.done, use_container_width=True)

if st.session_state.done:
    st.button("Play again", on_click=new_game, use_container_width=True)