FeatureScript 3112;
import(path : "onshape/std/geometry.fs", version : "3112.0");

/*
  FoodScan - Equipo 10 - Fundamentos de Diseño (UPCH)
  Prototipo Concepto C, Revisión 3 (10/11/2026)

  Modelo nuevo: se carga en un documento de Onshape aparte y no reemplaza ni
  modifica la revisión 2 (FoodScan_Onshape_v2.fs).

  Operación "FoodScan - Prototipo Concepto C v3": crea en mm todas las piezas del
  prototipo, cada una con nombre, color y material (Part Studio multiparte).

  Cambios respecto a la revisión 2:
    - Alto exterior 415 -> 380 mm: compartimento electrónico de 48 -> 32 mm,
      separadores de la celda de 8 -> 5 mm y plato encuadrado con 5 mm de margen
      (ángulo de la Waveshare OV5640 (C): 67,4° en diagonal, 43,6° en el lado corto).
    - Los tres paneles de 12 LED se sustituyen por 4 tiras COB 5 V de 200 mm,
      verticales en las esquinas, dentro de perfiles esquineros de aluminio con
      difusor opal. En las esquinas no aparecen en la foto y su reflejo cae fuera
      del plato.
    - Borneras X1-X5, canaletas, pasacables, cables y parasol del lente.
    - HX711 trasladado a la esquina trasera izquierda, fuera de la bandeja.
    - Conectores de ensamble (mate connectors) para colocar modelos STEP de los
      componentes comerciales, y opción para ocultar la electrónica simplificada.

  Ejes: X = ancho, Y = fondo (frente en y = 0, la puerta mira a -Y),
        Z = altura (piso en z = 0).
  Cada pieza es una tabla de sólidos:
    [x0, y0, z0, x1, y1, z1]          caja entre dos esquinas
    [ax, ay, az, bx, by, bz, r]       cilindro del centro A al centro B
    [x, y, z, r]                      esfera
    [z0, z1, [[x, y], [x, y], ...]]   prisma vertical de base poligonal
  Los "cortes" se restan de la pieza (agujeros, vanos, ranuras).
*/


// Crea una primitiva según el largo de d (ver el encabezado).
function primitiva(context is Context, id is Id, d is array)
{
    if (size(d) == 6)
    {
        fCuboid(context, id, {
                    "corner1" : vector(min(d[0], d[3]), min(d[1], d[4]), min(d[2], d[5])) * millimeter,
                    "corner2" : vector(max(d[0], d[3]), max(d[1], d[4]), max(d[2], d[5])) * millimeter
                });
    }
    else if (size(d) == 7)
    {
        fCylinder(context, id, {
                    "bottomCenter" : vector(d[0], d[1], d[2]) * millimeter,
                    "topCenter" : vector(d[3], d[4], d[5]) * millimeter,
                    "radius" : d[6] * millimeter
                });
    }
    else if (size(d) == 4)
    {
        opSphere(context, id, {
                    "center" : vector(d[0], d[1], d[2]) * millimeter,
                    "radius" : d[3] * millimeter
                });
    }
    else
    {
        // Prisma: contorno cerrado en el plano z = d[0], extruido hasta z = d[1].
        var puntos = [];
        for (var k = 0; k < size(d[2]); k += 1)
        {
            puntos = append(puntos, vector(d[2][k][0], d[2][k][1]) * millimeter);
        }
        puntos = append(puntos, puntos[0]);
        const boceto = newSketchOnPlane(context, id + "boceto", {
                    "sketchPlane" : plane(vector(0, 0, d[0]) * millimeter, vector(0, 0, 1), vector(1, 0, 0))
                });
        skPolyline(boceto, "contorno", { "points" : puntos });
        skSolve(boceto);
        opExtrude(context, id + "extruir", {
                    "entities" : qSketchRegion(id + "boceto"),
                    "direction" : vector(0, 0, 1),
                    "endBound" : BoundingType.BLIND,
                    "endDepth" : (d[1] - d[0]) * millimeter
                });
        opDeleteBodies(context, id + "borrarBoceto", {
                    "entities" : qCreatedBy(id + "boceto", EntityType.BODY)
                });
    }
}

// Crea los sólidos de una pieza (sin terminarla).
function solidos(context is Context, p is Id, lista is array)
{
    for (var i = 0; i < size(lista); i += 1)
    {
        primitiva(context, p + "s" + ("b" ~ toString(i)), lista[i]);
    }
}

// Crea una pieza completa: sus sólidos (bajo p) y luego la termina.
function pieza(context is Context, p is Id, nombre is string, rgb is array, mat is string,
               densidad is number, lista is array, cortes is array)
{
    solidos(context, p, lista);
    terminar(context, p, p, nombre, rgb, mat, densidad, cortes);
}

// Termina una pieza cuyos sólidos se crearon bajo "base": resta los cortes, une los
// sólidos en un solo cuerpo y asigna nombre, color y material.
function terminar(context is Context, p is Id, base is Id, nombre is string, rgb is array,
                  mat is string, densidad is number, cortes is array)
{
    for (var i = 0; i < size(cortes); i += 1)
    {
        primitiva(context, p + "c" + ("c" ~ toString(i)), cortes[i]);
    }
    if (size(cortes) > 0)
    {
        opBoolean(context, p + "resta", {
                    "tools" : qCreatedBy(p + "c", EntityType.BODY),
                    "targets" : qCreatedBy(base + "s", EntityType.BODY),
                    "operationType" : BooleanOperationType.SUBTRACTION
                });
    }
    const cuerpos = qCreatedBy(base + "s", EntityType.BODY);
    if (size(evaluateQuery(context, cuerpos)) > 1)
    {
        opBoolean(context, p + "union", {
                    "tools" : cuerpos,
                    "operationType" : BooleanOperationType.UNION
                });
    }
    setProperty(context, { "entities" : cuerpos, "propertyType" : PropertyType.NAME, "value" : nombre });
    setProperty(context, { "entities" : cuerpos, "propertyType" : PropertyType.APPEARANCE,
                "value" : color(rgb[0], rgb[1], rgb[2]) });
    setProperty(context, { "entities" : cuerpos, "propertyType" : PropertyType.MATERIAL,
                "value" : material(mat, densidad * gram / centimeter ^ 3) });
}

// Cantidad impar de dedos para un borde de largo L con dedos de ancho f.
function nImpar(L is number, f is number) returns number
{
    var n = floor(L / f);
    if (n % 2 == 0)
    {
        n = n - 1;
    }
    return max(n, 3);
}

// Tramo k (de n) de una arista: caja de la zona donde se cruzan dos tableros.
function segmento(eje is string, L0 is number, L1 is number, a0 is number, a1 is number,
                  b0 is number, b1 is number, n is number, k is number) returns array
{
    const s0 = L0 + (L1 - L0) * k / n;
    const s1 = L0 + (L1 - L0) * (k + 1) / n;
    if (eje == "X")
    {
        return [s0, a0, b0, s1, a1, b1];
    }
    if (eje == "Y")
    {
        return [a0, s0, b0, a1, s1, b1];
    }
    return [a0, b0, s0, a1, b1, s1];
}

// Unión de dedos en una arista: el borde va de L0 a L1 sobre el eje indicado y
// (a0, a1), (b0, b1) son los otros dos rangos. Los tramos pares (incluidos los
// extremos) quedan en el tablero "dueno" y los impares en el tablero "otro".
function junta(context is Context, id is Id, eje is string, L0 is number, L1 is number,
               a0 is number, a1 is number, b0 is number, b1 is number, n is number,
               dueno is Id, otro is Id)
{
    for (var k = 0; k < n; k += 2)
    {
        primitiva(context, id + "par" + ("k" ~ toString(k)), segmento(eje, L0, L1, a0, a1, b0, b1, n, k));
    }
    for (var k = 1; k < n; k += 2)
    {
        primitiva(context, id + "impar" + ("k" ~ toString(k)), segmento(eje, L0, L1, a0, a1, b0, b1, n, k));
    }
    opBoolean(context, id + "cortaOtro", {
                "tools" : qCreatedBy(id + "par", EntityType.BODY),
                "targets" : qCreatedBy(otro + "s", EntityType.BODY),
                "operationType" : BooleanOperationType.SUBTRACTION
            });
    opBoolean(context, id + "cortaDueno", {
                "tools" : qCreatedBy(id + "impar", EntityType.BODY),
                "targets" : qCreatedBy(dueno + "s", EntityType.BODY),
                "operationType" : BooleanOperationType.SUBTRACTION
            });
}

// Lleva puntos locales [u, v] de una esquina interior a coordenadas [x, y]:
// u se mide desde la pared lateral y v desde la pared frontal o trasera.
function enEsquina(pts is array, cx is number, cy is number, sx is number, sy is number) returns array
{
    var r = [];
    for (var k = 0; k < size(pts); k += 1)
    {
        r = append(r, [cx + sx * pts[k][0], cy + sy * pts[k][1]]);
    }
    return r;
}

// Bornera de n polos, paso 5,08 mm, alineada con Y: cuerpo de 7,5 x 5,08n x 10 mm
// con las cabezas de los tornillos arriba.
function borneraY(x0 is number, y0 is number, z0 is number, n is number) returns array
{
    var l = [[x0, y0, z0, x0 + 7.5, y0 + 5.08 * n, z0 + 10]];
    for (var k = 0; k < n; k += 1)
    {
        const yk = y0 + 5.08 * (k + 0.5);
        l = append(l, [x0 + 3.75, yk, z0 + 10, x0 + 3.75, yk, z0 + 10.8, 1.5]);
    }
    return l;
}

// Igual que borneraY, pero alineada con X.
function borneraX(x0 is number, y0 is number, z0 is number, n is number) returns array
{
    var l = [[x0, y0, z0, x0 + 5.08 * n, y0 + 7.5, z0 + 10]];
    for (var k = 0; k < n; k += 1)
    {
        const xk = x0 + 5.08 * (k + 0.5);
        l = append(l, [xk, y0 + 3.75, z0 + 10, xk, y0 + 3.75, z0 + 10.8, 1.5]);
    }
    return l;
}

// Cable de radio r que pasa por los puntos [x, y, z]: cilindros entre puntos y
// esferas en los quiebres.
function cable(pts is array, r is number) returns array
{
    var l = [];
    for (var k = 0; k + 1 < size(pts); k += 1)
    {
        l = append(l, [pts[k][0], pts[k][1], pts[k][2], pts[k + 1][0], pts[k + 1][1], pts[k + 1][2], r]);
        if (k > 0)
        {
            l = append(l, [pts[k][0], pts[k][1], pts[k][2], r]);
        }
    }
    return l;
}

// Conector de ensamble en el punto o (mm), con ejes X y Z dados, que pertenece a la
// pieza creada bajo "dueno". Sirve para colocar los modelos STEP comerciales.
function conector(context is Context, id is Id, dueno is Id, o is array, ejeX is array, ejeZ is array)
{
    opMateConnector(context, id, {
                "coordSystem" : coordSystem(vector(o[0], o[1], o[2]) * millimeter,
                        vector(ejeX[0], ejeX[1], ejeX[2]), vector(ejeZ[0], ejeZ[1], ejeZ[2])),
                "owner" : qCreatedBy(dueno + "s", EntityType.BODY)
            });
}

annotation { "Feature Type Name" : "FoodScan - Prototipo Concepto C v3" }
export const foodScanPrototipoV3 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Ancho exterior W (eje X)" }
        isLength(definition.ancho, { (millimeter) : [280, 310, 600] } as LengthBoundSpec);
        annotation { "Name" : "Fondo exterior D (eje Y, sin puerta)" }
        isLength(definition.fondo, { (millimeter) : [260, 300, 600] } as LengthBoundSpec);
        annotation { "Name" : "Alto exterior H (eje Z, sin patas)" }
        isLength(definition.alto, { (millimeter) : [330, 380, 800] } as LengthBoundSpec);
        annotation { "Name" : "Espesor del MDF" }
        isLength(definition.esp, { (millimeter) : [2.5, 3.5, 6] } as LengthBoundSpec);
        annotation { "Name" : "Ancho de dedo de las uniones" }
        isLength(definition.dedo, { (millimeter) : [8, 20, 60] } as LengthBoundSpec);
        annotation { "Name" : "Diametro del plato de referencia" }
        isLength(definition.dPlato, { (millimeter) : [150, 220, 250] } as LengthBoundSpec);
        annotation { "Name" : "Mostrar la puerta abierta", "Default" : false }
        definition.puertaAbierta is boolean;
        annotation { "Name" : "Mostrar electronica simplificada", "Default" : true }
        definition.electronica is boolean;
    }
    {
        const ancho = definition.ancho / millimeter;
        const fondo = definition.fondo / millimeter;
        const alto = definition.alto / millimeter;
        const esp = definition.esp / millimeter;
        const dedo = definition.dedo / millimeter;
        const dPlato = definition.dPlato / millimeter;
        const xi = ancho / 2 - esp; // cara interior de los laterales (x = +-xi)
        const yi0 = esp; // cara interior del panel frontal
        const yi1 = fondo - esp; // cara interior del panel trasero
        const zi0 = esp; // cara superior del piso
        const zi1 = alto - esp; // cara inferior de la tapa
        const hElec = 32; // altura libre del compartimento electronico (v2: 48)
        const zRep = zi1 - hElec - esp; // cara inferior de la repisa de camara
        const zRepS = zRep + esp; // cara superior de la repisa de camara
        const yc = fondo / 2; // eje comun de bandeja, plato y camara
        const hSep = 5; // altura de los separadores de la celda (v2: 8)
        const zLC0 = zi0 + hSep; // cara inferior de la celda de carga
        const zLC1 = zLC0 + 12.7; // cara superior de la celda de carga
        const zHub0 = zLC1 + hSep; // base del soporte de bandeja
        const zPl0 = zHub0 + 5; // cara inferior de la bandeja
        const zPl1 = zPl0 + esp; // cara superior de la bandeja
        const zPlato1 = zPl1 + 20; // borde superior del plato
        const zFondoPlato = zPl1 + 3; // fondo interior del plato
        const rPlat = dPlato / 2 + 15; // radio de la bandeja
        const xLC1 = 12.5; // extremo libre de la celda (bajo el centro de la bandeja)
        const xLC0 = xLC1 - 80; // extremo fijo de la celda (salida del cable)
        const aw = xi - 26.5; // semiancho del vano de la puerta
        const zA0 = zPl1 + 4.3; // borde inferior del vano
        const zA1 = min(zA0 + 220, zRep - 40); // borde superior del vano
        const zSw = (zA0 + zA1) / 2; // altura del microswitch
        const xMS = aw - 5; // eje del microswitch
        const xD = aw + 10; // semiancho de la puerta (traslape de 10 mm)
        const zD0 = zA0 - 10; // borde inferior de la puerta
        const zD1 = zA1 + 10; // borde superior de la puerta
        const zDc = (zD0 + zD1) / 2; // centro de la puerta
        const rb = 2.5; // radio del nudillo de bisagra
        const xH = -(xD + rb + 0.25); // eje de giro de la puerta (x)
        const yH = -max(rb + 0.25, esp / 2 + 1); // eje de giro de la puerta (y)
        const zH1 = zD0 + 35; // bisagra inferior
        const zH2 = zD1 - 35; // bisagra superior
        const zCam0 = zRepS + 3; // cara inferior de la placa de la camara
        const zLente = zCam0 - 5.5; // cara inferior del lente
        const yCB1 = yi1 - 4; // borde trasero de la placa de control
        const yCB0 = yCB1 - 90; // borde delantero de la placa de control
        const zCB0 = zRepS + 8; // cara inferior de la placa de control
        const zCB1 = zCB0 + 1.6; // cara superior de la placa de control
        const yE1 = yi1 - 6; // extremo USB de la ESP32
        const yE0 = yE1 - 62.7; // extremo de antena de la ESP32
        const yEc = (yE0 + yE1) / 2; // centro de la ESP32
        const zE0 = zCB1 + 11; // cara inferior de la PCB de la ESP32
        const zE1 = zE0 + 1.6; // cara superior de la PCB de la ESP32
        const zUSB = zE1 + 1.63; // eje de los conectores USB-C
        const zP = (zRepS + zi1) / 2; // eje de jack, fusible e interruptor
        const xSW1 = xi - 91.5; // interruptor KCD1
        const xF1 = xi - 55.5; // portafusible
        const xJ1 = xi - 23.5; // jack DC
        const xH0 = -xi + 35.5; // esquina del HX711 (esquina trasera izquierda)
        const yH0 = yi1 - 25.5; // esquina del HX711
        const lTira = 200; // largo de cada tira COB (multiplo de sus marcas de corte)
        const zT0 = zPlato1 + 5; // inicio de las tiras, sobre el borde del plato
        const zT1 = zT0 + lTira; // final de las tiras
        const zL = zRepS + 2; // altura de los cables de las tiras sobre la repisa
        const zM = zRepS + 5.5; // altura de los cables del HX711 y del microswitch
        const zEnt = zCB1 + 5; // altura de entrada de cables en las borneras de la placa
        const xBI = -33.5; // columna izquierda de borneras (X3, X2A); entrada por -X
        const xBD = 26; // columna derecha de borneras (X4, X2B, X1); entrada por +X
        const yX3 = yCB0 + 10.5; // X3: HX711, 4 polos
        const yX2A = yCB0 + 35.5; // X2A: tiras izquierdas, 4 polos
        const yX4 = yCB0 + 35.5; // X4: puerta, 2 polos
        const yX2B = yCB0 + 49.5; // X2B: tiras derechas, 4 polos
        const yX1 = yCB0 + 72; // X1: entrada 5 V, 2 polos
        const nX = nImpar(ancho, dedo); // dedos en aristas paralelas a X
        const nY = nImpar(fondo, dedo); // dedos en aristas paralelas a Y
        const nZ = nImpar(alto, dedo); // dedos en aristas verticales
        const cMDF = [0.84, 0.70, 0.50];
        const cMDF2 = [0.78, 0.62, 0.42];
        const cPLA = [0.96, 0.52, 0.12];
        const cPERF = [0.16, 0.52, 0.30];
        const cHX = [0.08, 0.50, 0.22];
        const cNEGRO = [0.09, 0.09, 0.11];
        const cOSCURO = [0.20, 0.20, 0.24];
        const cALU = [0.78, 0.80, 0.84];
        const cMETAL = [0.66, 0.67, 0.71];
        const cBLANCO = [0.97, 0.97, 0.97];
        const cOPAL = [0.95, 0.95, 0.92];
        const cTAPA = [0.72, 0.72, 0.74];
        const cLED = [1.00, 0.97, 0.80];
        const cRES = [0.86, 0.73, 0.52];
        const cELEC = [0.13, 0.22, 0.58];
        const cCER = [0.92, 0.64, 0.18];
        const cAZUL = [0.16, 0.42, 0.86];
        const cVERDE = [0.10, 0.55, 0.25];
        const cNYLON = [0.94, 0.93, 0.86];
        const cGOMA = [0.16, 0.16, 0.16];
        const cROJO = [0.80, 0.10, 0.10];
        const cGRIS = [0.55, 0.55, 0.60];
        const cCELDA = [0.92, 0.92, 0.92];
        const cAMAR = [0.95, 0.80, 0.10];
        const cPLANO = [0.50, 0.50, 0.55];

        // 0) Comprobaciones de diseño (avisos en Onshape; no detienen el modelo)
        const tanV = 0.4002; // tan(43,6°/2): lado corto de la imagen 4:3 de la Waveshare (C)
        if ((zLente - zPlato1) * tanV < dPlato / 2 + 3)
        {
            reportFeatureWarning(context, id, "La camara no encuadra el plato completo con margen: aumentar el alto.");
        }
        const dEsq = sqrt((xi - 7.5) ^ 2 + (fondo / 2 - esp - 7.5) ^ 2); // eje -> tira de esquina
        const zMaxTira = zFondoPlato + (zLente - zFondoPlato) * (dEsq / (dPlato / 2) - 1);
        if (zT1 > zMaxTira)
        {
            reportFeatureWarning(context, id, "El reflejo de las tiras LED cae dentro del plato: acortar las tiras o aumentar el alto.");
        }

        // 1) Tableros de la caja como placas completas
        solidos(context, id + "t01", [
            [-ancho / 2, 0, 0, ancho / 2, fondo, esp]
        ]); // MDF - Piso
        solidos(context, id + "t02", [
            [-ancho / 2, 0, alto - esp, ancho / 2, fondo, alto]
        ]); // MDF - Tapa superior
        solidos(context, id + "t03", [
            [-ancho / 2, 0, 0, -xi, fondo, alto]
        ]); // MDF - Lateral izquierdo
        solidos(context, id + "t04", [
            [xi, 0, 0, ancho / 2, fondo, alto]
        ]); // MDF - Lateral derecho
        solidos(context, id + "t05", [
            [-ancho / 2, 0, 0, ancho / 2, esp, alto]
        ]); // MDF - Panel frontal
        solidos(context, id + "t06", [
            [-ancho / 2, yi1, 0, ancho / 2, fondo, alto]
        ]); // MDF - Panel trasero

        // 2) Uniones de dedos en las 12 aristas (dueño, otro)
        junta(context, id + "j1", "X", -ancho / 2, ancho / 2, 0, esp, 0, esp, nX, id + "t05", id + "t01");
        junta(context, id + "j2", "X", -ancho / 2, ancho / 2, 0, esp, alto - esp, alto, nX, id + "t05", id + "t02");
        junta(context, id + "j3", "X", -ancho / 2, ancho / 2, yi1, fondo, 0, esp, nX, id + "t06", id + "t01");
        junta(context, id + "j4", "X", -ancho / 2, ancho / 2, yi1, fondo, alto - esp, alto, nX, id + "t06", id + "t02");
        junta(context, id + "j5", "Z", 0, alto, -ancho / 2, -xi, 0, esp, nZ, id + "t05", id + "t03");
        junta(context, id + "j6", "Z", 0, alto, xi, ancho / 2, 0, esp, nZ, id + "t05", id + "t04");
        junta(context, id + "j7", "Z", 0, alto, -ancho / 2, -xi, yi1, fondo, nZ, id + "t06", id + "t03");
        junta(context, id + "j8", "Z", 0, alto, xi, ancho / 2, yi1, fondo, nZ, id + "t06", id + "t04");
        junta(context, id + "j9", "Y", 0, fondo, -ancho / 2, -xi, 0, esp, nY, id + "t03", id + "t01");
        junta(context, id + "j10", "Y", 0, fondo, xi, ancho / 2, 0, esp, nY, id + "t04", id + "t01");
        junta(context, id + "j11", "Y", 0, fondo, -ancho / 2, -xi, alto - esp, alto, nY, id + "t03", id + "t02");
        junta(context, id + "j12", "Y", 0, fondo, xi, ancho / 2, alto - esp, alto, nY, id + "t04", id + "t02");

        // 3) Vanos, agujeros y ranuras de los tableros
        terminar(context, id + "p01", id + "t01", "MDF - Piso", cMDF, "MDF", 0.75, [
            [xLC0 + 5, yc, -1, xLC0 + 5, yc, esp + 1, 2.75],
            [xLC0 + 20, yc, -1, xLC0 + 20, yc, esp + 1, 2.75]
        ]);
        terminar(context, id + "p02", id + "t02", "MDF - Tapa superior", cMDF, "MDF", 0.75, []);
        terminar(context, id + "p03", id + "t03", "MDF - Lateral izquierdo", cMDF, "MDF", 0.75, [
            [-ancho / 2 - 1, fondo / 4 - 10, zRep, -xi, fondo / 4 + 10, zRepS],
            [-ancho / 2 - 1, 3 * fondo / 4 - 10, zRep, -xi, 3 * fondo / 4 + 10, zRepS]
        ]);
        terminar(context, id + "p04", id + "t04", "MDF - Lateral derecho", cMDF, "MDF", 0.75, [
            [xi, fondo / 4 - 10, zRep, ancho / 2 + 1, fondo / 4 + 10, zRepS],
            [xi, 3 * fondo / 4 - 10, zRep, ancho / 2 + 1, 3 * fondo / 4 + 10, zRepS]
        ]);
        terminar(context, id + "p05", id + "t05", "MDF - Panel frontal", cMDF, "MDF", 0.75, [
            [-aw, -1, zA0, aw, esp + 1, zA1],
            [-ancho / 4 - 10, -1, zRep, -ancho / 4 + 10, yi0, zRepS],
            [ancho / 4 - 10, -1, zRep, ancho / 4 + 10, yi0, zRepS]
        ]);
        terminar(context, id + "p06", id + "t06", "MDF - Panel trasero", cMDF, "MDF", 0.75, [
            [xSW1 - 10.6, yi1 - 1, zP - 7.6, xSW1 + 10.6, fondo + 1, zP + 7.6],
            [xF1, yi1 - 1, zP, xF1, fondo + 1, zP, 6.25],
            [xJ1, yi1 - 1, zP, xJ1, fondo + 1, zP, 4.1],
            [-14, yi1 - 1, zUSB - 6.5, 14, fondo + 1, zUSB + 6.5],
            [-ancho / 4 - 10, yi1, zRep, -ancho / 4 + 10, fondo + 1, zRepS],
            [ancho / 4 - 10, yi1, zRep, ancho / 4 + 10, fondo + 1, zRepS]
        ]);

        // 4) Resto de piezas: pieza(id, nombre, color, material, densidad g/cm3, sólidos, cortes)

        // ---------- Carcasa MDF (corte laser)
        pieza(context, id + "p07", "MDF - Repisa de cámara", cMDF, "MDF", 0.75, [
            [-xi, yi0, zRep, xi, yi1, zRepS],
            [-ancho / 2, fondo / 4 - 10, zRep, -xi, fondo / 4 + 10, zRepS],
            [xi, fondo / 4 - 10, zRep, ancho / 2, fondo / 4 + 10, zRepS],
            [-ancho / 2, 3 * fondo / 4 - 10, zRep, -xi, 3 * fondo / 4 + 10, zRepS],
            [xi, 3 * fondo / 4 - 10, zRep, ancho / 2, 3 * fondo / 4 + 10, zRepS],
            [-ancho / 4 - 10, 0, zRep, -ancho / 4 + 10, yi0, zRepS],
            [-ancho / 4 - 10, yi1, zRep, -ancho / 4 + 10, fondo, zRepS],
            [ancho / 4 - 10, 0, zRep, ancho / 4 + 10, yi0, zRepS],
            [ancho / 4 - 10, yi1, zRep, ancho / 4 + 10, fondo, zRepS]
        ], [
            [0, yc, zRep - 1, 0, yc, zRepS + 1, 8], // paso del lente
            [-xi + 21, yi1 - 10.5, zRep - 1, -xi + 30, yi1 - 1.5, zRepS + 1], // pasacables HX711
            [xi - 10.5, yi0 + 21, zRep - 1, xi - 1.5, yi0 + 30, zRepS + 1], // pasacables microswitch
            [-xi + 5, yi0 + 5, zRep - 1, -xi + 5, yi0 + 5, zRepS + 1, 3], // cables de tiras (4 esquinas)
            [xi - 5, yi0 + 5, zRep - 1, xi - 5, yi0 + 5, zRepS + 1, 3],
            [-xi + 5, yi1 - 5, zRep - 1, -xi + 5, yi1 - 5, zRepS + 1, 3],
            [xi - 5, yi1 - 5, zRep - 1, xi - 5, yi1 - 5, zRepS + 1, 3],
            [-31.5, yCB0 + 3.5, zRep - 1, -31.5, yCB0 + 3.5, zRepS + 1, 1.6],
            [-31.5, yCB1 - 3.5, zRep - 1, -31.5, yCB1 - 3.5, zRepS + 1, 1.6],
            [31.5, yCB0 + 3.5, zRep - 1, 31.5, yCB0 + 3.5, zRepS + 1, 1.6],
            [31.5, yCB1 - 3.5, zRep - 1, 31.5, yCB1 - 3.5, zRepS + 1, 1.6],
            [-15.35, yc - 9.45, zRep - 1, -15.35, yc - 9.45, zRepS + 1, 1.1],
            [-15.35, yc + 9.45, zRep - 1, -15.35, yc + 9.45, zRepS + 1, 1.1],
            [15.35, yc - 9.45, zRep - 1, 15.35, yc - 9.45, zRepS + 1, 1.1],
            [15.35, yc + 9.45, zRep - 1, 15.35, yc + 9.45, zRepS + 1, 1.1]
        ]);
        pieza(context, id + "p08", "MDF - Puerta", cMDF2, "MDF", 0.75, [
            [-xD, -esp, zD0, xD, 0, zD1]
        ], []);
        pieza(context, id + "p09", "MDF - Bandeja de pesaje", cMDF2, "MDF", 0.75, [
            [0, yc, zPl0, 0, yc, zPl1, rPlat]
        ], []);

        // ---------- Piezas PLA (impresion 3D)
        pieza(context, id + "p10", "PLA - Separador inferior de celda", cPLA, "PLA", 1.24, [
            [xLC0, yc - 6.35, zi0, xLC0 + 25, yc + 6.35, zLC0]
        ], [
            [xLC0 + 5, yc, zi0 - 1, xLC0 + 5, yc, zLC0 + 1, 2.75],
            [xLC0 + 20, yc, zi0 - 1, xLC0 + 20, yc, zLC0 + 1, 2.75]
        ]);
        pieza(context, id + "p11", "PLA - Separador superior de celda", cPLA, "PLA", 1.24, [
            [xLC1 - 25, yc - 6.35, zLC1, xLC1, yc + 6.35, zHub0]
        ], [
            [xLC1 - 5, yc, zLC1 - 1, xLC1 - 5, yc, zHub0 + 1, 2.25],
            [xLC1 - 20, yc, zLC1 - 1, xLC1 - 20, yc, zHub0 + 1, 2.25]
        ]);
        pieza(context, id + "p12", "PLA - Soporte de bandeja", cPLA, "PLA", 1.24, [
            [0, yc, zHub0, 0, yc, zPl0, 50]
        ], [
            [xLC1 - 5, yc, zHub0 - 1, xLC1 - 5, yc, zPl0 + 1, 2.25],
            [xLC1 - 20, yc, zHub0 - 1, xLC1 - 20, yc, zPl0 + 1, 2.25]
        ]);
        pieza(context, id + "p13", "PLA - Soporte de microswitch", cPLA, "PLA", 1.24, [
            [xMS + 3.25, yi0, zSw - 12, aw + 8, 18, zSw + 12]
        ], [
            [xMS + 3, 10.6, zSw - 4.75, aw + 9, 10.6, zSw - 4.75, 1.1],
            [xMS + 3, 10.6, zSw + 4.75, aw + 9, 10.6, zSw + 4.75, 1.1]
        ]);
        pieza(context, id + "p14", "PLA - Soporte HX711 y X5", cPLA, "PLA", 1.24, [
            [xH0 - 3.5, yi1 - 36.5, zi0, xH0 + 46, yi1 - 2.5, zi0 + 4]
        ], [
            [xH0 - 0.2, yH0 - 0.2, zi0 + 2, xH0 + 34.2, yH0 + 20.2, zi0 + 5]
        ]);
        pieza(context, id + "p15", "PLA - Tirador de puerta", cPLA, "PLA", 1.24, [
            [xD - 30, -esp - 15, zDc - 35, xD - 18, -esp, zDc + 35]
        ], [
            [xD - 31, -esp - 10, zDc - 25, xD - 17, -esp + 1, zDc + 25]
        ]);
        pieza(context, id + "p16", "PLA - Canaleta HX711 (esquina trasera izquierda)", cPLA, "PLA", 1.24, [
            [-xi + 19.5, yi1 - 12, zi0 + 25, -xi + 31.5, yi1, zRep]
        ], [
            [-xi + 21, yi1 - 10.5, zi0 + 24, -xi + 30, yi1 - 1.5, zRep + 1]
        ]);
        pieza(context, id + "p17", "PLA - Canaleta microswitch (lateral derecho)", cPLA, "PLA", 1.24, [
            [xi - 12, yi0 + 19.5, zSw + 5, xi, yi0 + 31.5, zRep]
        ], [
            [xi - 10.5, yi0 + 21, zSw + 4, xi - 1.5, yi0 + 30, zRep + 1]
        ]);
        pieza(context, id + "p18", "PLA - Parasol del lente", cPLA, "PLA", 1.24, [
            [0, yc, zRep - 8, 0, yc, zRep, 14]
        ], [
            [0, yc, zRep - 9, 0, yc, zRep + 1, 10]
        ]);

        // ---------- Herrajes y separadores
        pieza(context, id + "p19", "Bisagra inferior - hoja fija", cMETAL, "Acero", 7.85, [
            [xH - 15, -1, zH1 - 15, xH - 2.6, 0, zH1 + 15],
            [xH - 2.6, -1, zH1 - 5, xH, 0, zH1 + 5],
            [xH, yH, zH1 - 5, xH, yH, zH1 + 5, rb]
        ], []);
        pieza(context, id + "p20", "Bisagra inferior - hoja móvil", cMETAL, "Acero", 7.85, [
            [xH + 2.6, -esp - 1, zH1 - 15, xH + 15, -esp, zH1 + 15],
            [xH, -esp - 1, zH1 - 15, xH + 2.6, -esp, zH1 - 5],
            [xH, -esp - 1, zH1 + 5, xH + 2.6, -esp, zH1 + 15],
            [xH, yH, zH1 - 15, xH, yH, zH1 - 5, rb],
            [xH, yH, zH1 + 5, xH, yH, zH1 + 15, rb]
        ], []);
        pieza(context, id + "p21", "Bisagra superior - hoja fija", cMETAL, "Acero", 7.85, [
            [xH - 15, -1, zH2 - 15, xH - 2.6, 0, zH2 + 15],
            [xH - 2.6, -1, zH2 - 5, xH, 0, zH2 + 5],
            [xH, yH, zH2 - 5, xH, yH, zH2 + 5, rb]
        ], []);
        pieza(context, id + "p22", "Bisagra superior - hoja móvil", cMETAL, "Acero", 7.85, [
            [xH + 2.6, -esp - 1, zH2 - 15, xH + 15, -esp, zH2 + 15],
            [xH, -esp - 1, zH2 - 15, xH + 2.6, -esp, zH2 - 5],
            [xH, -esp - 1, zH2 + 5, xH + 2.6, -esp, zH2 + 15],
            [xH, yH, zH2 - 15, xH, yH, zH2 - 5, rb],
            [xH, yH, zH2 + 5, xH, yH, zH2 + 15, rb]
        ], []);
        pieza(context, id + "p23", "Pata de goma 1", cGOMA, "Caucho", 1.2, [
            [-ancho / 2 + 25, 25, -8, -ancho / 2 + 25, 25, 0, 10]
        ], []);
        pieza(context, id + "p24", "Pata de goma 2", cGOMA, "Caucho", 1.2, [
            [ancho / 2 - 25, 25, -8, ancho / 2 - 25, 25, 0, 10]
        ], []);
        pieza(context, id + "p25", "Pata de goma 3", cGOMA, "Caucho", 1.2, [
            [-ancho / 2 + 25, fondo - 25, -8, -ancho / 2 + 25, fondo - 25, 0, 10]
        ], []);
        pieza(context, id + "p26", "Pata de goma 4", cGOMA, "Caucho", 1.2, [
            [ancho / 2 - 25, fondo - 25, -8, ancho / 2 - 25, fondo - 25, 0, 10]
        ], []);
        pieza(context, id + "p27", "Separador M3x8 placa de control 1", cNYLON, "Nylon", 1.14, [
            [-31.5, yCB0 + 3.5, zRepS, -31.5, yCB0 + 3.5, zCB0, 2.5]
        ], []);
        pieza(context, id + "p28", "Separador M3x8 placa de control 2", cNYLON, "Nylon", 1.14, [
            [-31.5, yCB1 - 3.5, zRepS, -31.5, yCB1 - 3.5, zCB0, 2.5]
        ], []);
        pieza(context, id + "p29", "Separador M3x8 placa de control 3", cNYLON, "Nylon", 1.14, [
            [31.5, yCB0 + 3.5, zRepS, 31.5, yCB0 + 3.5, zCB0, 2.5]
        ], []);
        pieza(context, id + "p30", "Separador M3x8 placa de control 4", cNYLON, "Nylon", 1.14, [
            [31.5, yCB1 - 3.5, zRepS, 31.5, yCB1 - 3.5, zCB0, 2.5]
        ], []);
        pieza(context, id + "p31", "Separador M2x3 cámara 1", cNYLON, "Nylon", 1.14, [
            [-15.35, yc - 9.45, zRepS, -15.35, yc - 9.45, zCam0, 1.75]
        ], []);
        pieza(context, id + "p32", "Separador M2x3 cámara 2", cNYLON, "Nylon", 1.14, [
            [-15.35, yc + 9.45, zRepS, -15.35, yc + 9.45, zCam0, 1.75]
        ], []);
        pieza(context, id + "p33", "Separador M2x3 cámara 3", cNYLON, "Nylon", 1.14, [
            [15.35, yc - 9.45, zRepS, 15.35, yc - 9.45, zCam0, 1.75]
        ], []);
        pieza(context, id + "p34", "Separador M2x3 cámara 4", cNYLON, "Nylon", 1.14, [
            [15.35, yc + 9.45, zRepS, 15.35, yc + 9.45, zCam0, 1.75]
        ], []);

        // ---------- Iluminación: 4 tiras COB 5 V verticales en las esquinas
        // Sección en coordenadas locales de la esquina (u desde la pared lateral,
        // v desde la pared frontal o trasera), en mm.
        const secPerfil = [[0, 0], [15, 0], [0, 15]]; // aluminio, cara de 45° hacia el plato
        const secTira = [[10.33, 4.67], [10.89, 5.24], [5.24, 10.89], [4.67, 10.33]]; // COB de 8 mm
        const secDifusor = [[16.5, 0], [18, 0], [0, 18], [0, 16.5]]; // difusor opal
        const secTapa = [[0, 0], [18, 0], [0, 18]]; // tapas de los extremos
        const esquinas = [
            ["delantera izquierda", -xi, yi0, 1, 1],
            ["delantera derecha", xi, yi0, -1, 1],
            ["trasera izquierda", -xi, yi1, 1, -1],
            ["trasera derecha", xi, yi1, -1, -1]
        ];
        for (var k = 0; k < 4; k += 1)
        {
            const e = esquinas[k];
            const etiq = "L" ~ toString(k + 1);
            const sufijo = " (esquina " ~ e[0] ~ ")";
            const L = id + ("luz" ~ toString(k + 1));
            pieza(context, L + "perfil", etiq ~ " - Perfil esquinero de aluminio 16x16" ~ sufijo, cALU, "Aluminio", 2.7, [
                [zT0 - 3, zT1 + 3, enEsquina(secPerfil, e[1], e[2], e[3], e[4])]
            ], []);
            pieza(context, L + "difusor", etiq ~ " - Difusor opal" ~ sufijo, cOPAL, "Policarbonato", 1.2, [
                [zT0 - 3, zT1 + 3, enEsquina(secDifusor, e[1], e[2], e[3], e[4])]
            ], []);
            pieza(context, L + "tira", "LED" ~ toString(k + 1) ~ " - Tira COB 5 V 4000 K 200 mm" ~ sufijo, cLED, "Electronica", 2.0, [
                [zT0, zT1, enEsquina(secTira, e[1], e[2], e[3], e[4])]
            ], []);
            pieza(context, L + "tapaInf", etiq ~" - Tapa inferior del perfil" ~ sufijo, cTAPA, "Plastico", 1.2, [
                [zT0 - 5, zT0 - 3, enEsquina(secTapa, e[1], e[2], e[3], e[4])]
            ], []);
            pieza(context, L + "tapaSup", etiq ~" - Tapa superior del perfil con salida de cable" ~ sufijo, cTAPA, "Plastico", 1.2, [
                [zT1 + 3, zT1 + 5, enEsquina(secTapa, e[1], e[2], e[3], e[4])]
            ], []);
        }

        // ---------- Placa de control (siempre visible: es la base de los conectores)
        pieza(context, id + "p35", "Placa perforada 7x9 cm - control", cPERF, "FR4", 1.85, [
            [-35, yCB0, zCB0, 35, yCB1, zCB1]
        ], [
            [-31.5, yCB0 + 3.5, zCB0 - 1, -31.5, yCB0 + 3.5, zCB1 + 1, 1.6],
            [-31.5, yCB1 - 3.5, zCB0 - 1, -31.5, yCB1 - 3.5, zCB1 + 1, 1.6],
            [31.5, yCB0 + 3.5, zCB0 - 1, 31.5, yCB0 + 3.5, zCB1 + 1, 1.6],
            [31.5, yCB1 - 3.5, zCB0 - 1, 31.5, yCB1 - 3.5, zCB1 + 1, 1.6]
        ]);

        // ---------- Electrónica comercial simplificada (se puede ocultar para usar STEP)
        if (definition.electronica)
        {
            pieza(context, id + "p36", "U1 - ESP32-S3-DevKitC-1 N16R8", cOSCURO, "Electronica", 2.0, [
                [-12.7, yE0, zE0, 12.7, yE1, zE1],
                [-12.7, yEc - 27.94, zCB1 + 8.5, -10.16, yEc + 27.94, zE0],
                [10.16, yEc - 27.94, zCB1 + 8.5, 12.7, yEc + 27.94, zE0],
                [-9, yE0, zE1, 9, yE0 + 25.5, zE1 + 3.1],
                [-10.47, yE1 - 6.35, zE1, -1.53, yE1 + 1, zE1 + 3.26],
                [1.53, yE1 - 6.35, zE1, 10.47, yE1 + 1, zE1 + 3.26],
                [-11.25, yE1 - 12, zE1, -7.75, yE1 - 8.5, zE1 + 1.5],
                [7.75, yE1 - 12, zE1, 11.25, yE1 - 8.5, zE1 + 1.5]
            ], []);
            pieza(context, id + "p37", "Espadín hembra 1x22 izquierdo", cNEGRO, "Electronica", 2.0, [
                [-12.7, yEc - 27.94, zCB1, -10.16, yEc + 27.94, zCB1 + 8.5]
            ], []);
            pieza(context, id + "p38", "Espadín hembra 1x22 derecho", cNEGRO, "Electronica", 2.0, [
                [10.16, yEc - 27.94, zCB1, 12.7, yEc + 27.94, zCB1 + 8.5]
            ], []);
            pieza(context, id + "p39", "CAM1 - Waveshare OV5640 Camera Board (C)", cNEGRO, "Electronica", 2.0, [
                [-17.85, yc - 11.95, zCam0, 17.85, yc + 11.95, zCam0 + 1.6],
                [-4.25, yc - 4.25, zCam0 - 4.7, 4.25, yc + 4.25, zCam0],
                [0, yc, zCam0 - 5.5, 0, yc, zCam0 - 4.7, 3],
                [-11.43, yc + 5.37, zCam0 + 1.6, 11.43, yc + 10.45, zCam0 + 10.1]
            ], [
                [-15.35, yc - 9.45, zCam0 - 1, -15.35, yc - 9.45, zCam0 + 3, 1.1],
                [-15.35, yc + 9.45, zCam0 - 1, -15.35, yc + 9.45, zCam0 + 3, 1.1],
                [15.35, yc - 9.45, zCam0 - 1, 15.35, yc - 9.45, zCam0 + 3, 1.1],
                [15.35, yc + 9.45, zCam0 - 1, 15.35, yc + 9.45, zCam0 + 3, 1.1]
            ]);
            pieza(context, id + "p40", "LC1 - Celda de carga 5 kg", cALU, "Aluminio", 2.7, [
                [xLC0, yc - 6.35, zLC0, xLC1, yc + 6.35, zLC1]
            ], [
                [xLC0 + 5, yc, zLC0 - 1, xLC0 + 5, yc, zLC1 + 1, 2.5],
                [xLC1 - 5, yc, zLC0 - 1, xLC1 - 5, yc, zLC1 + 1, 2],
                [xLC0 + 20, yc, zLC0 - 1, xLC0 + 20, yc, zLC1 + 1, 2.5],
                [xLC1 - 20, yc, zLC0 - 1, xLC1 - 20, yc, zLC1 + 1, 2],
                [xLC0 + 32.5, yc - 7, zLC0 + 6.35, xLC0 + 32.5, yc + 7, zLC0 + 6.35, 5],
                [xLC0 + 47.5, yc - 7, zLC0 + 6.35, xLC0 + 47.5, yc + 7, zLC0 + 6.35, 5],
                [xLC0 + 32.5, yc - 7, zLC0 + 5.35, xLC0 + 47.5, yc + 7, zLC0 + 7.35]
            ]);
            pieza(context, id + "p41", "U2 - Módulo HX711", cHX, "Electronica", 2.0, [
                [xH0, yH0, zi0 + 2, xH0 + 34, yH0 + 20, zi0 + 3.6],
                [xH0 + 12, yH0 + 7, zi0 + 3.6, xH0 + 22, yH0 + 13, zi0 + 5.1],
                [xH0 + 30.5, yH0 + 4.92, zi0 + 3.6, xH0 + 33.04, yH0 + 15.08, zi0 + 12.1],
                [xH0 + 0.96, yH0 + 4.92, zi0 + 3.6, xH0 + 3.5, yH0 + 15.08, zi0 + 12.1]
            ], []);
            pieza(context, id + "p42", "SW2 - Microswitch KW11-3Z", cNEGRO, "Electronica", 2.0, [
                [xMS - 3.25, 5.6, zSw - 10, xMS + 3.25, 15.6, zSw + 10],
                [xMS - 2, 4.6, zSw - 9, xMS + 2, 5.6, zSw + 9],
                [xMS - 1.75, 2.6, zSw + 7, xMS + 1.75, 2.6, zSw + 7, 2.5],
                [xMS - 0.4, 15.6, zSw - 8.5, xMS + 0.4, 19.6, zSw - 5.5],
                [xMS - 0.4, 15.6, zSw - 1.5, xMS + 0.4, 19.6, zSw + 1.5],
                [xMS - 0.4, 15.6, zSw + 5.5, xMS + 0.4, 19.6, zSw + 8.5]
            ], [
                [xMS - 3.5, 10.6, zSw - 4.75, xMS + 3.5, 10.6, zSw - 4.75, 1.1],
                [xMS - 3.5, 10.6, zSw + 4.75, xMS + 3.5, 10.6, zSw + 4.75, 1.1]
            ]);
            pieza(context, id + "p43", "Q1 - MOSFET AO3400A en adaptador SOT-23", cAZUL, "Electronica", 2.0, [
                [6.19, yCB0 + 8.23, zCB1, 13.81, yCB0 + 10.77, zCB1 + 2.5],
                [5, yCB0 + 5.5, zCB1 + 2.5, 15, yCB0 + 13.5, zCB1 + 3.5],
                [8.55, yCB0 + 8.7, zCB1 + 3.5, 11.45, yCB0 + 10.3, zCB1 + 4.6]
            ], []);
            pieza(context, id + "p44", "R13 - Resistencia 10 kΩ (puerta)", cRES, "Electronica", 2.0, [
                [-7.15, yCB0 + 5.5, zCB1 + 1.15, -0.85, yCB0 + 5.5, zCB1 + 1.15, 1.15]
            ], []);
            pieza(context, id + "p45", "R14 - Resistencia 100 Ω (compuerta)", cRES, "Electronica", 2.0, [
                [20.85, yCB0 + 13.5, zCB1 + 1.15, 27.15, yCB0 + 13.5, zCB1 + 1.15, 1.15]
            ], []);
            pieza(context, id + "p46", "R15 - Resistencia 100 kΩ (compuerta a GND)", cRES, "Electronica", 2.0, [
                [20.85, yCB0 + 5.5, zCB1 + 1.15, 27.15, yCB0 + 5.5, zCB1 + 1.15, 1.15]
            ], []);
            pieza(context, id + "p47", "C1 - Electrolítico 470 µF 16 V", cELEC, "Electronica", 2.0, [
                [22, yCB0 + 25.5, zCB1, 22, yCB0 + 25.5, zCB1 + 12, 4]
            ], []);
            pieza(context, id + "p48", "C2 - Cerámico 100 nF", cCER, "Ceramica", 2.4, [
                [16, yCB0 + 31.5, zCB1, 20, yCB0 + 34, zCB1 + 5]
            ], []);
            pieza(context, id + "p49", "C3 - Electrolítico 100 µF 10 V", cELEC, "Electronica", 2.0, [
                [-18, yCB0 + 5.5, zCB1, -18, yCB0 + 5.5, zCB1 + 11, 3.15]
            ], []);
            pieza(context, id + "p50", "C4 - Cerámico 100 nF", cCER, "Ceramica", 2.4, [
                [-13.5, yCB0 + 10.5, zCB1, -9.5, yCB0 + 13, zCB1 + 5]
            ], []);
            pieza(context, id + "p51", "X1 - Bornera de tornillo 2P 5,08 mm - entrada 5 V", cAZUL, "Electronica", 2.0,
                borneraY(xBD, yX1, zCB1, 2), []);
            pieza(context, id + "p52", "X2A - Bornera de tornillo 4P 5,08 mm - tiras LED1 y LED3 (izquierda)", cAZUL, "Electronica", 2.0,
                borneraY(xBI, yX2A, zCB1, 4), []);
            pieza(context, id + "p53", "X2B - Bornera de tornillo 4P 5,08 mm - tiras LED2 y LED4 (derecha)", cAZUL, "Electronica", 2.0,
                borneraY(xBD, yX2B, zCB1, 4), []);
            pieza(context, id + "p54", "X3 - Bornera enchufable 4P 5,08 mm - HX711 (3V3, GND, DT, SCK)", cVERDE, "Electronica", 2.0,
                borneraY(xBI, yX3, zCB1, 4), []);
            pieza(context, id + "p55", "X4 - Bornera enchufable 2P 5,08 mm - puerta (DOOR_N, GND)", cVERDE, "Electronica", 2.0,
                borneraY(xBD, yX4, zCB1, 2), []);
            pieza(context, id + "p56", "X5 - Bornera de tornillo 4P 5,08 mm - celda (E+, E-, A-, A+)", cAZUL, "Electronica", 2.0,
                borneraX(xH0 + 14, yi1 - 35.5, zi0 + 4, 4), []);
            pieza(context, id + "p57", "SW1 - Interruptor KCD1-102", cNEGRO, "Electronica", 2.0, [
                [xSW1 - 12.5, fondo, zP - 9.5, xSW1 + 12.5, fondo + 2, zP + 9.5],
                [xSW1 - 8.5, fondo + 2, zP - 6, xSW1 + 8.5, fondo + 5, zP + 6],
                [xSW1 - 10.5, yi1 - 12, zP - 7.5, xSW1 + 10.5, fondo, zP + 7.5],
                [xSW1 - 0.4, yi1 - 20, zP - 6.4, xSW1 + 0.4, yi1 - 12, zP - 1.6],
                [xSW1 - 0.4, yi1 - 20, zP + 1.6, xSW1 + 0.4, yi1 - 12, zP + 6.4]
            ], []);
            pieza(context, id + "p58", "F1 - Portafusible 5x20 con fusible T3,15 A", cNEGRO, "Electronica", 2.0, [
                [xF1, fondo + 2, zP, xF1, fondo + 15, zP, 7],
                [xF1, fondo, zP, xF1, fondo + 2, zP, 8],
                [xF1, yi1 - 25, zP, xF1, fondo, zP, 6],
                [xF1, yi1 - 3, zP, xF1, yi1, zP, 8],
                [xF1 - 0.5, yi1 - 33, zP - 2.5, xF1 + 0.5, yi1 - 25, zP + 2.5]
            ], []);
            pieza(context, id + "p59", "J1 - Jack DC 5,5 x 2,1 mm de panel", cNEGRO, "Electronica", 2.0, [
                [xJ1, fondo, zP, xJ1, fondo + 2.5, zP, 5],
                [xJ1, yi1 - 6, zP, xJ1, fondo, zP, 3.9],
                [xJ1, yi1 - 2, zP, xJ1, yi1, zP, 5.5],
                [xJ1 - 4.5, yi1 - 14, zP - 4, xJ1 + 4.5, yi1 - 6, zP + 4],
                [xJ1 - 0.4, yi1 - 19, zP - 3, xJ1 + 0.4, yi1 - 14, zP + 3]
            ], [
                [xJ1, fondo - 5, zP, xJ1, fondo + 3, zP, 2.75]
            ]);
        }

        // ---------- Cables (representación de recorridos; radio = haz de conductores)
        pieza(context, id + "p60", "Cable +5V AWG20 - J1 a F1", cROJO, "Cable", 2.5, cable([
            [xJ1, yi1 - 19, zP], [xF1, yi1 - 33, zP]
        ], 1.25), []);
        pieza(context, id + "p61", "Cable +5V AWG20 - F1 a SW1", cROJO, "Cable", 2.5, cable([
            [xF1 - 6.5, yi1 - 22.5, zP], [xSW1, yi1 - 20, zP - 4]
        ], 1.25), []);
        pieza(context, id + "p62", "Cable +5V AWG20 - SW1 a X1", cROJO, "Cable", 2.5, cable([
            [xSW1, yi1 - 20, zP + 4], [xBD + 12, yX1 + 2.54, zP + 4],
            [xBD + 12, yX1 + 2.54, zEnt], [xBD + 7.5, yX1 + 2.54, zEnt]
        ], 1.25), []);
        pieza(context, id + "p63", "Cable GND AWG20 - J1 a X1", cNEGRO, "Cable", 2.5, cable([
            [xJ1, yi1 - 15.5, zP - 3], [xJ1 - 8, yi1 - 15.5, zRepS + 6.5],
            [xBD + 12, yX1 + 7.62, zRepS + 6.5], [xBD + 12, yX1 + 7.62, zEnt],
            [xBD + 7.5, yX1 + 7.62, zEnt]
        ], 1.25), []);
        pieza(context, id + "p64", "Cable LED1 AWG22 rojo/negro - esquina delantera izquierda a X2A", cROJO, "Cable", 2.5, cable([
            [-xi + 5, yi0 + 5, zT1 + 5], [-xi + 5, yi0 + 5, zL], [xBI - 5.5, yi0 + 5, zL],
            [xBI - 5.5, yX2A + 5.08, zL], [xBI - 5.5, yX2A + 5.08, zEnt], [xBI, yX2A + 5.08, zEnt]
        ], 1.5), []);
        pieza(context, id + "p65", "Cable LED2 AWG22 rojo/negro - esquina delantera derecha a X2B", cROJO, "Cable", 2.5, cable([
            [xi - 5, yi0 + 5, zT1 + 5], [xi - 5, yi0 + 5, zL], [xBD + 13, yi0 + 5, zL],
            [xBD + 13, yX2B + 5.08, zL], [xBD + 13, yX2B + 5.08, zEnt], [xBD + 7.5, yX2B + 5.08, zEnt]
        ], 1.5), []);
        pieza(context, id + "p66", "Cable LED3 AWG22 rojo/negro - esquina trasera izquierda a X2A", cROJO, "Cable", 2.5, cable([
            [-xi + 5, yi1 - 5, zT1 + 5], [-xi + 5, yi1 - 5, zL], [-xi + 5, yi1 - 26.5, zL],
            [xBI - 5.5, yi1 - 26.5, zL], [xBI - 5.5, yX2A + 15.24, zL],
            [xBI - 5.5, yX2A + 15.24, zEnt], [xBI, yX2A + 15.24, zEnt]
        ], 1.5), []);
        pieza(context, id + "p67", "Cable LED4 AWG22 rojo/negro - esquina trasera derecha a X2B", cROJO, "Cable", 2.5, cable([
            [xi - 5, yi1 - 5, zT1 + 5], [xi - 5, yi1 - 5, zL], [xBD + 13, yi1 - 5, zL],
            [xBD + 13, yX2B + 15.24, zL], [xBD + 13, yX2B + 15.24, zEnt], [xBD + 7.5, yX2B + 15.24, zEnt]
        ], 1.5), []);
        pieza(context, id + "p68", "Cable HX711 4 hilos - U2 a X3 por la canaleta", cGRIS, "Cable", 2.5, cable([
            [xH0 + 2.23, yH0 + 10, zi0 + 13.6], [-xi + 25.5, yi1 - 6, zi0 + 13.6],
            [-xi + 25.5, yi1 - 6, zM], [xBI - 10.5, yX3 + 10.16, zM],
            [xBI - 10.5, yX3 + 10.16, zEnt], [xBI, yX3 + 10.16, zEnt]
        ], 1.5), []);
        pieza(context, id + "p69", "Cable de la celda 4 hilos - LC1 a X5 (sujeto al piso)", cCELDA, "Cable", 2.5, cable([
            [xLC0, yc, (zLC0 + zLC1) / 2], [xLC0 - 5.5, yc, (zLC0 + zLC1) / 2],
            [xLC0 - 5.5, yc, zi0 + 2], [xLC0 - 5.5, yi1 - 41.5, zi0 + 2],
            [xH0 + 24.16, yi1 - 41.5, zi0 + 2], [xH0 + 24.16, yi1 - 41.5, zi0 + 9],
            [xH0 + 24.16, yi1 - 35.5, zi0 + 9]
        ], 1.25), []);
        pieza(context, id + "p70", "Cable de puerta 2 hilos - SW2 a X4 por la canaleta", cAMAR, "Cable", 2.5, cable([
            [xMS, 19.6, zSw], [xi - 6, yi0 + 25.5, zSw], [xi - 6, yi0 + 25.5, zM],
            [xBD + 18, yi0 + 25.5, zM], [xBD + 18, yX4 + 5.08, zM],
            [xBD + 18, yX4 + 5.08, zEnt], [xBD + 7.5, yX4 + 5.08, zEnt]
        ], 1.25), []);
        pieza(context, id + "p71", "Cable plano CAM1 a U1 (17 hilos, máximo 10 cm)", cPLANO, "Cable", 2.5, [
            [-11.43, yc + 5.37, zCam0 + 10.1, 11.43, yc + 10.45, zCam0 + 24],
            [-11.43, yc + 5.37, zCam0 + 24, 11.43, yCB0 + 2.5, zCam0 + 25],
            [-11.43, yCB0 + 0.5, zCB1, 11.43, yCB0 + 2.5, zCam0 + 24]
        ], []);

        // ---------- Referencia
        pieza(context, id + "p72", "Referencia - Plato Ø220 (no se fabrica)", cBLANCO, "Ceramica", 2.4, [
            [0, yc, zPl1, 0, yc, zPlato1, dPlato / 2]
        ], [
            [0, yc, zPl1 + 3, 0, yc, zPlato1 + 1, dPlato / 2 - 10]
        ]);

        // 5) Conectores de ensamble
        const ejeBisagra = coordSystem(vector(xH, yH, zH1) * millimeter, vector(1, 0, 0), vector(0, 0, 1));
        opMateConnector(context, id + "mcFija", { "coordSystem" : ejeBisagra, "owner" : qCreatedBy(id + "p19" + "s", EntityType.BODY) });
        opMateConnector(context, id + "mcMovil", { "coordSystem" : ejeBisagra, "owner" : qCreatedBy(id + "p20" + "s", EntityType.BODY) });
        // Puntos para colocar los modelos STEP comerciales (en piezas que no se ocultan)
        conector(context, id + "mcU1", id + "p35", [0, yEc, zE0], [1, 0, 0], [0, 0, 1]); // U1: centro inferior de la PCB
        conector(context, id + "mcQ1", id + "p35", [10, yCB0 + 9.5, zCB1], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcX1", id + "p35", [xBD, yX1, zCB1], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcX2A", id + "p35", [xBI, yX2A, zCB1], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcX2B", id + "p35", [xBD, yX2B, zCB1], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcX3", id + "p35", [xBI, yX3, zCB1], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcX4", id + "p35", [xBD, yX4, zCB1], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcCAM1", id + "p07", [0, yc, zCam0], [1, 0, 0], [0, 0, 1]); // CAM1: centro inferior de la PCB
        conector(context, id + "mcLC1", id + "t01", [xLC0, yc, zLC0], [1, 0, 0], [0, 0, 1]); // LC1: extremo fijo, cara inferior
        conector(context, id + "mcU2", id + "p14", [xH0, yH0, zi0 + 2], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcX5", id + "p14", [xH0 + 14, yi1 - 35.5, zi0 + 4], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcSW2", id + "p13", [xMS, 10.6, zSw], [1, 0, 0], [0, 0, 1]);
        conector(context, id + "mcJ1", id + "t06", [xJ1, fondo, zP], [1, 0, 0], [0, 1, 0]); // cara exterior del panel
        conector(context, id + "mcF1", id + "t06", [xF1, fondo, zP], [1, 0, 0], [0, 1, 0]);
        conector(context, id + "mcSW1", id + "t06", [xSW1, fondo, zP], [1, 0, 0], [0, 1, 0]);

        // 6) Puerta abierta 100 grados alrededor del eje de las bisagras (solo para ver el interior)
        if (definition.puertaAbierta)
        {
            opTransform(context, id + "abrirPuerta", {
                        "bodies" : qUnion([qCreatedBy(id + "p08" + "s", EntityType.BODY), qCreatedBy(id + "p15" + "s", EntityType.BODY), qCreatedBy(id + "p20" + "s", EntityType.BODY), qCreatedBy(id + "p22" + "s", EntityType.BODY)]),
                        "transform" : rotationAround(line(vector(xH, yH, 0) * millimeter, vector(0, 0, 1)), -100 * degree)
                    });
        }
    });
