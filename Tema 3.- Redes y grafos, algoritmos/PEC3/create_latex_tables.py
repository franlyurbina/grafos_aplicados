import os
import csv
import re

degree_path = "./tables/degree_distribution"
weighted_path = "./tables/weighted_degree"
output_file = "informe.tex"

def clean_id(value):
    return str(int(float(value)))

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def esc(text):
    return text.replace("_", r"\_")

def build_table(rows, common):
    lines = []
    lines.append(r"\begin{tabular}{r l r r}")
    lines.append(r"\hline")
    lines.append(r"Id & Label & Grado & \shortstack{Grado \\ con pesos} \\")
    lines.append(r"\hline")

    for row in rows:
        label = row["Label"]
        if label in common:
            label_tex = r"\textcolor{ForestGreen}{" + esc(label) + "}"
        else:
            label_tex = esc(label)

        lines.append(
            "{} & {} & {} & {:.4f} \\\\".format(
                clean_id(row["Id"]),
                label_tex,
                int(float(row["Grado"])),
                float(row["Grado con pesos"])
            )
        )

    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)

communities = {}

for file in os.listdir(degree_path):
    match = re.match(r"comunidad_(\d+)_top10_grado\.csv", file)
    if match:
        communities[match.group(1)] = {
            "degree": os.path.join(degree_path, file),
            "weighted": os.path.join(
                weighted_path,
                f"comunidad_{match.group(1)}_top10_pesos.csv"
            )
        }

with open(output_file, "w", encoding="utf-8") as out:

    # Documento LaTeX completo
    out.write(r"\documentclass{article}" + "\n")
    out.write(r"\usepackage[table]{xcolor}" + "\n")
    out.write(r"\definecolor{ForestGreen}{RGB}{34,139,34}" + "\n")
    out.write(r"\usepackage[margin=2cm]{geometry}" + "\n")
    out.write(r"\begin{document}" + "\n\n")

    for community in sorted(communities.keys(), key=int):

        degree_rows = read_csv(communities[community]["degree"])
        weighted_rows = read_csv(communities[community]["weighted"])

        degree_labels = {row["Label"] for row in degree_rows}
        weighted_labels = {row["Label"] for row in weighted_rows}
        common_labels = degree_labels.intersection(weighted_labels)

        out.write(r"\section*{Comunidad " + community + "}" + "\n\n")
        out.write(r"\noindent" + "\n")

        # Tabla izquierda
        out.write(r"\begin{minipage}[t]{0.48\textwidth}" + "\n")
        out.write(r"\centering" + "\n")
        out.write(build_table(degree_rows, common_labels) + "\n\n")
        out.write(r"\vspace{0.2cm}" + "\n")
        out.write(r"\textbf{Top 10 por Grado}" + "\n")
        out.write(r"\end{minipage}" + "\n")
        out.write(r"\hspace{0.5cm}" + "\n")

        # Tabla derecha
        out.write(r"\begin{minipage}[t]{0.48\textwidth}" + "\n")
        out.write(r"\centering" + "\n")
        out.write(build_table(weighted_rows, common_labels) + "\n\n")
        out.write(r"\vspace{0.2cm}" + "\n")
        out.write(r"\textbf{Top 10 por Grado con pesos}" + "\n")
        out.write(r"\end{minipage}" + "\n\n\n")

    out.write(r"\end{document}")

print("Archivo informe.tex generado correctamente.")
