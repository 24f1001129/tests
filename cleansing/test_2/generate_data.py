# Generate messy_text.txt with many lines and one REF-100001 occurrence
from pathlib import Path

out = Path.cwd()

lines = []
for i in range(50000):
    lines.append(f"line {i} random data {i*i%997}\n")

# Insert the unique reference near the middle
lines[25000] = "2025-01-01 INFO REF-100001 transaction completed\n"

(out / "messy_text.txt").write_text("".join(lines))
print("messy_text.txt generated. Expected REF code: REF-100001")



