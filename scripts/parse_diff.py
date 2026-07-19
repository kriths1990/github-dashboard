import re

def parse_patch(filename, patch):

    changes = []

    if patch is None:
        return changes

    old_line = 0
    new_line = 0

    for line in patch.split("\n"):

        # Match @@ -10,3 +12,4 @@
        if line.startswith("@@"):

            match = re.search(r'-(\d+).*?\+(\d+)', line)

            if match:
                old_line = int(match.group(1))
                new_line = int(match.group(2))

            continue

        if line.startswith("-") and not line.startswith("---"):

            changes.append({
                "file": filename,
                "type": "Removed",
                "line": old_line,
                "content": line[1:]
            })

            old_line += 1

        elif line.startswith("+") and not line.startswith("+++"):

            changes.append({
                "file": filename,
                "type": "Added",
                "line": new_line,
                "content": line[1:]
            })

            new_line += 1

        else:

            old_line += 1
            new_line += 1

    return changes