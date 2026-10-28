# Analizador Sintáctico LL(1) para el DSL "SmartRule"

Proyecto de Teoría de la Computación (INFO1148) - Analizador léxico y sintáctico LL(1) descendente recursivo, con AST y manejo de errores.

## 1. Descripción del lenguaje

**SmartRule** es un lenguaje de dominio específico (DSL) para definir reglas de automatización en sistemas IoT y domótica.

- Reglas: `WHEN <condición> THEN <acciones> [ELSE <acciones>];`
- Operadores relacionales: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Operadores lógicos: `AND`, `OR`, `NOT` (precedencia: `NOT` > `AND` > `OR`)
- Acciones: asignación `variable = valor`, llamada `accion [argumento]` y asignación con objeto `accion objeto = valor`
- Valores: números enteros, identificadores, `TRUE` y `FALSE`
- Varias acciones separadas por coma y varias reglas por archivo
- Cualquier otro símbolo (por ejemplo `#`, `@`, `(`, `)`) produce un error léxico

### Ejemplos válidos
```
WHEN temperatura > 28 AND humedad < 40 THEN encender ventilador;
WHEN luz == 0 OR movimiento == TRUE THEN encender luces, alarma = 1 ELSE apagar luces;
WHEN NOT puerta_abierta THEN activar_alarma;
WHEN humedad <= 30 THEN encender riego = 100;
```

### Ejemplos inválidos
```
WHEN temperatura > THEN encender ventilador;   # falta operando
temperatura > 28 THEN encender luces;          # falta WHEN
WHEN temperatura > 28 encender luces;          # falta THEN
WHEN temperatura > 28 THEN ;                   # lista de acciones vacía
```

## 2. Arquitectura

```
src/
├── gramatica.py   # Gramática (fuente única de verdad)
├── lexer/         # Analizador léxico
├── ast/           # Nodos del AST
├── parser/        # Parser LL(1) descendente recursivo
└── utils/         # FIRST/FOLLOW/tabla LL(1), generación de tablas y grafo del AST
tests/             # Suite de pruebas (68)
ejemplos/          # Archivos .sr válidos, inválidos y límite
docs/              # Gramática, tabla de casos e informe LaTeX
main.py            # CLI
```

## 3. Gramática (LL(1), 33 producciones)

```
Prog          -> Regla Prog | ε
Regla         -> WHEN Cond THEN ListaAcciones ElsePart PUNTO_COMA
ElsePart      -> ELSE ListaAcciones | ε
Cond          -> OrExpr
OrExpr        -> AndExpr OrTail
OrTail        -> OR AndExpr OrTail | ε
AndExpr       -> NotExpr AndTail
AndTail       -> AND NotExpr AndTail | ε
NotExpr       -> NOT NotExpr | RelExpr
RelExpr       -> Factor RelExprTail
RelExprTail   -> OP_REL Factor | ε
Factor        -> NUM | ID | TRUE | FALSE
ListaAcciones -> Accion AccionTail
AccionTail    -> COMA Accion AccionTail | ε
Accion        -> ID AsigOrCall
AsigOrCall    -> IGUAL Factor | ID AsigTail | NUM | TRUE | FALSE | ε
AsigTail      -> IGUAL Factor | ε
```

`IGUAL` es `=`. `AsigOrCall` y `AsigTail` resultan de factorizar por la izquierda el prefijo común `ID` de las acciones. Detalles, FIRST, FOLLOW y tabla LL(1) en `docs/gramatica.md`.

## 4. Requisitos

- Python 3.10 o superior
- Sin dependencias externas (solo librería estándar; `pytest` es opcional)

## 5. Ejecución

```bash
python main.py                              # modo interactivo
python main.py -f ejemplos/validos_1.sr     # analizar un archivo
python main.py -f ejemplos/validos_1.sr -t -a   # con tokens (-t) y AST (-a)
python -m src.utils.first_follow            # FIRST, FOLLOW y tabla LL(1)
python -m unittest discover -s tests -v     # pruebas (68)
python -m pytest tests -v                   # alternativa, si tiene pytest
```

Formato de los errores:
```
Error léxico (línea 1, columna 8): símbolo no reconocido '#'
Error sintáctico (token 4, línea 1, columna 20): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró 'THEN'
```

## 6. Archivos importantes

- `main.py`: punto de entrada
- `docs/gramatica.md`: gramática, FIRST, FOLLOW, tabla LL(1) y análisis
- `docs/tabla_casos.md`: casos de prueba documentados
- `docs/informe_latex/`: informe en LaTeX
- `tests/`: suite de 68 pruebas (incluye los 25 casos del informe: V1-V10, I1-I10, L1-L5)

## 7. Autoría y aclaraciones

- Integrantes: José Sáez (jefe de grupo), Catalina Vergara, Alexa Galeano.
- El lexer parte del cuaderno `anlizador_lexico1.ipynb` entregado por el docente, adaptado y extendido.
- El parser está implementado desde cero (sin ANTLR, Yacc, Bison ni PLY), con un solo token de anticipación y sin retroceso.
- El AST se construye explícitamente.
- Uso de IA: ver la declaración incluida en el informe.
