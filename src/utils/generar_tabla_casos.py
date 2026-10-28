import csv
import os
from src.lexer.lexer import analizador_lexico, LexerError
from src.parser.parser_ll1 import ParserLL1, ParserError
from tests.casos import CASOS


def escape_latex(text):
    if text is None:
        return ""
    text = str(text)
    # Escapar caracteres especiales de LaTeX
    replacements = [
        ('\\', '\\textbackslash{}'),
        ('_', '\\_'),
        ('%', '\\%'),
        ('&', '\\&'),
        ('$', '\\$'),
        ('#', '\\#'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('^', '\\^{}'),
        ('~', '\\~{}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def generar_tabla_casos(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                    'docs', 'tabla_casos.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    resultados = []
    discrepancias = []
    
    for caso in CASOS:
        entrada = caso["entrada"]
        esperado = caso["esperado"]
        observacion = caso.get("observacion", "")
        error_msg = ""
        try:
            tokens = analizador_lexico(entrada)
            parser = ParserLL1(tokens)
            ast = parser.parse(modo_panic=False)
            obtenido = "ACEPTA"
        except LexerError as e:
            obtenido = "RECHAZA"
            error_msg = str(e)
            if not observacion:
                observacion = error_msg
        except ParserError as e:
            obtenido = "RECHAZA"
            error_msg = str(e)
            if not observacion:
                observacion = error_msg
        except Exception as e:
            obtenido = "RECHAZA"
            error_msg = str(e)
            if not observacion:
                observacion = error_msg
        
        if obtenido != esperado:
            discrepancias.append({
                "id": caso["id"],
                "descripcion": caso["descripcion"],
                "esperado": esperado,
                "obtenido": obtenido,
                "entrada": entrada.strip(),
                "error": error_msg
            })
        
        # Para inválidos, incluir mensaje con línea y columna en Resultado obtenido si hay error
        if obtenido == "RECHAZA" and error_msg:
            resultado_obtenido = f"RECHAZA: {error_msg}"
        else:
            resultado_obtenido = obtenido
        
        resultados.append({
            "ID": caso["id"],
            "Descripción": caso["descripcion"],
            "Entrada": entrada.strip().replace("\n", " "),
            "Resultado esperado": esperado,
            "Resultado obtenido": resultado_obtenido,
            "Observación": observacion
        })
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Descripción", "Entrada", "Resultado esperado", "Resultado obtenido", "Observación"])
        writer.writeheader()
        for r in resultados:
            writer.writerow(r)
    
    # Generar Markdown
    md_path = os.path.join(os.path.dirname(output_path), 'tabla_casos.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Tabla de Casos de Prueba - SmartRule\n\n")
        f.write("| ID | Descripción | Entrada | Resultado esperado | Resultado obtenido | Observación |\n")
        f.write("|---|-------------|---------|-------------------|-------------------|-------------|\n")
        for r in resultados:
            entrada_md = r["Entrada"].replace("|", "\\|")
            obs_md = r["Observación"].replace("|", "\\|")
            res_obs_md = r["Resultado obtenido"].replace("|", "\\|")
            f.write(f"| {r['ID']} | {r['Descripción']} | `{entrada_md}` | {r['Resultado esperado']} | {res_obs_md} | {obs_md} |\n")
    
    # Generar LaTeX
    tex_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                            'docs', 'informe_latex', 'tabla_casos.tex')
    os.makedirs(os.path.dirname(tex_path), exist_ok=True)
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write("\\begin{longtable}{|p{6cm}|p{2cm}|p{5cm}|p{6cm}|}\n")
        f.write("\\hline\n")
        f.write("\\textbf{Entrada} & \\textbf{Resultado esperado} & \\textbf{Resultado obtenido} & \\textbf{Observación} \\\\\n")
        f.write("\\hline\n")
        f.write("\\endfirsthead\n")
        f.write("\\hline\n")
        f.write("\\textbf{Entrada} & \\textbf{Resultado esperado} & \\textbf{Resultado obtenido} & \\textbf{Observación} \\\\\n")
        f.write("\\hline\n")
        f.write("\\endhead\n")
        f.write("\\hline\n")
        f.write("\\endfoot\n")
        for r in resultados:
            entrada_tex = escape_latex(r["Entrada"])
            esp_tex = escape_latex(r["Resultado esperado"])
            obt_tex = escape_latex(r["Resultado obtenido"])
            obs_tex = escape_latex(r["Observación"])
            f.write(f"\\texttt{{{entrada_tex}}} & {esp_tex} & \\texttt{{{obt_tex}}} & {obs_tex} \\\\\n")
            f.write("\\hline\n")
        f.write("\\caption{Casos de prueba del analizador sintáctico LL(1)}\n")
        f.write("\\label{tab:casos}\n")
        f.write("\\end{longtable}\n")
    
    print(f"Tabla generada en: {output_path}")
    print(f"Markdown generado en: {md_path}")
    print(f"LaTeX generado en: {tex_path}")
    if discrepancias:
        print("\n=== DISCREPANCIAS ===")
        for d in discrepancias:
            print(f"Caso {d['id']}: {d['descripcion']} - Esperado {d['esperado']}, Obtenido {d['obtenido']}")
            print(f"  Entrada: {d['entrada']}")
            print(f"  Error: {d['error']}")
        print(f"\nTotal discrepancias: {len(discrepancias)}")
    else:
        print("\nSin discrepancias encontradas.")
    
    return resultados, discrepancias


if __name__ == '__main__':
    generar_tabla_casos()
