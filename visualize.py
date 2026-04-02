import os
import shutil

try:
    from colorama import init as _cinit, Fore, Style
    _cinit(autoreset=True)
except ImportError:
    print("Run:  pip install colorama")
    raise

_log = []

def init_visualizer():
    pass

def close_visualizer():
    pass

# ── color helpers ────────────────────────────────────────────────────
def _red(s):     return Fore.RED     + str(s) + Style.RESET_ALL
def _green(s):   return Fore.GREEN   + str(s) + Style.RESET_ALL
def _yellow(s):  return Fore.YELLOW  + str(s) + Style.RESET_ALL
def _cyan(s):    return Fore.CYAN    + str(s) + Style.RESET_ALL
def _magenta(s): return Fore.MAGENTA + str(s) + Style.RESET_ALL
def _dim(s):     return Style.DIM    + str(s) + Style.RESET_ALL

# ── event constructors ───────────────────────────────────────────────
def ev_combat(text): return ("combat", text)
def ev_move(text):   return ("move",   text)
def ev_chest(text):  return ("chest",  text)
def ev_storm(text):  return ("storm",  text)
def ev_info(text):   return ("info",   text)

def _color_event(kind, text):
    if kind == "combat": return _red(text)
    if kind == "move":   return _cyan(text)
    if kind == "chest":  return _yellow(text)
    if kind == "storm":  return _red(text)
    return text

# ── layout ───────────────────────────────────────────────────────────
CELL_W   = 26
COLS     = 3
LOG_TAIL = 10

def _term_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80

def _clear():
    os.system("cls" if os.name == "nt" else "clear")

def _hp_bar(hp, max_hp=150, width=8):
    pct    = max(0, min(1, hp / max_hp))
    filled = round(pct * width)
    bar    = "█" * filled + "░" * (width - filled)
    if pct > 0.5:  return _green(bar)
    if pct > 0.2:  return _yellow(bar)
    return _red(bar)

def _visible_len(s):
    """Approximate visible length by stripping ANSI escape codes."""
    import re
    return len(re.sub(r'\x1b\[[0-9;]*m', '', s))

def _rpad(s, width):
    """Right-pad string s to visible width."""
    return s + " " * max(0, width - _visible_len(s))

def _zone_block(zone_name, agents, storm_zones, chests, all_agent_zones):
    is_storm  = zone_name in storm_zones
    has_chest = bool(chests.get(zone_name))
    occupants = all_agent_zones.get(zone_name, [])

    bc = _red if is_storm else _cyan
    lines = []

    title = f" {zone_name}"
    if is_storm:   title += " STORM"
    if has_chest:  title += " [CHEST]"
    inner_w = CELL_W - 2
    title_padded = title[:inner_w].center(inner_w, "-")
    lines.append(bc("+" + title_padded + "+"))

    if not occupants:
        lines.append(bc("|") + " " * inner_w + bc("|"))
    else:
        for name in occupants:
            info  = agents.get(name, {})
            alive = info.get("alive", False)
            hp    = info.get("hp", 0)
            lvl   = info.get("level", 1)
            strat = info.get("strategy", "")[:3].upper()
            if alive:
                dot  = _green("*")
                body = f"{name[:8]:<8} HP:{hp:<4}L{lvl} {strat}"
            else:
                dot  = _red("x")
                body = _dim(f"{name[:8]:<8} [DEAD]")
            content = dot + " " + body
            line = bc("|") + " " + _rpad(content, inner_w - 1) + bc("|")
            lines.append(line)

    lines.append(bc("+" + "-" * inner_w + "+"))
    return lines

def _pad_lines(lines, target_h):
    blank = " " * CELL_W
    while len(lines) < target_h:
        lines.append(blank)
    return lines

def draw(tick, agents, actions, storm_zones, chests, events=None):
    global _log
    if events:
        _log.extend(events)

    from env import group_by_zone
    all_zones       = [f"Zone_{i}" for i in range(1, 10)]
    all_agent_zones = group_by_zone()

    _clear()
    tw = min(_term_width(), 80)
    div = "=" * tw

    # ── header ───────────────────────────────────────────────────────
    alive_count  = sum(1 for a in agents.values() if a["alive"])
    storm_labels = ", ".join(sorted(storm_zones)) if storm_zones else "none"
    print(_cyan(div))
    print(_cyan("  BATTLE ROYALE") +
          f"  |  Tick: {_yellow(str(tick))}" +
          f"  |  Alive: {_green(str(alive_count))}" +
          f"  |  Storm: {_red(storm_labels)}")
    print(_cyan(div))

    # ── 3x3 zone grid ────────────────────────────────────────────────
    zone_rows = [all_zones[i*COLS:(i+1)*COLS] for i in range(3)]
    for row_zones in zone_rows:
        cell_lines = []
        for z in row_zones:
            lines = _zone_block(z, agents, storm_zones, chests, all_agent_zones)
            cell_lines.append(lines)
        max_h = max(len(l) for l in cell_lines)
        cell_lines = [_pad_lines(l, max_h) for l in cell_lines]
        for row_idx in range(max_h):
            print("".join(cell_lines[col][row_idx] for col in range(len(row_zones))))

    # ── agent table ───────────────────────────────────────────────────
    print()
    print(_cyan("-" * tw))
    print(f"  {'Name':<12} {'Status':<7} {'HP':<6} {'Lvl':<4} {'Strategy':<11} Action")
    print("  " + "-" * (tw - 4))
    for name, info in agents.items():
        alive = info["alive"]
        hp    = info["hp"]
        lvl   = info.get("level", 1)
        strat = info["strategy"]
        act, tgt = actions.get(name, ("idle", None))
        if act == "attack": act_str = _red(f"ATK {tgt}")
        elif act == "move":  act_str = _cyan(f"MOV -> {tgt}")
        else:                act_str = _dim("IDLE")
        status = _green("ALIVE ") if alive else _red("DEAD  ")
        print(f"  {name:<12} {status} {hp:<6} L{lvl:<3} {strat:<11} {act_str}")

    # ── event log ─────────────────────────────────────────────────────
    print()
    print(_cyan("-" * tw))
    print(f"  Event Log  (last {LOG_TAIL})")
    print("  " + "-" * (tw - 4))
    for kind, text in _log[-LOG_TAIL:]:
        print("  " + _color_event(kind, text))

    print()
    print(_dim("  [Enter] next tick    [Ctrl+C] quit"))
    print(_cyan("=" * tw))
