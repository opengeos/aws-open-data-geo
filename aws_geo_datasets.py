import json
import os
import shutil
import yaml
import leafmap
import pandas as pd

url = "https://github.com/awslabs/open-data-registry/archive/refs/heads/main.zip"
out_dir = "open-data-registry-main"
zip_file = "open-data-registry-main.zip"
max_chars = 80  # The maximum number of characters in each column

if os.path.exists(out_dir):
    shutil.rmtree(out_dir)

if os.path.exists(zip_file):
    os.remove(zip_file)

leafmap.download_file(url, output=zip_file, unzip=True)


in_dir = os.path.join(out_dir, "datasets")

files = leafmap.find_files(in_dir, ext=".yaml")

print(f"Total number of AWS open datasets: {len(files)}")

datasets = []
names = {}

geo_tags = [
    "gis",
    "earth observation",
    "events",
    "mapping",
    "meteorological",
    "environmental",
    "transportation",
    "geospatial",
    "satellite imagery",
]

for file in files:
    dataset = {}
    with open(file, "r") as f:
        dataset = yaml.safe_load(f)

        if "Deprecated" in dataset:
            continue

        tags = dataset.get("Tags", [])
        name = dataset.get("Name", "")

        if bool(set(geo_tags) & set(tags)):

            basename = os.path.basename(file)
            out_file = os.path.join("datasets", basename)

            shutil.copy(file, out_file)

            resources = dataset.get("Resources", [])
            names[name] = len(resources)

            for resource in resources:

                before_href = resource["Description"].split("](")[0].replace("[", "")
                if len(resource["Description"].split("](")) > 1:
                    after_href = resource["Description"].split("](")[1].split(")")[1]
                else:  # No hyperlink
                    after_href = ""

                resource["Description"] = (
                    f"{before_href}{after_href}"[:max_chars]
                    .replace("\n", "")
                    .replace(".", "")
                    .replace("or [SQS", "")
                    .replace("(ORC", "")
                    .replace("[", "")
                    .replace("(2007-2014", "(2007-2014)")
                    .replace("(2007-2013", "(2007-2013)")
                    .strip()
                )

                item = {}

                if names[name] > 1:
                    item["Name"] = f"{name} - {resource['Description']}"
                else:
                    item["Name"] = name

                for key in resource:
                    item[key] = resource[key]

                item["Documentation"] = (
                    dataset["Documentation"]
                    .replace("<br/>", "")
                    .replace("\n", "")[:max_chars]
                )
                item["Contact"] = (
                    dataset["Contact"]
                    .replace("<br/>", "")
                    .replace("\n", "")[:max_chars]
                )
                item["ManagedBy"] = dataset["ManagedBy"][:max_chars]
                item["UpdateFrequency"] = dataset["UpdateFrequency"][:max_chars]
                item["License"] = dataset["License"].replace("\n", "")[:max_chars]
                item["Tags"] = ", ".join(dataset["Tags"])

                datasets.append(item)


print(f"Total number of geospatial datasets: {len(datasets)}")

df = pd.DataFrame(datasets)
df = df.sort_values(by="Name")
df.to_csv("aws_geo_datasets.tsv", index=False, sep="\t")

data = json.loads(df.to_json(orient="records"))

with open("aws_geo_datasets.json", "w") as f:
    json.dump(data, f, indent=4)
