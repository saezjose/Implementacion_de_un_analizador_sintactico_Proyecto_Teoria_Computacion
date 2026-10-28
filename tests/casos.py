# Casos de prueba para el analizador sintáctico LL(1) - SmartRule
# Tarea 5

CASOS = [
    # Casos válidos
    {
        "id": 1,
        "descripcion": "Regla simple con relacional",
        "entrada": "WHEN temperatura > 28 THEN encender;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 2,
        "descripcion": "Condición con AND",
        "entrada": "WHEN a > 1 AND b < 2 THEN accion1;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 3,
        "descripcion": "Condición con OR",
        "entrada": "WHEN a > 1 OR b < 2 THEN accion1;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 4,
        "descripcion": "Condición con NOT",
        "entrada": "WHEN NOT activo THEN apagar;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 5,
        "descripcion": "Regla con ELSE",
        "entrada": "WHEN x > 0 THEN encender ELSE apagar;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 6,
        "descripcion": "Múltiples acciones separadas por coma",
        "entrada": "WHEN x == 1 THEN a, b, c;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 7,
        "descripcion": "Acción con asignación",
        "entrada": "WHEN x > 0 THEN y = 5;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 8,
        "descripcion": "Acción con argumento",
        "entrada": "WHEN x > 0 THEN encender luces;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 9,
        "descripcion": "Acción sin argumento",
        "entrada": "WHEN x > 0 THEN reset;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 10,
        "descripcion": "Valores TRUE/FALSE",
        "entrada": "WHEN sistema == TRUE THEN iniciar;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 11,
        "descripcion": "Múltiples reglas",
        "entrada": "WHEN a > 1 THEN x;\nWHEN b < 2 THEN y;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    {
        "id": 12,
        "descripcion": "Condición sin operador relacional (factor solo)",
        "entrada": "WHEN activo THEN encender;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "valido"
    },
    # Casos inválidos 1-6
    {
        "id": 13,
        "descripcion": "Falta THEN",
        "entrada": "WHEN x > 1 encender;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 14,
        "descripcion": "Falta condición",
        "entrada": "WHEN THEN encender;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 15,
        "descripcion": "Falta punto y coma",
        "entrada": "WHEN x > 1 THEN encender\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 16,
        "descripcion": "Falta WHEN",
        "entrada": "x > 1 THEN encender;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 17,
        "descripcion": "Coma sobrante",
        "entrada": "WHEN x > 1 THEN a,, b;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 18,
        "descripcion": "Falta operando tras operador relacional",
        "entrada": "WHEN temperatura > THEN encender;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    # Casos inválidos 7-12
    {
        "id": 19,
        "descripcion": "Lista de acciones vacía",
        "entrada": "WHEN x > 1 THEN ;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 20,
        "descripcion": "Falta acción después de ELSE",
        "entrada": "WHEN x > 1 THEN a ELSE ;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 21,
        "descripcion": "Coma al final sin acción",
        "entrada": "WHEN x > 1 THEN a,;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 22,
        "descripcion": "Falta acción después de coma",
        "entrada": "WHEN x > 1 THEN ,a;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 23,
        "descripcion": "Falta valor tras IGUAL",
        "entrada": "WHEN x > 1 THEN y = ;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    {
        "id": 24,
        "descripcion": "Operador relacional mal formado o incompleto",
        "entrada": "WHEN x > = 1 THEN y;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "invalido"
    },
    # Casos límite
    {
        "id": 25,
        "descripcion": "Entrada vacía",
        "entrada": "",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "limite"
    },
    {
        "id": 26,
        "descripcion": "Solo espacios",
        "entrada": "   \n\t  \n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "limite"
    },
    {
        "id": 27,
        "descripcion": "Regla mínima con una sola acción",
        "entrada": "WHEN a > 1 THEN x;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "limite"
    },
    {
        "id": 28,
        "descripcion": "Múltiples punto y coma",
        "entrada": "WHEN a > 1 THEN x;;\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "limite"
    },
    {
        "id": 29,
        "descripcion": "Regla mal formada con doble WHEN",
        "entrada": "WHEN a > 1 THEN x; WHEN\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "limite"
    },
    {
        "id": 30,
        "descripcion": "Falta cierre tras múltiples reglas",
        "entrada": "WHEN a > 1 THEN x; WHEN b > 2 THEN y\n",
        "esperado": "RECHAZA",
        "observacion": "",
        "categoria": "limite"
    },
    {
        "id": 31,
        "descripcion": "Acción con ID ID asignación",
        "entrada": "WHEN x > 0 THEN encender luces = 100;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "limite"
    },
    {
        "id": 32,
        "descripcion": "Condición con NOT anidado",
        "entrada": "WHEN NOT NOT activo THEN encender;\n",
        "esperado": "ACEPTA",
        "observacion": "",
        "categoria": "limite"
    },
]
