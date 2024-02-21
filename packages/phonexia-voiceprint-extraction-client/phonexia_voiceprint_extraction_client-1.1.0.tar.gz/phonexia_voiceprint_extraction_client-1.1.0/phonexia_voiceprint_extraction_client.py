#!/usr/bin/env python3

import argparse
import logging
import os
import pathlib
from typing import Iterator, Optional

import google.protobuf.duration_pb2
import grpc
import phonexia.grpc.common.core_pb2 as phx_common
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2 as sid
import phonexia.grpc.technologies.speaker_identification.v1.speaker_identification_pb2_grpc as sid_grpc


def time_to_duration(time: float) -> google.protobuf.duration_pb2.Duration | None:
    if time is None:
        return None
    duration = google.protobuf.duration_pb2.Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(file: str, start: float, end: float) -> Iterator[sid.ExtractRequest]:
    time_range = phx_common.TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    chunk_size = 1024 * 1024
    with open(file, mode="rb") as fd:
        while chunk := fd.read(chunk_size):
            yield sid.ExtractRequest(audio=phx_common.Audio(content=chunk, time_range=time_range))
            time_range = None


def voiceprint_path(audio_path: str) -> str:
    suffix = ".ubj"
    return str(pathlib.Path(audio_path).with_suffix(suffix))


def write_voiceprint(path: str, content: bytes) -> None:
    with open(path, "wb") as f:
        f.write(content)


def write_result(audio_path: str, response: sid.ExtractResponse) -> None:
    vp_path = voiceprint_path(audio_path)
    logging.info(f"Writing voiceprint to {vp_path}")
    write_voiceprint(vp_path, response.result.voiceprint.content)

    print(
        f"Audio: {audio_path}\n"
        f"Total billed time: {response.processed_audio_length.ToTimedelta()}\n"
        "Voiceprint:\n"
        f" speech length: {response.result.speech_length.ToTimedelta()}\n"
        f" voiceprint file: {vp_path}",
        end="\n\n",
    )


def extract_vp(
    channel: grpc.Channel, file: str, start: Optional[float], end: Optional[float]
) -> None:
    logging.info(f"Extracting voiceprints from {file}")
    stub = sid_grpc.VoiceprintExtractionStub(channel)
    write_result(file, stub.Extract(make_request(file, start, end)))


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Voiceprint extraction gRPC client. Extracts voiceprint from an input audio file."
        ),
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
    parser.add_argument("file", type=str, help="input audio file")

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
                extract_vp(channel, args.file, args.start, args.end)
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                extract_vp(channel, args.file, args.start, args.end)

    except grpc.RpcError:
        logging.exception("RPC failed")
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
