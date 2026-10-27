#!/usr/bin/env python3
"""
Punto de entrada principal - Analizador Sintáctico SmartRule
"""

import sys
import argparse
from src.lexer.lexer import analizador_lexico, LexerError
from src.parser.parser_ll1 import ParserLL1, ParserError
from src.utils.grafo import mostrar_ast_simple


def analizar(entrada, mostrar_tokens=False, mostrar_ast=False):
    print("=" * 60)
    print("ANALIZADOR SINTACTICO SMART RULE (LL(1))")
    print("=" * 60)
    print(f"\nEntrada:\n{entrada}\n")
    
    try:
        # Análisis léxico
        tokens = analizador_lexico(entrada)
        if mostrar_tokens:
            print("TOKENS:")
            for i, token in enumerate(tokens):
                print(f"  {i}: {token}")
            print()
        
        # Análisis sintáctico
        parser = ParserLL1(tokens)
        ast = parser.parse()
        
        print("[OK] ANALISIS LEXICO EXITOSO")
        print("[OK] ANALISIS SINTACTICO EXITOSO")
        print(f"\nSe reconocieron {len(ast.reglas)} regla(s) valida(s).")
        
        if mostrar_ast:
            print("\n" + "=" * 60)
            print("ARBOL SINTACTICO ABSTRACTO (AST)")
            print("=" * 60)
            print()
            mostrar_ast_simple(ast)
            print()
        
        return True, ast
        
    except LexerError as e:
        print(f"[ERROR] ERROR LEXICO: {e}")
        return False, None
    except ParserError as e:
        print(f"[ERROR] ERROR SINTACTICO: {e}")
        return False, None
    except Exception as e:
        print(f"[ERROR] ERROR INESPERADO: {e}")
        return False, None


def modo_interactivo():
    print("=" * 60)
    print("MODO INTERACTIVO - SMART RULE")
    print("=" * 60)
    print("Ingrese reglas (una por línea). Escriba 'salir' para terminar.")
    print("Escriba 'tokens' para activar/desactivar visualización de tokens.")
    print("Escriba 'ast' para activar/desactivar visualización de AST.")
    print("=" * 60)
    
    mostrar_tokens = False
    mostrar_ast = True
    
    while True:
        try:
            entrada = input("\n> ").strip()
            if not entrada:
                continue
            # Limpiar '>' iniciales si vienen por copy-paste
            while entrada.startswith('>'):
                entrada = entrada[1:].strip()
            if entrada.lower() == 'salir':
                break
            if entrada.lower() == 'tokens':
                mostrar_tokens = not mostrar_tokens
                print(f"Visualización de tokens: {'ACTIVADA' if mostrar_tokens else 'DESACTIVADA'}")
                continue
            if entrada.lower() == 'ast':
                mostrar_ast = not mostrar_ast
                print(f"Visualización de AST: {'ACTIVADA' if mostrar_ast else 'DESACTIVADA'}")
                continue
            
            analizar(entrada, mostrar_tokens, mostrar_ast)
            
        except EOFError:
            break
        except KeyboardInterrupt:
            break
    
    print("\n¡Hasta luego!")


def main():
    parser = argparse.ArgumentParser(
        description='Analizador Sintáctico LL(1) para DSL SmartRule',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-f', '--archivo', help='Archivo con reglas SmartRule')
    parser.add_argument('-t', '--tokens', action='store_true', help='Mostrar tokens')
    parser.add_argument('-a', '--ast', action='store_true', help='Mostrar AST')
    parser.add_argument('-i', '--interactivo', action='store_true', help='Modo interactivo')
    
    args = parser.parse_args()
    
    if args.interactivo or not any([args.archivo]):
        if args.archivo and not args.interactivo:
            # Intentar leer archivo
            try:
                with open(args.archivo, 'r', encoding='utf-8') as f:
                    entrada = f.read()
                analizar(entrada, args.tokens, args.ast or True)
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo {args.archivo}")
                sys.exit(1)
        else:
            modo_interactivo()
    else:
        try:
            with open(args.archivo, 'r', encoding='utf-8') as f:
                entrada = f.read()
            analizar(entrada, args.tokens, args.ast or True)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {args.archivo}")
            sys.exit(1)


if __name__ == '__main__':
    main()
