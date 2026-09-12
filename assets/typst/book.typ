// Tarjoman Persian Book Template
// Formatted for A5 publication with RTL typography and Persian pagination

#let book-template(
  title: "عنوان کتاب",
  author: "مترجم",
  body
) = {
  set document(title: title, author: author)

  set page(
    paper: "a5",
    margin: (x: 1.8cm, top: 2.2cm, bottom: 2.2cm),
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

  show heading.where(level: 1): it => block(
    width: 100%,
    align(center)[
      #v(1.5cm)
      #text(size: 16pt, weight: "bold")[#it.body]
      #v(1cm)
    ]
  )

  show heading.where(level: 2): it => block(
    margin: (top: 1.5em, bottom: 0.8em),
    text(size: 13pt, weight: "bold")[#it.body]
  )

  body
}

#set page(paper: "a5", margin: (x: 1.8cm, top: 2.2cm, bottom: 2.2cm), numbering: "1")
#set text(font: "Vazirmatn", lang: "fa", dir: rtl, size: 11pt)
#set par(justify: true, leading: 0.85em, first-line-indent: 1.5em)
