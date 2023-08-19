import gradio as gr
import os
import time

def wait_for_file(file_path):
    """Waits for the specified file to be available."""
    while True:
        if os.path.exists(file_path):
            return True
        time.sleep(2)  # wait for two seconds

def tortoise_tts(text, voice, speed, emotion_prompt=False):
    # If emotion prompt is used, prepend the text with emotion text
    if emotion_prompt:
        emotion_mapping = {
            "Happy": "[I'm so happy!!]",
            "Sad": "[I'm feeling sad and sorrow!]",
            "Scared": "[I so coward & scared!]",
            "Brave": "[I'm the king of the world!]",
            "Angry": "[I'm so Angry!]",
            "Surprised": "[wow! I'm so Surprised!]",
            "Relaxed": "[Relaxe! take deep breath!]",
            "Neutral": ""
        }
        text = emotion_mapping[emotion_prompt] + " " + text

    # Decide which script to use based on text length
    if len(text.split()) <= 50:  
        cmd = f"python tortoise/do_tts.py --text \"{text}\" --voice {voice} --preset {speed}"
        os.system(cmd)
        
        # Assuming the audio files are generated as per the format provided
        prefix = "random" if voice == "random" else voice
        files = [f"results/{prefix}_0_{i}.wav" for i in range(3)]
        
        # Wait for the files to be generated before proceeding
        wait_for_file(files[-1])  # only wait for the last file in the list
    else:
        with open("tortoise/text.txt", "w") as file:
            file.write(text)
        cmd = f"python tortoise/read.py --textfile tortoise/text.txt --voice {voice} --preset {speed}"
        os.system(cmd)
        
        # Since only one file is generated for long text
        combined_path = f"results/longform/{voice}/combined.wav.wav"
        wait_for_file(combined_path)
        return (combined_path, None, None)  # Only one file is returned

    return tuple(files)

voice_options = ["random"] + [folder for folder in os.listdir("tortoise/voices")]
speed_options = ["ultra_fast", "fast", "standard", "high_quality"]
emotion_options = ["Neutral", "Happy", "Sad", "Scared", "Brave", "Angry", "Surprised", "Relaxed"]

examples = [
    ["Greetings, traveler! I am the guardian of these ancient ruins. Many have tried to uncover its secrets, but few have succeeded.", "train_atkins", "standard", "Neutral"],
    ["How dare you trespass into my lair! Leave now, or face the wrath of a thousand flames.", "tom", "fast", "Angry"],
    ["The moonlight casts a silver glow, and the night sings a song of solitude and memories.", "train_lescault", "ultra_fast", "Sad"],
    ["By the whiskers of my beard! I've never seen a gem sparkle like that before.", "train_daws", "standard", "Surprised"],
    ["Close your eyes, take a deep breath, and let the worries of the world fade away. Embrace the serenity within.", "train_dreams", "ultra_fast", "Relaxed"],
    ["It's been ages! I never thought we'd meet again in this lifetime. The stars have truly aligned.", "snakes", "fast", "Happy"]
]

iface = gr.Interface(
    fn=tortoise_tts, 
    title="TORTOISE-TTS GUI",
    description="Addaft by Shmuel Ronen",
    inputs=[
        gr.components.Textbox(placeholder="Enter text here..."),
        gr.components.Dropdown(voice_options, label="Select Voice:"),
        gr.components.Dropdown(speed_options, label="Product quality:"),
        gr.components.Dropdown(emotion_options, label="Experimental emotional expression:")
    ], 
    outputs=[
        gr.components.Audio(label="Result 1", type="filepath"),
        gr.components.Audio(label="Result 2", type="filepath"),
        gr.components.Audio(label="Result 3", type="filepath")
    ],
    examples=examples,
    live=False,
    flagging_options=[]
)

iface.launch()
