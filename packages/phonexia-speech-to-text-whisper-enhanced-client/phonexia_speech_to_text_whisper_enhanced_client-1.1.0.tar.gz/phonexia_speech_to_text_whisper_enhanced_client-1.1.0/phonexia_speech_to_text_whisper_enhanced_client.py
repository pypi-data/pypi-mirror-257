import argparse
import logging
import os
from typing import Iterator, Optional

import google.protobuf.duration_pb2
import grpc
import phonexia.grpc.technologies.speech_to_text_whisper_enhanced.v1.speech_to_text_whisper_enhanced_pb2_grpc as stt_grpc
from phonexia.grpc.common.core_pb2 import Audio, TimeRange
from phonexia.grpc.technologies.speech_to_text_whisper_enhanced.v1.speech_to_text_whisper_enhanced_pb2 import (
    TranscribeConfig,
    TranscribeRequest,
)

CHUNK_SIZE = 32000


def time_to_duration(time: float) -> google.protobuf.duration_pb2.Duration | None:
    if time is None:
        return None
    duration = google.protobuf.duration_pb2.Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def request_iterator(
    file: str,
    specified_language: Optional[str],
    start: Optional[float],
    end: Optional[float],
    enable_language_switching: bool = False,
) -> Iterator[TranscribeRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    config = TranscribeConfig(
        language=specified_language, enable_language_switching=enable_language_switching
    )

    with open(file, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            yield TranscribeRequest(
                audio=Audio(content=chunk, time_range=time_range), config=config
            )
            time_range = None
            config = None


def transcribe(
    channel: grpc.Channel,
    file: str,
    language: Optional[str],
    start: Optional[float],
    end: Optional[float],
    enable_language_switching: bool = False,
):
    stub = stt_grpc.SpeechToTextStub(channel)
    response = stub.Transcribe(
        request_iterator(
            file=file,
            specified_language=language,
            start=start,
            end=end,
            enable_language_switching=enable_language_switching,
        )
    )
    for _response in response:
        for segment in _response.result.one_best.segments:
            print(
                f"[{segment.start_time.ToJsonString()} ->"
                f" {segment.end_time.ToJsonString()} {segment.language}] {segment.text}"
            )
        if _response.HasField("processed_audio_length"):
            print(f"Processed audio length: {_response.processed_audio_length.ToJsonString()}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Speech To Text Whisper Enhanced gRPC client. Transcribes input audio into segments"
            " with timestamps."
        )
    )

    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
        help="Server address, default: localhost:8080",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="error",
        choices=["critical", "error", "warning", "info", "debug"],
    )
    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")

    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help=(
            "Force transcription to specified language, if not set, language is detected"
            " automatically"
        ),
    )
    parser.add_argument(
        "--enable-language-switching",
        action="store_true",
        help="Enable dynamic language switching during transcription, with the language being detected approximately every 30 seconds",
    )
    parser.add_argument("file", type=str, help="Path to input file")

    args = parser.parse_args()

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")

    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not os.path.isfile(args.file):
        logging.error(f"no such file {args.file}")
        exit(1)

    try:
        logging.info(f"Connecting to {args.host}")
        if args.use_ssl:
            with grpc.secure_channel(
                target=args.host, credentials=grpc.ssl_channel_credentials()
            ) as channel:
                transcribe(
                    channel=channel,
                    file=args.file,
                    language=args.language,
                    start=args.start,
                    end=args.end,
                    enable_language_switching=args.enable_language_switching,
                )
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                transcribe(
                    channel=channel,
                    file=args.file,
                    language=args.language,
                    start=args.start,
                    end=args.end,
                    enable_language_switching=args.enable_language_switching,
                )

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
