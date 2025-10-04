import vlc
import time
import shutil
import sys
import os
from mutagen import File

# --- Arguments ---
if len(sys.argv) > 1:
    audio_file = sys.argv[1]
else:
    audio_file = sys.stdin.readline().strip()

if not os.path.exists(audio_file):
    print("File not found!")
    sys.exit(1)

# Optional display name
if len(sys.argv) > 2:
    display_name = sys.argv[2]
else:
    # Try to grab tags from file
    audio = File(audio_file)
    if audio is not None and audio.tags is not None:
        title = audio.tags.get("TIT2")
        artist = audio.tags.get("TPE1")
        if title and artist:
            display_name = f"{artist[0]} - {title[0]}"
        elif title:
            display_name = title[0]
        else:
            display_name = os.path.basename(audio_file)
    else:
        display_name = os.path.basename(audio_file)

# --- Metadata ---
audio = File(audio_file)
if audio is not None and hasattr(audio, "info"):
    length_sec = getattr(audio.info, "length", None)
#    if length_sec:
#        print(f"Track length: {length_sec:.2f} seconds")

# Print initial info
print(f"Now playing: {display_name}")

# --- VLC Player ---
player = vlc.MediaPlayer(audio_file)
player.play()
time.sleep(0.5)  # let VLC parse

def format_time(ms):
    if ms <= 0:
        return "0:00"
    seconds = int(ms / 1000)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"

# Wait for VLC to report length
total = player.get_length()
retry_count = 0
while total <= 0 and retry_count < 50:
    time.sleep(0.1)
    total = player.get_length()
    retry_count += 1

if total <= 0:
    total = 1  # Prevent div zero

try:
    last_progress_line = ""
    while True:
        state = player.get_state()
        if state in [vlc.State.Ended, vlc.State.Error]:
            break

        width = shutil.get_terminal_size().columns
        current = player.get_time()

        progress = min(current / total, 1.0) if total > 0 else 0
        bar_width = max(width - 30, 10)
        filled = int(progress * bar_width)
        bar = "=" * filled + " " * (bar_width - filled)

        progress_text = f"[{bar}] {int(progress*100)}% | {format_time(current)}/{format_time(total)}"

        if len(progress_text) > width:
            progress_display = progress_text[:width]
        else:
            progress_display = progress_text.ljust(width)

        if progress_display != last_progress_line:
            print(f"\r{progress_display}", end='', flush=True)
            last_progress_line = progress_display

        time.sleep(0.05)

    print()
    print("Playback finished!")

except KeyboardInterrupt:
    print()
    print("Stopped!")
except Exception as e:
    print()
    print(f"Error: {e}")
finally:
    player.stop()
