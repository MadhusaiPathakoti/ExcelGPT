from faster_whisper import WhisperModel


class SpeechService:

    model = WhisperModel(

        "tiny",

        device="cpu",

        compute_type="int8"
    )

    @classmethod
    def transcribe(
        cls,
        audio_file
    ):

        try:

            segments, _ = (
                cls.model.transcribe(
                    audio_file
                )
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            raise e

        text = ""

        for segment in segments:

            text += (
                segment.text
                + " "
            )

        return text.strip()