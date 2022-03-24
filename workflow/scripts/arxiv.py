import tarfile


# Snakemake config (available automagically)
config = snakemake.config  # type:ignore
if config["showyourwork_path"]:
    sys.path.insert(1, config["showyourwork_path"])


# Import showyourwork
from showyourwork import paths


# Hack to run the `pdf.py` script
script = __file__.replace("arxiv.py", "pdf.py")
with open(script, "r") as f:
    script = f.read()
exec(script)


# File names to exclude
ms_name = snakemake.config["ms_name"]
exclude = [
    ".gitignore",
    f"{ms_name}.pdf",
    f"{ms_name}.aux",
    f"{ms_name}.blg",
    f"{ms_name}.log",
    f"{ms_name}.out",
]


# Tar up everything in the src/tex directory
with tarfile.open("arxiv.tar.gz", "w:gz") as tarball:
    for file in paths.user().tex.rglob("*"):
        if not file.is_dir() and not file.name in exclude:
            tarball.add(file, arcname=file.relative_to(paths.user().tex))
    for file in paths.user().compile.rglob("*"):
        if file.name not in exclude:
            tarball.add(file, arcname=file.name)
