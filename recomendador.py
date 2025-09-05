
FIBONACCI = [0, 1, 2, 3, 5, 8, 13, 21]

def redondear_fibonacci(valor):
    return min(FIBONACCI, key=lambda x: abs(x - valor))

def obtener_recomendacion(fib_valor):
    if fib_valor <= 8:
        return "✅ Historia aceptable."
    elif fib_valor < 13 and fib_valor > 8:
        return "⚠️ Considera dividir o refinar la historia."
    else:
        return "❌ División recomendada."
