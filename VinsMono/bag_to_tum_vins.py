#!/usr/bin/env python

import argparse
import os

import rosbag


GT_TOPIC = "/vicon/firefly_sbx/firefly_sbx"
ODOM_TOPIC = "/vins_estimator/odometry"
PATH_TOPIC = "/pose_graph/pose_graph_path"


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_gt_tum(bag, output_path):
    with open(output_path, "w") as f:
        for _, msg, _ in bag.read_messages(topics=[GT_TOPIC]):
            ts = msg.header.stamp.to_sec()
            t = msg.transform.translation
            q = msg.transform.rotation
            f.write(
                "{:.9f} {} {} {} {} {} {} {}\n".format(
                    ts, t.x, t.y, t.z, q.x, q.y, q.z, q.w
                )
            )


def write_odom_tum(bag, output_path):
    with open(output_path, "w") as f:
        for _, msg, _ in bag.read_messages(topics=[ODOM_TOPIC]):
            ts = msg.header.stamp.to_sec()
            p = msg.pose.pose.position
            q = msg.pose.pose.orientation
            f.write(
                "{:.9f} {} {} {} {} {} {} {}\n".format(
                    ts, p.x, p.y, p.z, q.x, q.y, q.z, q.w
                )
            )


def write_path_tum(bag, output_path):
    last_path_msg = None
    for _, msg, _ in bag.read_messages(topics=[PATH_TOPIC]):
        last_path_msg = msg

    if last_path_msg is None:
        print("WARNING: No path found in bag")
        return

    with open(output_path, "w") as f:
        for pose_stamped in last_path_msg.poses:
            ts = pose_stamped.header.stamp.to_sec()
            p = pose_stamped.pose.position
            q = pose_stamped.pose.orientation
            f.write(
                "{:.9f} {} {} {} {} {} {} {}\n".format(
                    ts, p.x, p.y, p.z, q.x, q.y, q.z, q.w
                )
            )


def process_bag(bag_path, output_dir):
    print("Processing:", bag_path)

    bag_name = os.path.splitext(os.path.basename(bag_path))[0]

    gt_out = os.path.join(output_dir, bag_name + "_gt.tum")
    odom_out = os.path.join(output_dir, bag_name + "_odom.tum")
    path_out = os.path.join(output_dir, bag_name + "_slam.tum")

    bag = rosbag.Bag(bag_path, "r")
    try:
        write_gt_tum(bag, gt_out)
        write_odom_tum(bag, odom_out)
        write_path_tum(bag, path_out)
    finally:
        bag.close()

    print("  Saved:", gt_out)
    print("  Saved:", odom_out)
    print("  Saved:", path_out)


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert all rosbag files in a directory to TUM format."
    )
    parser.add_argument(
        "--bag_dir",
        default = ".",
        help="Directory containing .bag files"
    )
    parser.add_argument(
        "--out_dir",
        default=".",
        help="Output directory for TUM files"
    )
    args = parser.parse_args()

    ensure_dir(args.out_dir)

    for filename in os.listdir(args.bag_dir):
        if filename.endswith(".bag"):
            bag_path = os.path.join(args.bag_dir, filename)
            process_bag(bag_path, args.out_dir)

    print("\nDone processing all bags.")


if __name__ == "__main__":
    main()