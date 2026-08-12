# OPERATION B.A.R.K. — MAP DESIGN

Running design doc for the whole world. One section per area.
Started 2026-08-12. Expected to take many sessions — nothing here evaporates between them.

**Status key:** `LOCKED` = decided, build to it. `OPEN` = still a question. `IDEA` = Claude's pitch, unconfirmed.

---

## RULES THAT GOVERN EVERY AREA

Carried over from the design sessions. These apply to all maps, not just one.

- **Genre is metroidvania.** The map IS the ability graph.
- **The roster is the progression gate.** Rescue a doggo → they become playable → their signature move is the key to somewhere new. DB's character-select screen IS the ability menu. Zero new UI.
- **Swap anywhere, instantly.** Traversal is a chord: dig → swap → glide → swap.
- **Bosses are rescues.** Each boss gets its own bespoke fight concept — no universal chip-break verb.
- **Getting the band off ENDS the fight.** That's the win. Killing requires beating them a *second* time while they thank you. Must be impossible to do by accident.
- **Undertale endings.** Kill a main-cast doggo → lose their move forever → whole regions stay permanently sealed.
- **Every coin is hand-placed and unique.** Sinks: secret levels, tolls/shortcut doors, a shop doggo, paying for information.
- **Regular robo doggos and brutes are just machines.** Smashing them is guilt-free. Only the main cast is chipped.
- **THE WORLD IS ONE CONNECTED MAP, LIKE HOLLOW KNIGHT.** `LOCKED`
  No hub. No level select for the main world. You walk everywhere, and going back to an old area
  means walking back. **Secret maps are the only exception** — those get their own load screens.
  This supersedes the earlier "Lego Star Wars hub" idea for the main world.

### Combat numbers

| | HP | Notes |
|---|---|---|
| Robo doggo | 145 | standard patrol unit |
| Brute robo | 175 | the heavy |
| BARKmc's dash | 5 dmg | the standard DB move, a charge/dash |

**5 DAMAGE IS FINAL. YOU CANNOT WIN A FIGHT AS BARKmc.** `LOCKED`

29 dashes to kill one robot is not a fight, it's a statement. The dash was never an attack —
**it is a dodge that happens to hurt a little.** You solve the bunker by making the robots
**shoot each other and hit each other.** You bait a laser and step out of its line; the robot
behind you eats it. Brutes swing and clip their own squad.

This makes BARKmc's chapter a **positioning puzzle wearing a fight's clothing** — a different
genre from the rest of the game, on purpose. Once you have a roster, you can actually punch.

---

## THE CAST

**Player: BARKmc** — `OPEN`, placeholder name, stands for "BD OP BARK Main Character."
He is Xanboo78o's Doggo wearing the grey collar with a red and a yellow light: **the chip he tore off.**

- **Move 1 — THE CHIP.** Robo doors open for him. `LOCKED`
  - **The chip is a disguise, not a power.** The doors think he's one of them. He isn't strong, he's *invisible*.
- **Move 2 — THE DASH.** The standard DB charge/dash. 5 damage. `LOCKED`

**First rescue: DALMATIAN.** `LOCKED`

**The throughline:** Dalmatian is Doggo's best friend. Doggo is the most heavily guarded doggo in
the game — so he is the *last* rescue. Dalmatian is therefore with you for the entire game, pushing
you toward the final door.

> `IDEA` — In DB canon, Normal Doggo is a **villain** (taunts Qorvex through a door in the "Qorvex?"
> teaser; antagonist of Doggo Battles Infection). So "most heavily guarded" may not mean *imprisoned*.
> The first friend you make spends the whole game begging you to save someone who doesn't want saving.

Full roster (15): BARKmc · Dalmatian · Cowboy · Knight · Alien · King · Zombie · Cool · Toxic ·
Plasma · Qorvex (locked/unpickable) · Billie · Tall Doggo · Glider · Digger

---

## CHAPTERS

The game is told in chapters. `LOCKED`

- **CHAPTER 1 — THE BUNKER.** You are alone. No roster, no allies. The whole chapter is you
  learning how the world around you works.
- **CHAPTER 3** — Shapeshifter unlocks here.
- Remaining chapter boundaries: `OPEN`.

---

## AREA 1 — THE BUNKER  ·  CHAPTER 1

**The only place in the game you are alone.** Every other area is played with a roster and a radial
swap menu. The bunker has to be good *specifically* at being small, because there is nothing to swap to.

It is also the only tutorial the game gets.

### Structure — three beats `LOCKED`

| | Beat | Encounter |
|---|---|---|
| **Front** | Opening | **LASER-DOG** |
| **Middle** | The turn | **A dismantled robo doggo** |
| **End** | Climax | **Three robo doggos** |

### Casting — all art already exists `LOCKED`

| Role | Art file | Why |
|---|---|---|
| **LASER-DOG** | `Robo-Doggo-Cyclops.png` | one big red eye on the headband. It's an eye that shoots. |
| **THE DISMANTLED ONE** | `Scrapped-Robo-Doggo.png` | literally torn apart, ragged edges, one dying red dot |
| **THE BRUTE** | `heavyrobodoggo.png` | two red eyes, wide plated body. 175 HP. Melee. |
| **Patrol robos** | `Robo-Doggo-V1..V4.png` | the standard units. 145 HP. |

### THE TEN MINUTES — room by room `LOCKED`

The whole area teaches one verb: **their weapons are your weapons.** It escalates in three steps —
laser vs *wall*, then laser vs *robot*, then a room where you need both.

**1 · THE CELL — 0:00** · teaches MOVE, JUMP, and the chip
Wake up in a cell. The door is a robo door. You walk into it and **it opens** — because you're
wearing the chip. The first thing the game teaches you is that you are disguised. No enemies.

**2 · THE CELL BLOCK — 0:45** · teaches the premise, with no cutscene
A long corridor of cells, all standing open, all empty, a doghouse in each one. Nobody is here.
Easy jumps, first coins.

**3 · LASER-DOG — 2:00** · teaches THE VERB, in its simplest possible form
A Cyclops holds the corridor. 145 HP against your 5 damage — you cannot win. The way out is behind
a **cracked panel**, and the only thing in the bunker strong enough to break it is his laser.
Stand in front of it. Bait the shot. Dash aside. *One robot, one wall.*

**4 · THE DISMANTLED ONE — 4:00** · the turn. Exposition and both promises.
The Scrapped robo, torn in half and still running its script. It tells you where everyone went: **up.**
Visible from this room and unreachable for hours:
- **the flooded stairwell** — dark water going down → THE AQUADEPTHS
- **the doggo-locked door** — your chip does nothing → DELETION DEPTHS HIGHWAY

**5 · THE PATROL — 5:30** · teaches the verb again, escalated: robot vs robot
A Cyclops and a brute in one room. Now you line *them* up on each other. The brute swings and
clips its own squad; the laser cuts through whatever's behind you.

**6 · THE GUARD ROOM — 7:30** · the exam
**Three robos around Dalmatian's cell.** 435 HP that has to come out of their own weapons.

**7 · DALMATIAN, AND UP — 9:30**
The cell opens. He walks out. **The roster goes from one to two** — the first time that screen
grows. Then a shaft going up, and at the top of it, the first daylight in the game.

### Dalmatian's rescue `LOCKED`

**He is a find, not a fight. You beat the bots, you get Dalmatian.**

The three robos are the obstacle; Dalmatian is the prize behind them. A dog walks out happy to
see you. Nobody has attacked you yet on purpose.

Which means the *second* rescue — the first chipped one, who comes at you swinging — is where the
player learns what a chip actually does. Free the first one easy so the second one hurts.

### Promises — what you can see and can't reach yet

The most metroidvania thing a starting area can do is give you reasons to come back to the very
first room. Slots in the bunker:

- **THE FLOODED STAIRWELL → THE AQUADEPTHS.** `LOCKED` The water region has a name now, and its
  front door is in the first area of the game. You will stand at the top of that water in minute
  three and not be able to go down it.
- a vent — `OPEN`
- a ceiling hatch — `OPEN` (→ Alien's jump, or Glider)
- a wall of loose dirt — `OPEN` (→ Digger)
- **a door that is *not* a robo door** — `OPEN`. The chip doesn't open it. Everything in the bunker
  opens for you because the machines think you're a machine — so what did a *doggo* lock?

### Notes

- The dash is a **traversal** verb as well as an attack. The bunker can gate on dash distance.
- Escaping the bunker is the transition into the **grass** biome.

---

## THE REGIONS

Five biomes are drawn and sliced already, matching DB's five arenas. ~14 rescuable doggos over
5 regions ≈ 3 locked doors and 3 keys per region.

### THE SPINE — THE WORLD IS A CLIMB `LOCKED`

**The bunker is LOW. You start near the bottom and the entire game is above you.**

This is the opposite of Hollow Knight, and it fits a rescue story: every doggo you free, you free
on the way *up*.

```
            ROBO MOTHERSHIP ALPHA        ← IN THE SKY. Doggo. The final area.
                        ▲
                   the FLY-BUS           ← you hitch a ride
                        ▲
         [ grass · rock · wildfire · city ]   names + order OPEN
                        ▲
                   THE BUNKER            ← you start here. low. a crossroads.
              ╱                    ╲
   flooded stairwell        the doggo-locked door
              ▼                    ▼
       THE AQUADEPTHS     DELETION DEPTHS HIGHWAY   ← the vertical shaft
                                     ▼
                            THE DELETION DUMP       ← the floor. Qorvex.
```

**THE BUNKER IS THE HINGE OF THE WHOLE MAP.** One way up into the world, and **two separate ways
down** — both of them sealed in minute three. It is a crossroads you can't use yet.

**The downward pull.** Everything beneath your starting room is unreachable. You spend the whole
game climbing away from the bottom — and to get Qorvex you come back down, past where you started,
to the floor of the world. **The Deletion Dump is underneath the first room.**

### THE ARC OF THE DISGUISE

Not planned — it fell out of three separate decisions. Worth protecting.

1. **THE BUNKER — the disguise works.** The chip opens robo doors. The machines think you're one
   of them. You are not strong, you are invisible.
2. **THE DELETION DEPTHS HIGHWAY — the disguise stops mattering.** Fewer robots the deeper you go.
   Nothing left to fool. Cursors don't check ID.
3. **THE FLY-BUS — the disguise fails.** You board disguised; the robos *eventually work it out*,
   and the endgame starts because your oldest trick finally ran out.

| Art sheet | Region | Status |
|---|---|---|
| — | **THE BUNKER** | Area 1. No art sheet yet. |
| `grass` | — | unnamed. The bunker escapes up into it. |
| `rock` | — | unnamed |
| `wildfire` | — | unnamed. Adam's sheet says "(Add fire, and smoke)" — effects not built. |
| `city` | — | unnamed |
| `water` | **THE AQUADEPTHS** | `LOCKED`. Front door is the bunker's flooded stairwell. |
| — | **DELETION DEPTHS HIGHWAY** | `LOCKED`. The shaft down. **No art sheet yet.** |
| — | **THE DELETION DUMP** | `LOCKED`. Bottom of the map. **No art sheet yet.** |
| — | **ROBO MOTHERSHIP ALPHA** | `LOCKED`. In the sky. Doggo. **No art sheet yet.** |

### DELETION DEPTHS HIGHWAY `LOCKED`

Behind the bunker's doggo-locked door. **A hugeeeeee vertical shaft** — a giant dungeon in its own
right, not a corridor.

- **Jumping down instantly deletes you.** You cannot fall your way to the bottom. The descent is
  earned, slowly, by puzzle. A vertical shaft where falling is death inverts the usual thing:
  down is the hard direction.
- **Puzzles on puzzles.**
- **The gradient:** robots get fewer and fewer the deeper you go. Cursors and body-glitch horrors
  get *more*. The population swaps over as you descend.
- Consequence: **your chip becomes worthless by degrees** — not broken, just irrelevant. See
  "The arc of the disguise."

### ROBO MOTHERSHIP ALPHA `LOCKED`

**In the sky.** Where Doggo is. The last rescue and the top of the climb.

**Approach — the FLY-BUS.** You hitch a ride, disguised (`OPEN` — see Shapeshifter below).

- **There is a kennel ON the bus.** So the swap is live during the set piece — you fight it as
  **any doggo you like.** After a whole game of areas gating which doggo you can be, the finale
  hands you the entire roster at once and says: pick.
- **The disguise expires.** The robos eventually work out you're not one of them, and that's the
  fight starting. You take them all out.

**SHAPESHIFTER** `LOCKED` — a doggo, but a **lesser one**. Not a main character.
**UNLOCKED IN CHAPTER 3.** Used a few times after that; boarding the fly-bus is his biggest job.
He does not exist in Chapter 1 and must not drift earlier — Chapter 1 is a solo area by design.

### THE DELETION DUMP `LOCKED`

The bottom of the world. **Where you free Qorvex.**

- Enemies are **body-glitch horror** and **MOUSE CURSORS.**
- This is where deleted sprites go. The cursor that deleted them still hunts down there.
- **It explains Qorvex's art.** He's drawn twice — clean (`Qorvex.png`) and torn (`Qorvex-glitch.png`)
  — and the game already flicks between them so he never holds still. That was a style choice with
  no reason behind it. Now it has one: **he is a deleted sprite.** The glitch is his address.
- `OPEN` — needs an art sheet. It's the only region with no drawing.

### WATER

`OPEN` — **nobody in the roster can swim.** Adam: *"there will be a Water doggo eventually."*
Unassigned. Aquadepths is named and its front door is built into Area 1, but it has no key yet.
