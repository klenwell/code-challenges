/*
 * SolLewittSvg
 *
 * For course: https://www.freecodecamp.org/news/data-visualizatoin-with-d3/
 *
 * Uses JS Class template:
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
 */

SVG_NS_URL = 'http://www.w3.org/2000/svg'

class SolLewittSvg {
  constructor() {
  }

  /*
   * Static Methods
  **/
  static reproduce(parentId) {
    const canvasWidth = 400
    const canvasHeight = 400
    const parent = document.getElementById(parentId)

    // Create SVG and append to parent element
    const sol = new SolLewittSvg()
    const svg = sol.createSvgEl('svg', {width: canvasWidth, height: canvasHeight})
    parent.appendChild(svg)

    // Create columns
    const colWidth = 10
    const numCols = canvasWidth / colWidth / 2
    for (let i = 0; i < numCols; i++) {
      let x = (i * 20) + 10
      let col = sol.createRect(colWidth, canvasHeight, x, 0)
      //row.setAttribute('mask', 'url(#col-mask)')
      svg.appendChild(col)
    }

    // Create rows
    const rowHeight = 10
    const numRows = canvasHeight / rowHeight / 2
    for (let i = 0; i < numRows; i++) {
      let y = (i * 20) + 10
      let row = sol.createRect(canvasWidth, rowHeight, 0, y)
      //row.setAttribute('mask', 'url(#row-mask)')
      svg.appendChild(row)
    }

    // Create column mask: cut out columns in circle
    const colMask = sol.createSvgEl('mask')
    colMask.setAttribute('id', 'col-mask')
    svg.appendChild(colMask)

    const colMaskRect = sol.createSvgEl('rect')
    colMaskRect.setAttribute('width', canvasWidth)
    colMaskRect.setAttribute('height', canvasHeight)
    colMaskRect.setAttribute('fill', 'black')
    colMask.append(colMaskRect)

    const colMaskCircle = sol.createSvgEl('circle')
    colMaskCircle.setAttribute('cx', canvasWidth / 2)
    colMaskCircle.setAttribute('cy', canvasHeight / 2)
    colMaskCircle.setAttribute('r', canvasHeight / 3)
    colMaskCircle.setAttribute('fill', 'white')
    colMask.append(colMaskCircle)

    // Create row mask: cut out rows not in column
    const rowMask = sol.createSvgEl('mask')
    rowMask.setAttribute('id', 'row-mask')
    svg.appendChild(rowMask)

    const rowMaskRect = sol.createSvgEl('rect')
    rowMaskRect.setAttribute('width', canvasWidth)
    rowMaskRect.setAttribute('height', canvasHeight)
    rowMaskRect.setAttribute('fill', 'white')
    rowMask.append(rowMaskRect)

    const rowMaskCircle = sol.createSvgEl('circle')
    rowMaskCircle.setAttribute('cx', canvasWidth / 2)
    rowMaskCircle.setAttribute('cy', canvasHeight / 2)
    rowMaskCircle.setAttribute('r', canvasHeight / 3)
    rowMaskCircle.setAttribute('fill', 'black')
    rowMask.append(rowMaskCircle)

    // Apply masks
    svg.setAttribute('mask', 'url(#col-mask)')
    svg.setAttribute('mask', 'url(#row-mask)')
  }

  /*
   * Getters
  **/
  get foo() {
    return 'foo'
  }

  /*
   * Methods
  **/
  createSvgEl(el, attrs) {
    attrs = attrs !== undefined ? attrs : {}
    const svg = document.createElementNS(SVG_NS_URL, el)
    for (const [attr, value] of Object.entries(attrs)) {
      svg.setAttribute(attr, value)
    }
    return svg
  }

  createRect(width, height, x, y, attrs) {
    const rectAttrs = {
      width: width,
      height: height,
      x: x,
      y: y
    }
    const elAttrs = Object.assign(rectAttrs, attrs)
    return this.createSvgEl('rect', elAttrs)
  }

  createMask(el, id) {
    const attrs = {
      id: id,
      'data-url': `url(#${id})`
    }
    return this.createSvgEl('mask', attrs)
  }
}
