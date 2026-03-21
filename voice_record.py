#!/usr/bin/env python3
import sys
import subprocess
import os
import threading
import warnings

warnings.filterwarnings("ignore")
import whisper
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

TMP_FILE = "/tmp/opencode_voice.wav"
recording_done = threading.Event()
transcript_result = [None]
rec_proc = None


def notify(msg):
    subprocess.run(
        ["curl", "-s", "-X", "POST", "https://ntfy.sh/OpenCode", "-d", msg],
        capture_output=True,
    )


def get_terminal_window_frame():
    try:
        script = """
        tell application "System Events"
            set terminalFound to false
            try
                tell process "Terminal"
                    if exists window 1 then
                        set winPos to position of window 1
                        set winSize to size of window 1
                        set terminalFound to true
                    end if
                end tell
            end try
            if not terminalFound then
                try
                    tell process "iTerm"
                        if exists window 1 then
                            set winPos to position of window 1
                            set winSize to size of window 1
                            set terminalFound to true
                        end if
                    end tell
                end try
            end if
            if terminalFound then
                return (item 1 of winPos as string) & "," & (item 2 of winPos as string) & "," & (item 1 of winSize as string) & "," & (item 2 of winSize as string)
            else
                return "notfound"
            end if
        end tell
        """
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, timeout=3
        )
        output = result.stdout.strip()
        if output and output != "notfound":
            parts = output.split(",")
            if len(parts) == 4:
                return map(int, parts)
    except:
        pass
    return None, None, None, None


def main():
    global rec_proc

    app = QApplication([])

    x, y, w, h = get_terminal_window_frame()
    if x is not None:
        btn_x = x + w - 130
        btn_y = y + h - 60
    else:
        screen = app.desktop().screenGeometry()
        btn_x = screen.width() - 130
        btn_y = screen.height() - 60

    w = QWidget()
    w.setFixedSize(120, 40)
    w.move(btn_x, btn_y)
    w.setWindowFlags(
        Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
    )

    btn = QPushButton("⏹ Stop", w)
    btn.setFixedSize(120, 40)
    btn.setFont(QFont("Arial", 13, QFont.Bold))
    btn.setStyleSheet(
        "background-color: #e74c3c; color: white; border-radius: 20px; border: none;"
    )

    app_ref = [app]

    def on_stop():
        global rec_proc
        btn.setText("...")
        btn.setEnabled(False)
        if rec_proc:
            rec_proc.terminate()
        recording_done.set()

        btn.setText("⏳")
        btn.setStyleSheet(
            "background-color: #3498db; color: white; border-radius: 20px; border: none;"
        )

        def transcribe():
            if os.path.exists(TMP_FILE) and os.path.getsize(TMP_FILE) > 1000:
                notify("⏳ Transcription...")
                try:
                    model = whisper.load_model("medium")
                    result = model.transcribe(
                        TMP_FILE, language="fr", task="transcribe"
                    )
                    transcript = result["text"].strip()
                    os.remove(TMP_FILE)
                    transcript_result[0] = transcript
                    if transcript:
                        notify(f"✅ {transcript}")
                        btn.setText("✅")
                        btn.setStyleSheet(
                            "background-color: #27ae60; color: white; border-radius: 20px; border: none;"
                        )
                    else:
                        notify("❌ Vide")
                        btn.setText("❌")
                except Exception as e:
                    notify(f"❌ Erreur: {str(e)}")
                    btn.setText("❌")
            else:
                transcript_result[0] = ""
                btn.setText("❌")

            threading.Timer(1.5, lambda: app_ref[0].quit()).start()

        threading.Thread(target=transcribe, daemon=True).start()

    btn.clicked.connect(on_stop)
    w.show()

    def record_audio():
        global rec_proc
        rec_proc = subprocess.Popen(
            [
                "rec",
                "--no-show-progress",
                "--rate",
                "16000",
                "--channels",
                "1",
                "--encoding",
                "signed-integer",
                "--bits",
                "16",
                TMP_FILE,
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        rec_proc.wait()
        recording_done.set()

    threading.Thread(target=record_audio, daemon=True).start()

    app.exec_()
    transcript = transcript_result[0]
    print(transcript if transcript else "")


if __name__ == "__main__":
    main()
