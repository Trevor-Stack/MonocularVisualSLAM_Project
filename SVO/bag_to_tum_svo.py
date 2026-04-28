import rosbag
import os
import glob

def bag_to_tum(bag_path):
    base_name = os.path.splitext(os.path.basename(bag_path))[0]

    odom_file = "{}_odom.tum".format(base_name)
    slam_file = "{}_slam.tum".format(base_name)
    gt_file = "{}_gt.tum".format(base_name)

    bag = rosbag.Bag(bag_path)

    with open(odom_file, "w") as f:
        for topic, msg, t in bag.read_messages(topics=["/svo/pose_imu"]):
            ts = t.to_sec()
            p = msg.pose.pose.position
            q = msg.pose.pose.orientation
            f.write("{} {} {} {} {} {} {} {}\n".format(
                ts, p.x, p.y, p.z, q.x, q.y, q.z, q.w))
    print("Saved:", odom_file)

    with open(slam_file, "w") as f:
        for topic, msg, t in bag.read_messages(topics=["/svo/backend_pose_imu"]):
            ts = t.to_sec()
            p = msg.pose.pose.position
            q = msg.pose.pose.orientation
            f.write("{} {} {} {} {} {} {} {}\n".format(
                ts, p.x, p.y, p.z, q.x, q.y, q.z, q.w))
    print("Saved:", slam_file)

    with open(gt_file, "w") as f:
        for topic, msg, t in bag.read_messages(topics=["/vicon/firefly_sbx/firefly_sbx"]):
            ts = t.to_sec()
            tr = msg.transform.translation
            qr = msg.transform.rotation
            f.write("{} {} {} {} {} {} {} {}\n".format(
                ts, tr.x, tr.y, tr.z, qr.x, qr.y, qr.z, qr.w))
    print("Saved:", gt_file)

    bag.close()

bag_files = sorted(glob.glob("*.bag"))

if not bag_files:
    print("No .bag files found in current directory.")
else:
    for bag_path in bag_files:
        print("\nProcessing:", bag_path)
        bag_to_tum(bag_path)