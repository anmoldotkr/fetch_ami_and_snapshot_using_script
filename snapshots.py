
import boto3
import csv

region = "us-west-2"
ec2_client = boto3.client("ec2", region_name=region)

response = ec2_client.describe_images(Owners=['self'])

ami_ids = []
snapshots = set()

# list to store CSV rows
csv_rows = []

for image in response["Images"]:

    # Adding Total Ami in Array then using len function getting total amis
    ami_ids.append(image['ImageId'])

    # creating variable (your fields)
    imageLocation = image['ImageLocation']
    ImageName = image.get("Name")
    amiIds = image['ImageId']

    print(f"Total AMI's:", len(ami_ids))
    print(f"Image Name:", ImageName)

    for bdm in image.get("BlockDeviceMappings", []):

        if "Ebs" in bdm and "SnapshotId" in bdm["Ebs"]:
            snapshot_id = bdm['Ebs']["SnapshotId"]
            snapshots.add(snapshot_id)

            print(f"snapshot ID's: ", snapshot_id)
            print(f"Total Snapshots:", len(snapshots))

            # add row for CSV (ONLY your fields)
            csv_rows.append({
                "AMI_ID": amiIds,
                "IMAGE_NAME": ImageName,
                "IMAGE_LOCATION": imageLocation,
                "SNAPSHOT_ID": snapshot_id
            })

# ======================
# EXPORT TO CSV
# ======================
csv_file = "ami_snapshot_report.csv"

with open(csv_file, "a", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "AMI_ID",
            "IMAGE_NAME",
            "IMAGE_LOCATION",
            "SNAPSHOT_ID"
        ]
    )
    writer.writeheader()
    writer.writerows(csv_rows)

print("\nCSV exported successfully:", csv_file)
