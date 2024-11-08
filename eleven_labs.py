from playsound import playsound
import os
import uuid
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


voices = {
    "saul-dub": {"id": 'Dyt77XyVgLv7Zjv60RIk', "stability": 0.6, "similarity": 0.7, "style": 0, "speaker_boost": True, "image": 'saul-dub.png'},
    "rusandor": {"id": 'nVmhh1Ng3I1FjNWJ46Zb', "stability": 0.7, "similarity": 0.75, "style": 0, "speaker_boost": True, "image": 'rusandor.jpg'},
    "ramzan": {"id": 'DShsMnazdfKPnA276gRk', "stability": 0.5, "similarity": 0.75, "style": 0, "speaker_boost": True, "image": 'ramzan.jpg'},
}


def text_to_speech_file_eleven_labs(text: str, voice: str) -> str | None:
    if voice not in voices:
        print('voice is not in voices')
        return
    opts = voices[voice]
    response = client.text_to_speech.convert(
        voice_id=opts["id"],
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=opts['stability'],
            similarity_boost=opts['similarity'],
            style=opts['style'],
            use_speaker_boost=opts['speaker_boost']
        )
    )

    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path
