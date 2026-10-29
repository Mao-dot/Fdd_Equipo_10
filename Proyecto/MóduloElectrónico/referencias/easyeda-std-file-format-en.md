# EasyEDA Standard Edition File Format Specification

## Overview

EasyEDA Standard Edition (EasyEDA Std) uses an open JSON-based file format. With this format, you can create schematics or PCB designs using code, even with a simple text editor. When you need to batch-add hundreds of components, you can generate an EasyEDA file programmatically and import it into the editor.

The file format includes the following document types:

| docType | Document Type |
|---------|--------------|
| 1 | Schematic |
| 2 | Schematic Symbol |
| 3 | PCB |
| 4 | PCB Footprint |
| 5 | Schematic Project (multi-sheet) |

## Common Format

### Delimiters

EasyEDA uses special characters as delimiters to compress data, making files smaller and faster to transfer:

| Delimiter | Name | Usage |
|-----------|------|-------|
| `~` | Tilde | Separates shape attribute fields |
| `` ` `` | Back Quote | Separates custom attribute key-value pairs |
| `^^` | Double Circumflex | Joins segments of compound shapes (Pin, Netflag, PAD) |
| `#@$` | Octothorpe-At-Dollar | Joins shapes within Symbol/Footprint |

### Head `head`

The head is a JSON object containing basic document information.

```json
{
  "docType": "1",
  "editorVersion": "6.5.51",
  "newgId": true,
  "c_para": {},
  "x": "0",
  "y": "0",
  "hasIdFlag": true,
  "c_spiceCmd": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| docType | string | Document type |
| editorVersion | string | Editor version |
| newgId | boolean | Whether internal elements generate unique IDs |
| c_para | object | Custom attributes |
| x | string | Document origin X coordinate |
| y | string | Document origin Y coordinate |
| hasIdFlag | boolean | Whether library has bound footprint UUID |
| c_spiceCmd | string | Simulation command (schematic only) |

### Canvas `canvas`

String type, separated by `~`.

**Schematic canvas format:**

```
CA~viewWidth~viewHeight~backGround~gridVisible~gridColor~gridSize~canvasWidth~canvasHeight~gridStyle~snapSize~unit~altSnapSize~originX~originY
```

| # | Field | Description |
|---|-------|-------------|
| 1 | CA | Fixed identifier |
| 2 | viewWidth | View box width |
| 3 | viewHeight | View box height |
| 4 | backGround | Background color |
| 5 | gridVisible | Grid visibility (yes/none) |
| 6 | gridColor | Grid color |
| 7 | gridSize | Grid size |
| 8 | canvasWidth | Canvas width |
| 9 | canvasHeight | Canvas height |
| 10 | gridStyle | Grid style (line/dot) |
| 11 | snapSize | Snap grid size |
| 12 | unit | Unit (pixel) |
| 13 | altSnapSize | Alt key snap size |
| 14 | originX | Canvas origin X |
| 15 | originY | Canvas origin Y |

**PCB canvas format** (additional fields beyond schematic):

| # | Field | Description |
|---|-------|-------------|
| 13 | routingWidth | Routing width |
| 14 | routingAngle | Routing angle (45/90/free) |
| 15 | copperAreaDisplay | Copper area visibility |
| 16 | altSnapSize | Alt key snap size |
| 17 | originX | Canvas origin X |
| 18 | originY | Canvas origin Y |
| 19 | routeConflict | Routing conflict mode |
| 20 | removeLoop | Whether to remove loops |

### Shape Data `shape`

String array type. Each entry is the compressed data of one shape element.

```json
"shape": [
  "R~440~300~~~50~110~#000000~1~0~none~gge5~0~",
  "T~L~360~300~0~#0000FF~~9pt~~~~comment~Text~1~start~gge8~0~pinpart",
  "E~410~355~10~25~#000000~1~0~none~gge12~0"
]
```

### Bounding Box `BBox`

JSON object representing the boundary of document content.

```json
{
  "x": 4033.1,
  "y": 3282.1,
  "width": 113.3,
  "height": 147.8
}
```

### Layers `layers` (PCB only)

String array recording layer display and activation information.

```json
"layers": [
  "1~TopLayer~#FF0000~true~true~true~",
  "2~BottomLayer~#0000FF~true~false~true~",
  "3~TopSilkLayer~#FFCC00~true~false~true~"
]
```

| # | Field | Description |
|---|-------|-------------|
| 1 | layerid | Layer ID |
| 2 | name | Layer name |
| 3 | color | Layer color |
| 4 | visible | Whether visible |
| 5 | active | Whether active layer |
| 6 | config | Whether layer is configured |
| 7 | transparency | Layer transparency (optional) |
| 8 | type | Layer type (inner layer only, optional) |

### DRC Rule `DRCRULE` (PCB only)

```json
{
  "Default": {
    "trackWidth": 1,
    "clearance": 0.6,
    "viaHoleDiameter": 2.4,
    "viaHoleD": 1.2
  },
  "isRealtime": false,
  "checkObjectToCopperarea": true,
  "showDRCRangeLine": true
}
```

### Preference `preference` (PCB only)

```json
{
  "hideFootprints": "",
  "hideNets": ""
}
```

---

## Schematic Shape Format

### Units

All coordinates and dimensions in schematics use **pixel** as the unit.

### strokeStyle

| Value | Style |
|-------|-------|
| 0 | solid |
| 1 | dashed |
| 2 | dotted |

### Polyline

```
PL~points~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Example: `PL~230 290 430 180 550 340~#000000~1~0~none~gge5~0`

| # | Field | Description |
|---|-------|-------------|
| 1 | PL | Command identifier |
| 2 | points | Point coordinates string |
| 3 | strokeColor | Stroke color |
| 4 | strokeWidth | Stroke width |
| 5 | strokeStyle | Stroke style |
| 6 | fillColor | Fill color |
| 7 | gId | Element ID |
| 8 | locked | Whether locked |

### Wire

```
W~points~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Same format as Polyline with identifier `W`. Used for electrical connections.

### Bus

```
B~points~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Same format as Polyline with identifier `B`.

### Rectangle

```
R~x~y~rx~ry~width~height~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked~c_etype
```

Example: `R~360~250~~~70~80~#000000~1~0~none~gge6~0~`

| # | Field | Description |
|---|-------|-------------|
| 1 | R | Command identifier |
| 2 | x | X coordinate |
| 3 | y | Y coordinate |
| 4 | rx | Horizontal corner radius |
| 5 | ry | Vertical corner radius |
| 6 | width | Width |
| 7 | height | Height |
| 8 | strokeColor | Stroke color |
| 9 | strokeWidth | Stroke width |
| 10 | strokeStyle | Stroke style |
| 11 | fillColor | Fill color |
| 12 | gId | Element ID |
| 13 | locked | Whether locked |
| 14 | c_etype | Element subtype (optional) |

### Circle

```
C~cx~cy~r~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Example: `C~685~315~35~#000000~1~0~none~gge21~0`

### Ellipse

```
E~cx~cy~rx~ry~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Example: `E~420~295~40~25~#000000~1~0~none~gge22~0`

### Line

```
L~x1~y1~x2~y2~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

### Polygon

```
PG~points~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Same format as Polyline with identifier `PG`. Forms a closed region.

### Path

```
PT~pathString~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Example: `PT~M370 280 C410 380 490 300 440 240~#000000~1~0~none~gge23~0~`

### Arc

```
A~pathString~helperDots~strokeColor~strokeWidth~strokeStyle~fillColor~gId~locked
```

Example: `A~M 459.9983 319.997 A 70 170 0 1 1 461.2807 267.9875~~#000000~1~0~none~gge26~0`

### Image

```
I~x~y~width~height~rotation~href~gId~locked
```

### Annotation (Text)

```
T~mark~x~y~rotation~fillColor~fontFamily~fontSize~fontWeight~fontStyle~dominantBaseline~type~value~visible~textAnchor~gId~locked~c_etype
```

| # | Field | Description |
|---|-------|-------------|
| 1 | T | Command identifier |
| 2 | mark | Text mark: L(label) / N(name) / P(prefix) / PK(package) |
| 3 | x | X coordinate |
| 4 | y | Y coordinate |
| 5 | rotation | Rotation angle |
| 6 | fillColor | Fill color |
| 7 | fontFamily | Font family |
| 8 | fontSize | Font size |
| 9 | fontWeight | Font weight |
| 10 | fontStyle | Font style |
| 11 | dominantBaseline | Dominant baseline attribute |
| 12 | type | Text type (comment/spice) |
| 13 | value | Text value |
| 14 | visible | Visibility (1/0) |
| 15 | textAnchor | Text anchor (start/middle/end) |
| 16 | gId | Element ID |
| 17 | locked | Whether locked |
| 18 | c_etype | Element subtype (optional) |

### Pin

Pins use `^^` to separate segments:

```
configure^^pinDot^^pinPath^^name^^number^^dot^^clock
```

Example:
```
P~show~0~1~420~300~~gge31~0^^420~300^^M 420 300 h -20~#880000^^1~398~303~0~1~end~~~#0000FF^^1~405~299~0~1~start~~~#0000FF^^0~403~300^^0~M 400 297 L 397 300 L 400 303
```

**Segment formats:**

1. **Configure** `P~display~electric~spicePin~x~y~rotation~gId~locked`
2. **Pin Dot** `x~y`
3. **Pin Path** `pathString~pinColor`
4. **Name** `visible~x~y~rotation~text~textAnchor~fontFamily~fontSize~fillColor`
5. **Number** Same format as Name
6. **Dot** `visible~x~y`
7. **Clock** `visible~pathString`

### Netlabel

```
N~x~y~rotation~fillColor~name~gId~textAnchor~textX~textY~fontFamily~fontSize~locked
```

### Netflag

Uses `^^` to separate segments:

```
configure^^pinDot^^markString^^shapes...
```

1. **Configure** `F~partId~x~y~rotation~gId~transform~locked`
2. **Pin Dot** `x~y`
3. **Mark String** `text~color~x~y~rotation~textAnchor~visible~fontFamily~fontSize~gId`
4. **Shapes** Remaining items are standard shapes

### Junction

```
J~x~y~radius~fillColor~gId~locked
```

### No Connect Flag

```
O~x~y~gId~pathString~strokeColor~locked
```

### Bus Entry

```
BE~rotation~x1~y1~x2~y2~gId~locked
```

### Arrowhead

```
AR~partType~x~y~gId~rotation~pathString~fillColor~locked~arrowType~arrowSize
```

### Symbol (schlib)

A Symbol consists of header data and internal shapes, separated by `#@$`:

```
LIB~x~y~c_para~rotation~importFlag~gId~puuid~uuid~locked~bindPcbId~convertToPcb~addIntoBom#@$shape1#@$shape2...
```

**Header fields:**

| # | Field | Description |
|---|-------|-------------|
| 1 | LIB | Command identifier |
| 2 | x | X coordinate |
| 3 | y | Y coordinate |
| 4 | c_para | Custom attributes (back-quote separated key-value pairs) |
| 5 | rotation | Rotation angle |
| 6 | importFlag | Import flag |
| 7 | gId | Element ID |
| 8 | puuid | Bound PCB footprint UUID |
| 9 | uuid | Symbol UUID |
| 10 | locked | Whether locked |

---

## PCB Shape Format

### Units

All coordinates and dimensions in PCB use **10mil** as the base unit. For example, a stroke width of 1 means 10mil, 2 means 20mil. Display supports mil, inch, and mm, but storage always uses the 10mil factor.

### TRACK

```
TRACK~strokeWidth~layerid~net~points~gId~locked
```

Example: `TRACK~1~1~~4055.5 3348 4055.5 3346 4131.5 3270 4096 3270~gge5~0`

| # | Field | Description |
|---|-------|-------------|
| 1 | TRACK | Command identifier |
| 2 | strokeWidth | Stroke width |
| 3 | layerid | Layer ID |
| 4 | net | Net name |
| 5 | points | Point coordinates |
| 6 | gId | Element ID |
| 7 | locked | Whether locked |

### RECT

```
RECT~x~y~width~height~layerid~gId~locked~strokeWidth~fill~transform~net~c_etype
```

### CIRCLE

```
CIRCLE~cx~cy~r~strokeWidth~layerid~gId~locked~net~transformarc
```

### ARC

```
ARC~strokeWidth~layerid~net~pathString~helperDots~gId~locked
```

### TEXT

```
TEXT~type~x~y~strokeWidth~rotation~mirror~layerid~net~fontSize~text~pathStr~display~gId~fontFamily~locked~c_etype
```

| # | Field | Description |
|---|-------|-------------|
| 1 | TEXT | Command identifier |
| 2 | type | Text mark (L=label, P=prefix) |
| 3 | x | X coordinate |
| 4 | y | Y coordinate |
| 5 | strokeWidth | Stroke width |
| 6 | rotation | Rotation angle |
| 7 | mirror | Whether mirrored |
| 8 | layerid | Layer ID |
| 9 | net | Net name |
| 10 | fontSize | Font size |
| 11 | text | Text value |
| 12 | pathStr | Path data |
| 13 | display | Whether displayed |
| 14 | gId | Element ID |
| 15 | fontFamily | Font family |
| 16 | locked | Whether locked |
| 17 | c_etype | Element subtype (optional) |

### PAD

```
PAD~shape~x~y~width~height~layerid~net~number~holeR~pointArr~rotation~gId~holeLength~slotPointArr~plated~locked~pasteExpansion~solderExpansion~holeCenter
```

| # | Field | Description |
|---|-------|-------------|
| 1 | PAD | Command identifier |
| 2 | shape | Shape (ELLIPSE/RECT/OVAL/POLYGON) |
| 3 | x | Center X coordinate |
| 4 | y | Center Y coordinate |
| 5 | width | Width |
| 6 | height | Height |
| 7 | layerid | Layer ID |
| 8 | net | Net name |
| 9 | number | Pad number |
| 10 | holeR | Hole diameter |
| 11 | pointArr | Point coordinates |
| 12 | rotation | Rotation angle |
| 13 | gId | Element ID |
| 14 | holeLength | Hole length |
| 15 | slotPointArr | Slot hole points |
| 16 | plated | Plated (Y/N) |
| 17 | locked | Whether locked |
| 18 | pasteExpansion | Paste expansion |
| 19 | solderExpansion | Solder mask expansion |
| 20 | holeCenter | Hole center coordinate |

### VIA

```
VIA~x~y~diameter~net~holeR~gId~locked
```

### HOLE

```
HOLE~x~y~holeR~gId~locked
```

### COPPERAREA

```
COPPERAREA~strokeWidth~layerid~net~pathStr~clearanceWidth~fillStyle~gId~thermal~keepIsland~compressData~locked~name~order~gridTrackWidth~gridClearance~toBoardOutline~fabricationImprove~spokeWidth
```

### SOLIDREGION

```
SOLIDREGION~layerid~net~pathStr~type~gId~teardrop~targetPad~targetWire~locked
```

| # | Field | Description |
|---|-------|-------------|
| 1 | SOLIDREGION | Command identifier |
| 2 | layerid | Layer ID |
| 3 | net | Net name |
| 4 | pathStr | Path data |
| 5 | type | Type (solid/cutout/npth) |
| 6 | gId | Element ID |
| 7 | teardrop | Teardrop |
| 8 | targetPad | Target pad |
| 9 | targetWire | Target wire |
| 10 | locked | Whether locked |

### DIMENSION

```
DIMENSION~layerid~pathString~gId~fontSize~locked~measuringType~fontWidth
```

### FOOTPRINT

A Footprint consists of header data and internal shapes, separated by `#@$`:

```
LIB~x~y~c_para~rotation~importFlag~gId~layerid~uuid~utime~locked#@$shape1#@$shape2...
```

**Header fields:**

| # | Field | Description |
|---|-------|-------------|
| 1 | LIB | Command identifier |
| 2 | x | X coordinate |
| 3 | y | Y coordinate |
| 4 | c_para | Custom attributes |
| 5 | rotation | Rotation angle |
| 6 | importFlag | Import flag |
| 7 | gId | Element ID |
| 8 | layerid | Layer ID |
| 9 | uuid | Footprint UUID |
| 10 | utime | Update time |
| 11 | locked | Whether locked |

### SVGNODE

Free-form graphic combination with JSON string data format. Used for imported graphics, 3D models, etc. in PCB.

```
SVGNODE~{JSON data}
```

---

## Schematic Project File Format (docType: 5)

A schematic project can contain multiple sheets, stored in the `schematics` array:

```json
{
  "editorVersion": "6.5.51",
  "docType": "5",
  "title": "Project Name",
  "description": "",
  "colors": {},
  "schematics": [
    {
      "docType": "1",
      "title": "Sheet_1",
      "description": "",
      "dataStr": {
        "head": {...},
        "canvas": "CA~...",
        "shape": [...],
        "BBox": {...}
      }
    }
  ]
}
```

## PCB File Format (docType: 3)

PCB files do not contain multiple sheets. Structure:

```json
{
  "head": {
    "docType": "3",
    "editorVersion": "6.5.51",
    "newgId": true,
    "c_para": {},
    "hasIdFlag": true
  },
  "canvas": "CA~...",
  "shape": [...],
  "layers": [...],
  "objects": [...],
  "BBox": {...},
  "preference": {...},
  "DRCRULE": {...},
  "netColors": {}
}
```

## Schematic Symbol File Format (docType: 2)

```json
{
  "head": {
    "docType": "2",
    "editorVersion": "6.5.51",
    "newgId": true,
    "c_para": {
      "pre": "U?",
      "name": "PartName",
      "package": "FootprintName"
    },
    "x": 440,
    "y": 315,
    "hasIdFlag": true
  },
  "canvas": "CA~...",
  "shape": [...],
  "BBox": {...}
}
```

## PCB Footprint File Format (docType: 4)

```json
{
  "head": {
    "docType": "4",
    "editorVersion": "6.5.51",
    "newgId": true,
    "c_para": {
      "package": "PackageName",
      "pre": "U?"
    },
    "hasIdFlag": true,
    "x": 4000,
    "y": 3000
  },
  "canvas": "CA~...",
  "shape": [...],
  "layers": [...],
  "objects": [...],
  "BBox": {...}
}
```

---

## Example Files

The `example/` directory in this repository provides complete examples for each document type:

- [Schematic Project Example](example/easyeda-std-schematic-file-format-example.json) - docType: 5 (sheet page docType: 1)
- [Schematic Symbol Example](example/easyeda-std-symbol-file-format-example.json) - docType: 2
- [PCB Example](example/easyeda-std-pcb-file-format-example.json) - docType: 3
- [PCB Footprint Example](example/easyeda-std-footprint-file-format-example.json) - docType: 4
