# Safety notes (draft, plan stage)
- This board is planned to connect **230 V AC**: fuse, varistor, HLK-5M05 input, relay contacts and screw terminals. Nothing has been built, measured or reviewed by a qualified engineer.
- Do not power any prototype from mains until the engineer-review list in [PLAN.md](../PLAN.md) section 14 is closed.
- Program and test over USB with mains **disconnected**. USB ground is the isolated secondary of the HLK module.
- Relays are intended to pulse a contactor or control circuit, not to switch a pump motor directly.
- Keep the mains/SELV slot clear, use an enclosure with finger-safe terminals, and install only if you are competent with mains wiring.
