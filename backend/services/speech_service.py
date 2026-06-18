from faster_whisper import WhisperModel


class SpeechService:

    model = WhisperModel(
        "base"
    )

    @classmethod
    def transcribe(
        cls,
        audio_file
    ):

        segments, _ = (
            cls.model.transcribe(
                audio_file
            )
        )

        text = ""

        for segment in segments:

            text += (
                segment.text
                + " "
            )

        return text.strip()