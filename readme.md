# Zola Combo Console (Python Port)

This is a **Python-based port** of the original C++ "Zola Console" created by **Evil Duck**, a toolkit used to simulate, optimize, and evaluate combo strings in *Marvel Rivals* Spiderman gameplay.

The purpose of this console is to simulate sequences of actions (like tracers, swings, jump overheads, etc.) and evaluate their damage and frame cost under realistic conditions (with cooldowns, airborne states, buffs, and more).

---

## 🎮 Features

- Rewritten entirely in Python for portability and easier development
- Fully supports original mechanics:
  - Tracer and BurnTracer stacking
  - Frame-based cooldown simulation
  - Buff scaling (Seasonal and Mantis)
  - Melee combo sequence tracking
- Interactive console UI to input and simulate combos
- Easily extendable for new moves or characters

---

## 🚀 Getting Started

Clone this repo and run:

```bash
python main.py
```

You’ll enter a console where you can enter commands like:

```bash
>> calc tp
>> set hasMantisBuff 1
>> calc tbpu
>> properties
```

---

## 🧠 Commands

- `help` — Shows available commands
- `calc [actions]` — Simulates a combo string
- `set [property] [value]` — Modifies starting state
- `properties` — Prints current simulation state
- `actions` — Lists key mappings for actions
- `exit` — Quits the console

---

## 🎮 Action Key Map

| Key | Action                   |
|-----|--------------------------|
| j   | Jump                     |
| l   | Land                     |
| p   | Melee Punch              |
| P   | Melee Punch (second hit) |
| k   | Melee Kick               |
| o   | Overhead                 |
| t   | Tracer                   |
| b   | Burn Tracer (Inferna)    |
| s   | Swing                    |
| w   | Swing Whiff              |
| g   | Get Over Here            |
| G   | Get Over Here Targetting |
| u   | Uppercut                 |
| f   | FFame Stack              |
| n   | Saporen                  |

---

## 🛠 Status

✅ Core logic ported  
✅ BurnTracer and damage DoT implemented  
✅ Fully interactive console  
🔜 Combo generator (`gen`, `genf`)  
🔜 GUI frontend  

---

## 📜 Credits & Source

This is a faithful port of the **Zola Console** by **Evil Duck**.  
**Original C++ source** and video:  
📎 [Get the source code for the Zola Console (Google Drive)](https://drive.google.com/drive/folders/1wlQ0qxPRk73b1lVlOpOaTdNf_MmwdGTW)

> "Yeah, the source code is super ugly — it's not for your admiration and I don't expect even the most competent programmer to understand why I wrote it the way that I did, it's just for compiling."

> "Disclaimer: the timings aren't necessarily frame-perfect, but they're close enough to be useful."

**If you're interested in cutting-edge Spiderman tech, check these out:**

- FFame (join his Discord): [@ffamefs](https://www.youtube.com/@ffamefs)
- The Amazing Spiderman Playbook (courtesy of icegawd):  
  [Google Sheets Spreadsheet](https://docs.google.com/spreadsheets//u/0/d/1jqAZ5lBqqHAbt9BxX3eIn7MducMWYf34n0b5DpHYflw/htmlview#gid=0)

---

## 📂 License

This project is distributed for educational and experimental use.  
Original work by Evil Duck. Python port and enhancements by the community.
