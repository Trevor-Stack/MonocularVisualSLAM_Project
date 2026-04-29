#!/usr/bin/env python3
"""
Add motion blur to camera images in EuRoC ROS1 bag files.

Usage:
    python add_motion_blur.py <input.bag> <output.bag> --kernel-size 5
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from rosbags.rosbag1 import Reader, Writer
from rosbags.typesys import Stores, get_typestore

IMAGE_TOPICS = {"/cam0/image_raw", "/cam1/image_raw"}


def make_motion_kernel(size: int, angle_deg: float) -> np.ndarray:
    """Return a normalized linear motion-blur kernel of given size and angle."""
    kernel = np.zeros((size, size), dtype=np.float32)
    center = size // 2
    kernel[center, :] = 1.0
    M = cv2.getRotationMatrix2D((center, center), angle_deg, 1.0)
    kernel = cv2.warpAffine(kernel, M, (size, size))
    kernel /= kernel.sum()
    return kernel


def apply_motion_blur(image: np.ndarray, kernel_size: int, rng: np.random.Generator) -> np.ndarray:
    """Apply random-direction motion blur to a grayscale or color image."""
    angle = rng.uniform(0, 360)
    kernel = make_motion_kernel(kernel_size, angle)
    blurred = cv2.filter2D(image, -1, kernel)
    return blurred


def process_bag(input_path: str, output_path: str, kernel_size: int, seed: int = 42) -> None:
    typestore = get_typestore(Stores.ROS1_NOETIC)
    rng = np.random.default_rng(seed)

    with Reader(input_path) as reader:
        image_conns = {c for c in reader.connections if c.topic in IMAGE_TOPICS}

        total_images = sum(c.msgcount for c in image_conns)
        processed = 0

        with Writer(output_path) as writer:
            conn_map = {}
            for conn in reader.connections:
                conn_map[conn.id] = writer.add_connection(
                    conn.topic,
                    conn.msgtype,
                    msgdef=conn.msgdef.data if conn.msgdef else None,
                    md5sum=conn.digest,
                    callerid=conn.ext.callerid if conn.ext else None,
                    latching=conn.ext.latching if conn.ext else None,
                )

            for conn, timestamp, rawdata in reader.messages():
                out_conn = conn_map[conn.id]
                if conn not in image_conns:
                    writer.write(out_conn, timestamp, rawdata)
                    continue

                msg = typestore.deserialize_ros1(rawdata, conn.msgtype)

                h, w = msg.height, msg.width
                encoding = msg.encoding

                if encoding == "mono8":
                    image = np.frombuffer(msg.data, dtype=np.uint8).reshape(h, w)
                elif encoding in ("bgr8", "rgb8"):
                    image = np.frombuffer(msg.data, dtype=np.uint8).reshape(h, w, 3)
                elif encoding == "mono16":
                    image = np.frombuffer(msg.data, dtype=np.uint16).reshape(h, w)
                else:
                    writer.write(out_conn, timestamp, rawdata)
                    processed += 1
                    continue

                blurred = apply_motion_blur(image, kernel_size, rng)
                msg.data = np.ascontiguousarray(blurred, dtype=np.uint8).ravel()

                new_rawdata = typestore.serialize_ros1(msg, conn.msgtype)
                writer.write(out_conn, timestamp, new_rawdata)

                processed += 1
                if processed % 200 == 0 or processed == total_images:
                    print(f"  [{processed}/{total_images}] images processed", flush=True)

    print(f"Done: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Add motion blur to EuRoC bag images")
    parser.add_argument("input", help="Input .bag file")
    parser.add_argument("output", help="Output .bag file")
    parser.add_argument(
        "--kernel-size", type=int, default=15,
        help="Motion blur kernel length in pixels (default: 15). "
             "Suggested levels: light=5, medium=9, heavy=15",
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    out = Path(args.output)
    if out.exists():
        out.unlink()
        print(f"Removed existing {args.output}")

    print(f"Input:  {args.input}")
    print(f"Output: {args.output}")
    print(f"Kernel size: {args.kernel_size}")
    process_bag(args.input, args.output, args.kernel_size, args.seed)


if __name__ == "__main__":
    main()
