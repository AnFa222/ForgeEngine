# Game Loop & Lifecycle

## Game Loop Overview

The game loop is the heart of ForgeEngine. It runs continuously from when `engine.main_loop()` is called until the game closes.

### High-Level Flow

```mermaid
graph TD
    Start["engine.main_loop()"] -->|Once| Init["Initialize:<br/>- Collect Components<br/>- Get Cameras<br/>- Call start() on objects"]
    Init --> Loop["Main Loop"]
    Loop -->|Each Frame| PollEvents["1. Poll Window Events"]
    PollEvents --> CheckQuit{"Quit Event?"}
    CheckQuit -->|Yes| End["Exit Loop"]
    CheckQuit -->|No| GetComp["2. Get Components"]
    GetComp --> CalcDT["3. Calculate Delta Time"]
    CalcDT --> Input["4. Handle Input"]
    Input --> DestroyObj["5. Destroy Queued Objects"]
    DestroyObj --> UpdateTime["6. Update Timers"]
    UpdateTime --> EarlyUpdate["7. Early Update<br/>(Scripts run)"]
    EarlyUpdate --> Physics["8. Update Physics"]
    Physics --> Animation["9. Update Animation"]
    Animation --> Update["10. Update<br/>(Scripts run)"]
    Update --> Clear["11. Clear Screen"]
    Clear --> Render["12. Render Objects"]
    Render --> Audio["13. Handle Audio"]
    Audio --> Loop
    End --> Shutdown["Cleanup"]
