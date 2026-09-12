// Tarjoman Persian Academic Paper Template
// Formatted for A4 publication with RTL academic layout

#let paper-template(
  title: "عنوان مقاله پژوهشی",
  author: "پژوهشگر / مترجم",
  abstract: none,
  body
) = {
  set document(title: title, author: author)

  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 2.5cm),
    numbering: "1",
  )

  set text(
    font: "Vazirmatn",
    lang: "fa",
    dir: rtl,
    size: 11pt,
  )

  set par(
    justify: true,
    leading: 0.85em,
    first-line-indent: 1.5em,
  )

  align(center)[
    #block(margin: (bottom: 2em))[
      #text(size: 18pt, weight: "bold")[#title]
      #v(0.5em)
      #text(size: 11pt, fill: rgb("#4b5563"))[#author]
    ]
  ]

  if abstract != none [
    #block(
      width: 100%,
      stroke: (right: 2pt + rgb("#2563eb")),
      inset: (right: 1em, top: 0.5em, bottom: 0.5em),
      margin: (bottom: 2em),
      fill: rgb("#f8fafc"),
      [
        #text(weight: "bold", size: 10.5pt)[چکیده:]
        #text(size: 10pt, style: "italic")[#abstract]
      ]
    )
  ]

  body
}

#set page(paper: "a4", margin: (x: 2.5cm, y: 2.5cm), numbering: "1")
#set text(font: "Vazirmatn", lang: "fa", dir: rtl, size: 11pt)
#set par(justify: true, leading: 0.85em, first-line-indent: 1.5em)
