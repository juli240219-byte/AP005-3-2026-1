#  SISTEMA DE INVENTARIO - Programación Aplicada

# --- TUPLA: información fija del sistema (categorías permitidas) ---
CATEGORIAS = ("Electrónica", "Ropa", "Alimentos", "Hogar", "Deportes", "Otro")

# --- LISTA: almacena todos los productos registrados ---
productos = []

def mostrar_bienvenida():
    print("=" * 50)
    print("   SISTEMA DE INVENTARIO - Bienvenido")
    print("=" * 50)
    print(f"Categorías disponibles: {', '.join(CATEGORIAS)}")
    print()


def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Agregar producto")
    print("2. Mostrar todos los productos")
    print("3. Buscar producto")
    print("4. Eliminar producto")
    print("5. Salir")
    print("----------------------")


def agregar_producto():
    print("\n[ Agregar producto ]")

    # Código (validación: no vacío y no duplicado)
    while True:
        codigo = input("Código del producto: ").strip()
        if not codigo:
            print("  ⚠ El código no puede estar vacío.")
        elif buscar_por_codigo(codigo) is not None:
            print("  ⚠ Ya existe un producto con ese código.")
        else:
            break

    nombre = input("Nombre del producto: ").strip()
    while not nombre:
        print("  ⚠ El nombre no puede estar vacío.")
        nombre = input("Nombre del producto: ").strip()

    # Precio (conversión float + validación)
    while True:
        try:
            precio = float(input("Precio ($): "))
            if precio < 0:
                print("  ⚠ El precio no puede ser negativo.")
            else:
                break
        except ValueError:
            print("  ⚠ Ingresa un número válido para el precio.")

    # Cantidad (conversión int + validación)
    while True:
        try:
            cantidad = int(input("Cantidad en stock: "))
            if cantidad < 0:
                print("  ⚠ La cantidad no puede ser negativa.")
            else:
                break
        except ValueError:
            print("  ⚠ Ingresa un número entero para la cantidad.")

    # Categoría (validación contra la tupla)
    print(f"Categorías: {', '.join(CATEGORIAS)}")
    while True:
        categoria = input("Categoría: ").strip().capitalize()
        if categoria in CATEGORIAS:
            break
        else:
            print(f"  ⚠ Categoría inválida. Elige una de: {', '.join(CATEGORIAS)}")

    # --- DICCIONARIO: representa cada producto ---
    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad,
        "categoria": categoria
    }

    productos.append(producto)
    print(f"  ✓ Producto '{nombre}' agregado correctamente.")


def mostrar_productos():
    print("\n[ Todos los productos ]")
    if not productos:
        print("  No hay productos registrados.")
        return

    print(f"{'Código':<10} {'Nombre':<20} {'Precio':>10} {'Cantidad':>10} {'Categoría':<15}")
    print("-" * 68)

    # --- CICLO FOR: recorre la lista de productos ---
    for p in productos:
        print(f"{p['codigo']:<10} {p['nombre']:<20} ${p['precio']:>9.2f} {p['cantidad']:>10} {p['categoria']:<15}")

    print(f"\nTotal de productos registrados: {len(productos)}")


def buscar_por_codigo(codigo):
    """Retorna el producto si lo encuentra, o None si no existe."""
    for p in productos:
        if p["codigo"].lower() == codigo.lower():
            return p
    return None


def buscar_producto():
    print("\n[ Buscar producto ]")
    codigo = input("Ingresa el código a buscar: ").strip()

    producto = buscar_por_codigo(codigo)
    if producto:
        print("\nProducto encontrado:")
        print(f"  Código    : {producto['codigo']}")
        print(f"  Nombre    : {producto['nombre']}")
        print(f"  Precio    : ${producto['precio']:.2f}")
        print(f"  Cantidad  : {producto['cantidad']}")
        print(f"  Categoría : {producto['categoria']}")
    else:
        print(f"  ⚠ No se encontró ningún producto con código '{codigo}'.")


def eliminar_producto():
    print("\n[ Eliminar producto ]")
    codigo = input("Ingresa el código del producto a eliminar: ").strip()

    producto = buscar_por_codigo(codigo)

    if producto:
        confirmacion = input(f"  ¿Seguro que deseas eliminar '{producto['nombre']}'? (s/n): ").strip().lower()
        if confirmacion == "s":
            productos.remove(producto)
            print(f"  ✓ Producto '{producto['nombre']}' eliminado correctamente.")
        else:
            print("  Eliminación cancelada.")
    else:
        print(f"  ⚠ No se encontró ningún producto con código '{codigo}'.")

#  PROGRAMA PRINCIPAL

mostrar_bienvenida()

# --- CICLO WHILE: mantiene el menú en ejecución ---
while True:
    mostrar_menu()
    opcion = input("Elige una opción (1-5): ").strip()

    # --- CONDICIONALES: if / elif / else ---
    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        mostrar_productos()
    elif opcion == "3":
        buscar_producto()
    elif opcion == "4":
        eliminar_producto()
    elif opcion == "5":
        print("\n¡Hasta luego! Cerrando el sistema de inventario.")
        break
    else:
        print("  ⚠ Opción inválida. Por favor elige un número del 1 al 5.")
